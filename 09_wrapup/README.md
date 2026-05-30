# 09 総まとめ(所要時間: 約10分)

ハンズオン完走おめでとうございます!
00 〜 08 までを通じて、LangChain / LangGraph を使った LLM アプリ構築の主要パターンを一通り体験しました。
本章では、ここまでの内容を振り返り、次の学習リソースを案内します。

## ここまでで身についたこと

| 章 | キーワード | 体験したこと |
|---|---|---|
| 01 基礎 | `ChatBedrockConverse` / LCEL | Bedrock 経由で LLM を呼び、宣言的にチェーンを組む |
| 02 RAG最小構成 | Loader / Splitter / Chroma / Retriever | 文書を埋め込んで検索し、回答に活用する基本フロー |
| 03 AIエージェント | `@tool` / `create_agent` | LLM 自身がツールを選択し連続実行する |
| 05 LangGraph + LangSmith | `StateGraph` / `InMemorySaver` / トレース | 状態を持つエージェントと観測 |
| 06 RAG深掘り | MultiQuery / Ensemble / Rerank / `evaluate` | 検索精度を上げ、客観的に評価する |
| 07 マルチエージェント | `create_supervisor` / hand-off | 役割分担した複数 Agent の協調 |
| 08 MCP連携 | `MultiServerMCPClient` / FastMCP | 外部ツールサーバの取り込み |

## 実務で次に何を作るか — テンプレート

### A. 社内ナレッジ検索ボット\n
- 02章+06章の RAG パターンを土台に\n
- ナレッジソースを **PDF / Confluence / Notion** に拡張\n
- **Bedrock Knowledge Bases** に乗せ替えると運用負荷が激減\n
- フロントは **Streamlit / Slack Bot** など\n

### B. 業務自動化エージェント\n
- 03章+05章+07章 を土台に、Supervisor の下に役割別 Agent を配置\n
- 08章の MCP で **GitHub / Slack / Postgres** に接続\n
- **LangSmith でトラブル時のデバッグ** を必ず設計に組み込む\n

### C. 評価駆動の RAG 改善ループ\n
- 06章の `evaluate` を使って、改善前後を毎回スコア比較\n
- データセットを少しずつ拡張し、退行(regression)を防ぐ\n
- 最終的には CI に組み込んで自動評価\n

## 次に学ぶと良いリソース

### LangChain / LangGraph 公式

- **LangChain Docs**: https://docs.langchain.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **LangChain Academy**(無料コース): https://academy.langchain.com/
- **LangSmith Docs**: https://docs.smith.langchain.com/

### Bedrock 系の発展

- **Bedrock Knowledge Bases**: マネージドな RAG。OpenSearch / Aurora pgvector / Pinecone 等をバックエンドに選択可能
- **Bedrock Agents**: マネージドな Agent 実行環境
- **Guardrails for Bedrock**: 入出力の PII マスキング、有害コンテンツフィルタ
- **Bedrock Studio**: GUI でプロトタイピング
- 公式: https://aws.amazon.com/bedrock/

### MCP エコシステム

- **公式サーバ一覧**: https://github.com/modelcontextprotocol/servers
- **MCP 仕様**: https://modelcontextprotocol.io/
- **AWS 製 MCP サーバ**: AWS Labs などで提供されている各種 AWS リソース連携サーバ

### 評価・観測

- **RAGAS**: RAG 専門の評価フレームワーク (`faithfulness`, `answer_relevancy` などの指標)
- **Arize Phoenix**: オープンソースの LLM 観測ツール(LangSmith の代替)
- **DeepEval**: LLM アプリの単体テスト風フレームワーク

### Python 以外の選択肢

- **LangChain JS/TS**: フロントエンド統合や Edge / Vercel 系でデプロイする場合
- **LlamaIndex**: RAG 寄りに振った別系統のフレームワーク。比較検討の価値あり

## 開発を続けていくときのコツ

1. **早めに LangSmith をオンにする**: トレースを取らずに作ると、後でデバッグが地獄になりがち
2. **小さく評価する**: 5〜10件のテストケースでもいいので、評価データセットを早期に作る
3. **責務を分ける**: 1 エージェントに詰め込みすぎず、必要に応じてマルチエージェントに分解する
4. **ツールには良い docstring を書く**: LLM の選択精度は説明文の質に強く依存する
5. **モデルは適材適所**: Supervisor や軽い分類は Haiku 級、本格生成は Sonnet/Opus 級、と階層で使い分けるとコスト効率が良い
6. **コストを把握する**: Bedrock の CloudWatch メトリクスや LangSmith のトークン消費を定期的にチェック

## おわりに

LangChain は v1 系で **LCEL + LangGraph**(`create_agent` などの標準エージェントも LangGraph ベース)という設計が定着しました。
この延長線上で、観測(LangSmith)・評価(evaluate)・相互運用(MCP)・マルチエージェントといった広がりを 1 通り掴んでいれば、ほとんどの LLM アプリは設計図が描けるはずです。

あとは作りたいものを作るだけです。よい開発を!

---

← [08 MCP連携](../08_mcp/README.md) | [↑ トップに戻る](../README.md)
