# 章別 概要・設計思想・実装計画

各章が「何を教えるか（概要）」「なぜその構成にしたか（設計思想）」「どう実装したか（実装計画）」を 1 枚にまとめたドキュメントです。
教材の全体像を俯瞰し、章をまたいだ依存関係や意図を把握するために使います。

> 最終更新: 2026-05-30 / 対象: langchain 1.x 系（[design_decisions.md](design_decisions.md) 参照）

---

## 全体構成

本教材は **速習コース（00〜04章）** と **発展コース（05〜09章）** の 2 部構成です。

| コース | 章 | ねらい |
|---|---|---|
| 速習 | 00 セットアップ 〜 04 中間まとめ | 1.5 時間程度で「LLM を業務で試す PoC」を作れる基礎 |
| 発展 | 05 LangGraph 〜 09 総まとめ | 観測・評価・協調・相互運用といった実務寄りの広がり |

### 章をまたぐ依存関係

```
01 → 02 → 03 → 04（速習コースは直線）
              ↓
05（LangGraph/LangSmith：発展コースの土台）
   ├→ 06（RAG深掘り：05 の LangGraph を活用）
   │     └→ 07（マルチエージェント：06 が作る .chroma_v2 を検索ツールに使う）
   └→ 08（MCP：05 の create_agent を活用）
                          ↓
                         09（総まとめ）
```

**重要な実体依存**: 07 章の Researcher エージェントは、06 章の Notebook が生成する `06_rag_advanced/.chroma_v2`（ベクトルDB）を検索ツールとして再利用する。07 章を動かす前に 06 章を通しで実行しておく必要がある。

### 全章を貫く設計思想

- **最小構成から始める**: 各章は「動く最小例」を先に見せ、説明は後付け。1.5 時間ハンズオン志向に合わせ、1 章 1 ファイルで完結。
- **Bedrock + 低コストモデル前提**: 既定は Amazon Nova Lite。動作確認が目的なので安価・純正・非中国発を優先（[design_decisions.md](design_decisions.md) §1）。
- **段階的に積み上げる**: 前章の概念を次章で発展させる（例: 03 のエージェント → 05 の LangGraph 化 → 07 のマルチ化）。
- **観測と評価を早期に**: 05 で LangSmith、06 で `evaluate` を導入し、「なんとなく動く」を「数値で確認できる」へ。

---

## 01 基礎（約20分）

- **概要**: LangChain 経由で Bedrock の LLM を呼び、PromptTemplate で整形し、LCEL（`prompt | model | parser`）でチェーンを組む。最後にストリーミング応答。
- **設計思想**: すべての出発点。「Bedrock を叩けること」と「LCEL という宣言的記法」を体に入れることだけに絞り、RAG やツールなどの応用要素は持ち込まない。
- **実装計画**:
  1. `ChatBedrockConverse` で最小呼び出し（Hello Bedrock）
  2. `ChatPromptTemplate` で System / User メッセージをテンプレ化
  3. `prompt | llm | StrOutputParser` でチェーン化
  4. ストリーミングでトークン単位の受信を体験
- **Done 条件**: 最後のセルでストリーミング応答が文字単位で表示される。

## 02 RAG 最小構成（約30分）

- **概要**: 文書をベクトル化して Chroma に保存し、質問に対して検索した内容を根拠に回答する RAG の基本フロー。
- **設計思想**: RAG を「Load → Split → Embed → Store → Retrieve → 注入 → 生成」という一本道のパイプラインとして提示。精度改善（→06章）はまだ扱わず、フロー理解に集中する。
- **実装計画**:
  1. `TextLoader` で Markdown 文書をロード
  2. `RecursiveCharacterTextSplitter` でチャンク分割
  3. `BedrockEmbeddings`（Titan）でベクトル化 → `Chroma` に保存
  4. Retriever で類似検索 → LCEL チェーンでプロンプトに注入して回答
- **Done 条件**: サンプル文書の内容に関する質問に、文書を根拠にした回答が返る。

## 03 AIエージェント 最小構成（約20分）

- **概要**: 「LLM 自身がツールを選んで呼ぶ」エージェントの最小例。`@tool` で自作関数をツール化し、`create_agent` でループ実行する。
- **設計思想**: エージェントの本質（LLM が次のアクションを決める）を、時刻取得・加算という単純なツールで体験させる。langchain 1.x 標準の `create_agent` に統一し、入出力を `{"messages": [...]}` 形式にすることで **05 章の LangGraph へ自然につなげる**。
- **実装計画**:
  1. `@tool` デコレータで `get_current_time` / `add_numbers` を定義
  2. `create_agent(llm, tools=..., system_prompt=...)` でエージェント構築（旧 `AgentExecutor` + `create_tool_calling_agent` の統合版）
  3. 時刻・計算・一般知識の 3 パターンを実行し、ツールが呼ばれる／呼ばれないを観察
- **Done 条件**: `result["messages"]` の履歴でツール呼び出し（Ai の tool_calls → Tool メッセージ）が見え、最終回答が得られる。
- **移行メモ**: langchain 0.3 → 1.x で書き換えた章（[design_decisions.md](design_decisions.md) §5）。

## 04 中間まとめ（約5分）

- **概要**: 速習コース（01〜03）の振り返りと、発展コースへ進むかの判断軸。
- **設計思想**: ここで一区切りつけ、興味に応じて 05〜08 を**独立に**選べることを示す。学習者の離脱ポイントをあえて設け、達成感を区切る。
- **実装計画**: コードなし。学んだこと・作れるもの・次に進む章の対応表を提示。

## 05 LangGraph + LangSmith（90〜120分）

- **概要**: LangGraph で「状態を持つエージェント」を組み、LangSmith で内部動作を可視化する。prebuilt の `create_agent` と手書き `StateGraph` の両方を体験。
- **設計思想**: 03 章のブラックボックスなエージェントを「グラフ（ノード／エッジ）」として開いて見せる。`create_agent`（楽な道）と手書き `StateGraph`（理解の道）を**対比**させ、内部構造の理解と可観測性（LangSmith）をセットで導入する。発展コースの土台。
- **実装計画**:
  1. LangSmith 環境変数の確認（未設定でも動く設計）
  2. `create_agent` で 1 行エージェント
  3. LangSmith ダッシュボードでトレース確認
  4. `StateGraph` + `ToolNode` + `tools_condition` を手書き
  5. Mermaid / ASCII でグラフ可視化
  6. `InMemorySaver` + `thread_id` で複数ターン会話
- **Done 条件**: prebuilt / 手書き両方でツール呼び出し応答が返り、LangSmith にツリー表示され、InMemorySaver で会話が引き継がれる。

## 06 RAG 深掘り（90〜120分）

- **概要**: 02 章の素朴な top-k 検索の限界を体感し、MultiQuery / Ensemble / Rerank の 3 手法と LangSmith `evaluate` による定量評価を学ぶ。
- **設計思想**: 「改善した気がする」を「数値で確認できる」へ進化させるのが主眼。retriever だけを差し替えて比較できるよう、RAG を **LangGraph でノード化**（05 章の応用）し、各手法を同じ土俵で評価する。実データ（Markdown + PDF）を扱う。
- **実装計画**:
  1. 複数 Loader（`TextLoader` + `PyPDFLoader`、PDF は `reportlab` で動的生成）で統合インデックス構築
  2. ベースライン（top-k）
  3. `MultiQueryRetriever`（言い換えで検索漏れ低減）
  4. `EnsembleRetriever`（密ベクトル + BM25 ハイブリッド）
  5. `BedrockRerank` + `ContextualCompressionRetriever`（再ランキング）
  6. `retrieve_node → generate_node` の RAG グラフ化
  7. `langsmith.evaluation.evaluate` でデータセット評価・スコア比較
- **Done 条件**: 改善版 Retriever がベースラインより関連チャンクを上位に返すケースを確認、LangSmith に評価結果が記録される。
- **移行メモ**: Retriever 群を `langchain_classic.retrievers` へ変更した章（[design_decisions.md](design_decisions.md) §5）。後続の 07 章が使う `.chroma_v2` を生成する。

## 07 マルチエージェント（60〜90分）

- **概要**: 役割の異なる 2 エージェント（Researcher / Writer）を Supervisor パターンで協調させる最小構成。
- **設計思想**: 「1 エージェントに詰め込みすぎない」という実務的な責務分割を体験させる。中央集権型の Supervisor を題材に、hand-off（誰がいつ何をしたか）を LangSmith で可視化。06 章の RAG 資産を**ツールとして再利用**し、章間のつながりを実感させる。
- **実装計画**:
  1. 06 章の `.chroma_v2` を再ロードし、`@tool` で `retrieve_company_docs` 化
  2. `create_agent` で Researcher（検索ツールあり）構築
  3. `create_agent` で Writer（ツールなし）構築
  4. `create_supervisor` で 2 エージェントをオーケストレーション → `.compile()`
  5. `.invoke()` / `.stream()` で Researcher → Writer の流れを観察
- **Done 条件**: 複合タスクで Researcher → Writer の順に呼ばれて最終文章が返り、LangSmith に協調のツリーが現れる。
- **前提**: 06 章を通しで実行し `.chroma_v2/` を生成済みであること。

## 08 MCP 連携（60〜90分）

- **概要**: MCP（Model Context Protocol）の基本構成を理解し、LangGraph エージェントに MCP サーバ提供のツールを取り込む。自作サーバと公式 filesystem サーバを同時接続。
- **設計思想**: ツールの供給源を「自前コード」から「標準プロトコル経由の外部サーバ」へ広げる相互運用性がテーマ。Server / Client / Transport の関係を、自作（FastMCP）と公式（npx）の 2 サーバを stdio で同時に繋いで体感させる。05 章の `create_agent` をそのまま流用し、「ツールの出所が変わるだけ」を強調。
- **実装計画**:
  1. Node.js / npx の存在確認
  2. 自作 `mcp_servers/math_server.py`（FastMCP）の中身確認
  3. `MultiServerMCPClient` で stdio 接続 → `get_tools()` でツール取得
  4. `create_agent` に MCP ツールを渡して計算実行
  5. 公式 `@modelcontextprotocol/server-filesystem` を npx 経由で起動
  6. math + filesystem の複数サーバを同時利用し、エージェントが使い分ける
- **Done 条件**: 自作 math サーバで計算、filesystem サーバで `data/` の一覧・読み出しができ、LangSmith に MCP ツール呼び出しが可視化される。

## 09 総まとめ（約10分）

- **概要**: 全章の振り返りと、実務テンプレート・次の学習リソース・開発のコツの案内。
- **設計思想**: 学んだ部品を「実際に何を作れるか」に接続して締める。Bedrock Knowledge Bases / Agents、MCP エコシステム、評価ツール（RAGAS 等）など発展先を提示し、教材の外へ橋渡しする。
- **実装計画**: コードなし。到達点の整理、テンプレート（社内ナレッジ検索 / 業務自動化 / 評価駆動改善）、公式リソースリンク、運用のコツをまとめる。

---

## 参考

- 設計判断（モデル・認証・バージョン方針・移行詳細）: [design_decisions.md](design_decisions.md)
- セットアップ: [00_setup.md](00_setup.md) / [05_langsmith_setup.md](05_langsmith_setup.md)
