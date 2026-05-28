# sandbox — 自由実験スペース

ハンズオン(01〜08章)で学んだ内容を使って、自由にコードを書いて試すための場所です。
教材のように手順は決まっていません。思いついたことを `sandbox.ipynb` でどんどん試してください。

## 使い方

1. [sandbox.ipynb](sandbox.ipynb) を開く
2. 先頭の **環境変数セル**(必須)を実行 → Bedrock / LangSmith の設定が読まれる
3. **import 一覧セル** で、使いたい機能のコメント(`#`)を外す
4. **LLM 初期化セル** を実行
5. あとは空のセルで自由に実験

> 出力は nbstripout により git にコミットされません(リポジトリ全体の設定)。気にせず実行・保存してOKです。

## 用意してあるもの

```
sandbox/
├── README.md
├── sandbox.ipynb            # 自由実験用Notebook(env + import一覧 + 空セル)
├── data/
│   └── sample_knowledge.md  # RAG実験用のサンプル文書(自由に追加・差し替えOK)
└── mcp_servers/
    └── example_server.py    # MCP実験用の自作サーバ(stdio)
```

## 実験のヒント(章別の起点)

| やりたいこと | 参考章 | 主なクラス/関数 |
|---|---|---|
| LLMを呼ぶ / LCELチェーン | 01 | `ChatBedrockConverse`, `ChatPromptTemplate`, `StrOutputParser` |
| RAG | 02・06 | `TextLoader`, `RecursiveCharacterTextSplitter`, `Chroma`, `as_retriever` |
| 検索精度向上 | 06 | `MultiQueryRetriever`, `EnsembleRetriever`, `BedrockRerank` |
| エージェント | 03・05 | `@tool`, `create_react_agent` |
| 状態を持つグラフ | 05 | `StateGraph`, `MessagesState`, `ToolNode`, `MemorySaver` |
| マルチエージェント | 07 | `create_supervisor` |
| MCP連携 | 08 | `MultiServerMCPClient` |
| 評価 | 06 | `langsmith` の `evaluate` |

## メモ

- `data/` に自分のテキストやPDFを置けば、すぐRAGの題材にできます。
- `mcp_servers/example_server.py` を編集すれば、自作MCPツールを増やせます。
- Chroma を永続化する場合は `persist_directory="./.chroma_sandbox"` のように sandbox 配下を指定してください(`.gitignore` で除外済み)。
