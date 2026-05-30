# 設計判断メモ（Design Decisions）

LangChain × Amazon Bedrock ハンズオン教材の主要な設計判断を記録するドキュメントです。
「なぜこの構成にしたか」を残し、将来の変更時に判断の前提を見失わないことを目的とします。

> 最終更新: 2026-05-30

---

## 1. モデル選定

### チャットモデル: `us.amazon.nova-lite-v1:0`
- **判断**: Bedrock で最安級・Amazon 純正・非中国発の Nova Lite を既定とする。
- **理由**: 「動作確認ができれば良いので安いモデルを使いたい。中国発（DeepSeek / Qwen 等）は除外」というユーザー方針。
- **運用**: Anthropic 製モデル等へ切り替える際も、**コストと出自**を確認してから採用する。
  - 切り替え先の例: `anthropic.claude-3-haiku-20240307-v1:0`（Nova で Tool Calling が不安定な場合の代替。初回のみ「使用フォーム」提出が必要）。
- **Nova 2 系について（2026-05 時点）**: 後継の Amazon Nova 2 Lite（例 `us.amazon.nova-2-lite-v1:0`）が提供されている。長コンテキスト・推論強化などの利点があるが**価格が大きく上がる**ため、本教材の「安価に動作確認」という目的では **Nova Lite v1 を維持**する。コスト許容できるなら環境変数 `BEDROCK_CHAT_MODEL_ID` の差し替えのみで移行可能（コードは無変更）。

### 埋め込みモデル: `amazon.titan-embed-text-v2:0`
- RAG（02 / 06 章）のベクトル化に使用。

### Rerank モデル: `amazon.rerank-v1:0`
- 06 章の Reranker セクションで使用。`.env` の `BEDROCK_RERANK_MODEL_ID` で上書き可能。
- リージョン未提供の場合があるため、該当セルは失敗してもスキップ可能な作りにしている。

---

## 2. AWS 認証方式

- **判断**: ホストの `~/.aws` を DevContainer にマウントする（`aws sso login` のトークンキャッシュを流用）。
- **理由**: ユーザーは WSL 上で `aws sso login` する運用のため、`.env` への認証情報直書きではなくマウント方式を採用。
- **運用**: `.env` では `AWS_PROFILE` と `AWS_REGION` のみ管理し、**認証情報そのものは触らない**。

---

## 3. 教材形式

- **判断**: Jupyter Notebook（`.ipynb`）、章ごとに 1 ファイル。
- **理由**: ユーザー指定。1.5 時間程度で通せるシンプルなハンズオン志向。
- **運用**: 各セルが順番に実行可能で、Markdown で説明を挟む。
- **補足（編集時の注意）**: `.ipynb` は VSCode で開いたまま外部から編集すると競合・上書きが起きる。編集前にエディタ上で当該ファイルを閉じること。
- **出力の Git 管理**: `nbstripout` を git の clean filter として登録し、Notebook の実行結果（outputs）はコミットしない（`postCreateCommand` で `nbstripout --install`）。

---

## 4. LangChain バージョン方針

### 現行: langchain 1.x 系
- **判断**: 2026-05-30 に langchain **0.3 系 → 1.x 系**へ全面移行。
- **主要バージョン**（`requirements.txt` 参照）:

  | パッケージ | バージョン |
  |---|---|
  | langchain | >=1.3, <2 |
  | langchain-core | （依存解決で）>=1.4 |
  | langchain-aws | >=1.5, <2 |
  | langchain-community | >=0.4, <0.5 |
  | langchain-chroma | >=1.1, <2 |
  | langchain-text-splitters | >=1.1, <2 |
  | langgraph | >=1.2, <2 |
  | langgraph-supervisor | >=0.0.31 |
  | langchain-mcp-adapters | >=0.2, <0.3 |
  | deepagents | >=0.6, <0.7 |

- **理由**: `deepagents`（最新 0.6.x）を pip install 対象に追加したいというユーザー要望。deepagents は **langchain 1.x（langchain-core>=1.4）必須**のため、教材全体を 1.x へ引き上げる選択を採用した。

### deepagents 追加に関する補足
- deepagents は依存として `langchain-anthropic` / `langchain-google-genai` も導入するが、本教材は **Bedrock 構成のため、それらの API キーは不要**（インストールされるだけ）。

---

## 5. langchain 0.3 → 1.x 移行で行った変更

破壊的変更は限定的で、import 修正が必要だったのは **03 章と 06 章のみ**だった。

### 変更が必要だった章
| 章 | 旧（0.3 系） | 新（1.x 系） |
|---|---|---|
| **03 Agent** | `from langchain.agents import AgentExecutor, create_tool_calling_agent` | `from langchain.agents import create_agent` |
| **06 RAG 深掘り** | `from langchain.retrievers import ...` / `.multi_query` | `from langchain_classic.retrievers import ...` |

- **03 章**: `AgentExecutor` + `create_tool_calling_agent`（Agent本体と実行ループの2分割）は、1.x の `create_agent` 1つに統合された。
  - 入出力が `{"input": ...}` / `{"output": ...}` から **`{"messages": [...]}` 形式**（OpenAI 互換のメッセージ列）に変わる。
  - `MessagesPlaceholder("agent_scratchpad")` は不要（内部で自動処理）。
  - 第 5 章の LangGraph と同じ入出力形式になり、章のつながりが自然になった。
- **06 章**: `MultiQueryRetriever` / `EnsembleRetriever` / `ContextualCompressionRetriever` は 1.x では `langchain_classic.retrievers` に移動。ロガー名も `langchain_classic.retrievers.multi_query` に変わる。

### 変更が不要だった章
- **01 / 02 / 05 / 07 / 08 章**は import 変更不要。
  - `langgraph.prebuilt.create_react_agent` / `ToolNode` / `tools_condition`、`langgraph_supervisor.create_supervisor`、`langchain_mcp_adapters.client.MultiServerMCPClient`、`langsmith` などは 1.x でもパスが不変。

### 既知の注意点
- `langchain_community`（02 / 06 章の Loader・BM25Retriever）は動作するが「sunset 予定」の **DeprecationWarning** が出る。動作優先で現状維持。将来は standalone パッケージへの移行を検討。

---

## 6. 検証状況（移行時点）

- ✅ 隔離 venv で 1.x スタックの依存解決がクリーンに成立。
- ✅ 変更した全 import が 1.x で解決。
- ✅ `create_agent` が `CompiledStateGraph` を構築（グラフ構築まで確認）。
- ✅ 両 Notebook の JSON 妥当性・全コードセルの構文を確認。
- ⚠️ **実機の Bedrock 呼び出しによる動作確認は未実施**（認証情報・コストが絡むため）。DevContainer で `pip install -r requirements.txt` 後、各 Notebook を通しで実行して最終確認すること。

---

## 7. 非推奨 API のクリーンアップ（2026-05-30）

各章の最新化レビューで、**正式に非推奨化された API** を現行の代替へ置き換えた（Web 検索で非推奨ステータスを確認の上）。

| 旧（非推奨） | 新（現行推奨） | 対象章 | 根拠 |
|---|---|---|---|
| `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` | 05 / 07 / 08 | LangGraph v1 で非推奨・**v2 で削除予定**。`create_agent` は同等のエージェントを返す後継 |
| `MemorySaver` | `InMemorySaver` | 05 | `MemorySaver` は `InMemorySaver` のエイリアス。正式名は `InMemorySaver` |

- **移行の注意**: `create_react_agent(llm, tools, prompt=...)` → `create_agent(llm, tools=..., system_prompt=...)`（振る舞いの指示の引数名が `prompt` → `system_prompt`）。`name=` は両者で利用可。
- **互換性検証済み**: `langgraph_supervisor.create_supervisor` は `create_agent` 製エージェントを束ねて `compile()` できることを隔離 venv で確認（07 章）。MCP ツール + `ainvoke` も `create_agent` で動作（08 章）。

### 置き換えなかった「保守モード」依存（代替が存在しないため維持）
- **`langchain_classic.retrievers`**（06 章: `MultiQueryRetriever` / `EnsembleRetriever` / `ContextualCompressionRetriever`）: 2026-12 までセキュリティ保守。**これらは classic 以外に提供されておらず、ドロップイン代替が無い**ため現状維持。
- **`langchain_community`**（02 / 06 章: `TextLoader` / `PyPDFLoader` / `BM25Retriever`）: パッケージは sunset だが**当該クラスは非推奨でなく標準代替も無い**ため現状維持。

いずれも該当セルにコメントで注記済み。完全終了が告知された場合に移行を再検討する。
