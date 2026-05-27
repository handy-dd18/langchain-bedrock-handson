# 04 まとめと次の一歩(所要時間: 約5分)

お疲れさまでした! このハンズオンで体験した内容を振り返り、次に学ぶと良いトピックを紹介します。

## このハンズオンで学んだこと

| 章 | キーポイント |
|---|---|
| 01 基礎 | `ChatBedrockConverse` で LLM を呼び、LCEL (`prompt | llm | parser`) でチェーンを組む |
| 02 RAG | Loader → Splitter → Embeddings → VectorStore → Retriever → Chain の流れ |
| 03 Agent | `@tool` で関数をツール化、`create_tool_calling_agent` + `AgentExecutor` でループ実行 |

## 次の一歩

### より複雑なエージェント / ワークフロー → LangGraph
状態遷移を持つマルチステップなエージェントや、人間レビューを挟むワークフローを書くなら **LangGraph** が標準です。
- 公式: https://langchain-ai.github.io/langgraph/

### 観測・デバッグ → LangSmith
プロンプト・トークン消費・チェーン中の中間出力を可視化できるトレーシングサービス。
本番運用や開発デバッグに必須レベル。
- 公式: https://docs.smith.langchain.com/

### RAG をもう少し深掘り
- **多様な Loader**: PDF (`PyPDFLoader`)、Web (`WebBaseLoader`)、Notion、Confluence など
- **再ランキング**: 検索 Top-k をさらに高精度で並べ替える(Cohere Rerank、Bedrock Rerank など)
- **ハイブリッド検索**: 密ベクトル + キーワード(BM25)の併用
- **評価**: RAGAS などで RAG パイプラインの精度を測る

### エージェントの発展
- **複数ツール選択** + **計画立案**: LangGraph で計画・実行・振り返りループ
- **マルチエージェント**: 役割の違うエージェントを協調させる
- **MCP (Model Context Protocol)**: 外部のツール群を MCP サーバ経由で接続

### Bedrock 側の発展
- **Bedrock Knowledge Bases**: マネージドな RAG(自前で Chroma 等を持たなくて済む)
- **Bedrock Agents**: マネージドなエージェント
- **Guardrails**: 入出力のフィルタリング・PII マスキング

## おわりに

ここまでで「LangChain で LLM アプリの基本パターンを組む」感覚は掴めたはずです。
あとはやりたいことに合わせて、上記の発展トピックから必要なものを掘り下げていきましょう。

---

← [03 エージェント](../03_agent/)
