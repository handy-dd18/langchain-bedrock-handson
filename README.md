# LangChain × AWS Bedrock ハンズオン

LangChainの基本〜RAG〜AIエージェントまでを、**約90分**で一通り体験するためのハンズオン教材です。

> [!WARNING]
> **本ハンズオンはAI(Claude)により生成されています。**
> 内容・コード・手順に誤りが含まれている可能性があります。実行前にコードや設定を確認し、エラーが出た場合は原文の公式ドキュメント(LangChain / AWS Bedrock 等)も参照してください。
> またライブラリのバージョンアップによりAPIが変わっている可能性もあるため、想定どおり動かない場合はバージョンや最新の使い方を確認してください。

## 学習ゴール

- LangChainの基本(Model / Prompt / LCELチェーン)を理解する
- RAG (Retrieval Augmented Generation) の流れを最小構成で動かす
- AIエージェント(Tool呼び出し)の最小構成を動かす

「ざっくり構築でき、流れが理解できる」レベルがゴールです。

## 前提条件

### 動作環境

| 項目 | 内容 |
|---|---|
| ホストOS | Windows 11 + WSL2(Ubuntu)を想定。Linux / macOS でも動作する想定 |
| エディタ | Visual Studio Code |
| 必須拡張機能 | Dev Containers, Python, Jupyter(Dev Container起動時に自動インストール) |
| コンテナ | Docker Desktop(または Docker Engine)が起動していること |
| 言語ランタイム | Python 3.11(DevContainer内で自動構築) |

### AWS 側の前提

- AWS Bedrock が利用可能なAWSアカウントを持っていること
- 本ハンズオンで使用する **Amazon Nova Lite / Titan Text Embeddings V2** は、2025年9月29日以降のBedrock仕様変更により **モデルアクセス申請なしで自動的に利用可能** です(詳細は [docs/00_setup.md](docs/00_setup.md) 参照)
- Bedrockを利用するリージョンが決まっていること(例: `us-east-1`)
- ホスト側で `aws` CLI v2 がインストール済みで、SSO等によるログインが行える状態
  - 例: `aws sso login --profile <your-profile>` が成功すること
  - `~/.aws/config` にプロファイル設定があること
  - 本教材では `~/.aws/` ディレクトリをDevContainerにマウントして認証情報を共有します
- IAMロールに `bedrock:InvokeModel` 権限が付与されていること

### 主要ライブラリ(`requirements.txt` で自動インストール)

| ライブラリ | バージョン目安 |
|---|---|
| langchain | >=0.3, <0.4 |
| langchain-aws | >=0.2 |
| langchain-chroma | >=0.1 |
| chromadb | >=0.5 |
| boto3 | >=1.34 |

## 構成

### 速習コース(約90分)

| 章 | 内容 | 所要時間 |
|---|---|---|
| [00 セットアップ](docs/00_setup.md) | DevContainer起動 + Bedrock疎通 | 15分 |
| [01 LangChain基礎](01_basics/README.md) | Chat Model / Prompt / LCEL | 20分 |
| [02 RAG最小構成](02_rag/README.md) | 文書 → 埋め込み → 検索 → 生成 | 30分 |
| [03 AIエージェント](03_agent/README.md) | Tool定義 → Agent実行 | 20分 |
| [04 中間まとめ](04_wrapup/README.md) | ここまでの振り返り | 5分 |

### 発展コース(各章 60〜120分、章ごとに分割受講可)

| 章 | 内容 | 所要時間 |
|---|---|---|
| [05 LangGraph + LangSmith](05_langgraph/README.md) | StateGraph / create_react_agent / トレース可視化 / MemorySaver | 90〜120分 |
| [06 RAG深掘り](06_rag_advanced/README.md) | MultiQuery / Ensemble / Rerank / 評価 | 90〜120分 |
| [07 マルチエージェント](07_multi_agent/README.md) | Supervisor パターン | 60〜90分 |
| [08 MCP連携](08_mcp/README.md) | langchain-mcp-adapters / stdio | 60〜90分 |
| 09 総まとめ(準備中) | 学習リソース総覧 | 10分 |

> 発展コースを始める前に [LangSmithセットアップガイド](docs/05_langsmith_setup.md) でAPIキーを設定しておくと、05章以降の全実行がトレース可視化されます(無料、必須ではありません)。

## クイックスタート

```bash
# 1. リポジトリを開いてDev Containerで起動
#    VSCode > "Reopen in Container"

# 2. ホスト側で AWS にログイン(コンテナ内ではなく WSL/ホスト側で実行)
aws sso login --profile <your-profile>

# 3. .env を用意
cp .env.example .env
# .env を編集し、AWS_PROFILE と AWS_REGION を設定

# 4. 章ごとの Notebook を順に開いて実行
#    01_basics/basics.ipynb → 02_rag/rag.ipynb → 03_agent/agent.ipynb
```

## 使用モデル

- **チャット**: `us.amazon.nova-lite-v1:0`(Amazon Nova Lite、安価)
- **埋め込み**: `amazon.titan-embed-text-v2:0`

いずれも申請不要で自動アクセス可能です。詳細は [docs/00_setup.md](docs/00_setup.md) を参照してください。
