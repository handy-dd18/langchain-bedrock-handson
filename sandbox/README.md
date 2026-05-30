# sandbox — 自由実験スペース

ハンズオン(01〜08章)で学んだ内容を使って、自由にコードを書いて試すための場所です。
教材のように手順は決まっていません。思いついたことを `sandbox.ipynb` でどんどん試してください。

## はじめての準備(初回のみ)

雛形ファイル `sandbox.ipynb.example` を `sandbox.ipynb` という名前にコピーしてから開いてください。

```bash
cp sandbox/sandbox.ipynb.example sandbox/sandbox.ipynb
```

`sandbox.ipynb` は **`.gitignore` 対象** なので、自由に編集・実行・保存しても git にコミットされません。
雛形(`.example`)は git 管理されているので、最新の雛形が必要になったらいつでもこのリポジトリから再取得できます。

`data/` や `mcp_servers/` 配下に自分でファイルを追加した場合も、**雛形以外は git 管理外** になります(後述)。

## 使い方

1. 上記コマンドで `sandbox.ipynb` を作成し、それを VSCode で開く
2. 先頭の **環境変数セル**(必須)を実行 → Bedrock / LangSmith の設定が読まれる
3. **import 一覧セル** で、使いたい機能のコメント(`#`)を外す
4. **LLM 初期化セル** を実行
5. その下の空セルで自由に実験

## 用意してあるもの(git 管理されている雛形)

```
sandbox/
├── README.md
├── sandbox.ipynb.example       # 自由実験用Notebookの雛形(コピーして使う)
├── data/
│   └── sample_knowledge.md     # RAG実験用のサンプル文書
└── mcp_servers/
    └── example_server.py       # MCP実験用の自作サーバ雛形
```

## git 管理外になるもの(自由に追加・編集してOK)

`sandbox/` 配下に追加したファイルは、上記の雛形を除いて **すべて git 管理外** に設定してあります。
具体的には以下が無視されます:

- `sandbox/sandbox.ipynb`(雛形をコピーして使う実験用ノート)
- `sandbox/.chroma_sandbox/`(Chroma 永続化用)
- `sandbox/data/` 配下の `sample_knowledge.md` 以外の追加文書(自分の社内文書や PDF など)
- `sandbox/mcp_servers/` 配下の `example_server.py` 以外の自作 MCP サーバ

業務寄りの題材で試してもgit に上がらないので、気軽に実験できます。

## 実験のヒント(章別の起点)

| やりたいこと | 参考章 | 主なクラス/関数 |
|---|---|---|
| LLMを呼ぶ / LCELチェーン | 01 | `ChatBedrockConverse`, `ChatPromptTemplate`, `StrOutputParser` |
| RAG | 02・06 | `TextLoader`, `RecursiveCharacterTextSplitter`, `Chroma`, `as_retriever` |
| 検索精度向上 | 06 | `MultiQueryRetriever`, `EnsembleRetriever`, `BedrockRerank` |
| エージェント | 03・05 | `@tool`, `create_agent` |
| 状態を持つグラフ | 05 | `StateGraph`, `MessagesState`, `ToolNode`, `InMemorySaver` |
| マルチエージェント | 07 | `create_supervisor` |
| MCP連携 | 08 | `MultiServerMCPClient` |
| 評価 | 06 | `langsmith` の `evaluate` |

## メモ

- Chroma を永続化する場合は `persist_directory="./.chroma_sandbox"` のように指定すると、`.gitignore` 対象になっているのでそのまま使えます。
- 雛形を更新したい(全員に共有したい変更がある)場合は `sandbox.ipynb.example` の方を直接編集してください。
