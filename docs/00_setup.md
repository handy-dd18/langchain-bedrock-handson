# 00 セットアップ(所要時間: 約15分)

## このステップのゴール
- DevContainer が起動でき、Notebookが実行可能
- AWS Bedrock に Notebook から接続できる

## 1. Bedrock モデルへのアクセス可否を確認

> 📣 **2025年9月29日以降、Amazon Bedrock のサーバーレス基盤モデルは AWS アカウントに対して自動的に有効化** されるようになりました。
> 以前必要だった「Model access」画面でのリクエスト操作は廃止されており、原則 **追加のアクセス申請なしに利用できます**。
>
> 参考: [Simplified model access in Amazon Bedrock (AWS Security Blog)](https://aws.amazon.com/blogs/security/simplified-amazon-bedrock-model-access/)

本ハンズオンのデフォルトモデルは以下で、いずれもサーバーレスで自動アクセス可能なため申請は不要です:

- `Amazon Nova Lite`(チャット用) — 申請不要
- `Amazon Titan Text Embeddings V2`(埋め込み用) — 申請不要

### Anthropic製モデルを使う場合(オプション)

第3章でフォールバックとして紹介している `Claude 3 Haiku` など **Anthropic 製モデルだけは例外** で、自動有効化された状態でも **初回利用時に一度だけ「使用フォーム」(use case details の提出)が必要** です。

手順(必要な場合のみ):
1. AWSコンソール → Amazon Bedrock → 左メニュー「Model catalog」または該当モデルのページ
2. Anthropic 製モデルを選び、初回はユースケースを記載するフォームを送信
3. 数分程度で利用可能になります

### アクセス制御

組織で IAM ポリシーや SCP によりモデル利用が制限されている場合は、`bedrock:InvokeModel` 等の権限が自分のロールに付与されているか管理者に確認してください。

## 2. ホスト(WSL)で AWS にログイン

```bash
# 既に aws CLI v2 とプロファイル設定が済んでいる前提
aws sso login --profile <your-profile-name>
```

ログイン後、`~/.aws/sso/cache/` 配下に短期トークンが保存されます。
DevContainerはホストの `~/.aws/` をマウントするため、コンテナ内でもそのまま `AWS_PROFILE` 経由で認証が通ります。

## 3. リポジトリを Dev Container で開く

1. VSCodeでこのリポジトリを開く
2. 右下の通知から「Reopen in Container」を選択(または `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`)
3. 初回ビルドは2〜3分程度待つ

## 4. `.env` を用意

リポジトリルートで:

```bash
cp .env.example .env
```

`.env` を開いて以下を編集:

- `AWS_PROFILE` = 手順2で使ったプロファイル名
- `AWS_REGION` = Bedrockを利用するリージョン(例 `us-east-1`、`ap-northeast-1`)
- `BEDROCK_CHAT_MODEL_ID` = リージョン地域に応じてプレフィックスを変更

### Nova Lite モデルIDとリージョンの対応

Nova Lite はクロスリージョン推論プロファイル経由で呼び出すため、**呼び出し元のリージョンが属する地域に応じてプレフィックスを変える** 必要があります。

| `AWS_REGION` 例 | `BEDROCK_CHAT_MODEL_ID` |
|---|---|
| `us-east-1`, `us-west-2`(US) | `us.amazon.nova-lite-v1:0` |
| `ap-northeast-1`(東京), `ap-southeast-1` 等(APAC) | `apac.amazon.nova-lite-v1:0` |
| `eu-central-1`, `eu-west-1` 等(EU) | `eu.amazon.nova-lite-v1:0` |

> プレフィックスが合っていないと `ValidationException: The provided model identifier is invalid` が発生します。

## 5. 疎通確認

`01_basics/basics.ipynb` を開き、最初のセル(`Hello Bedrock`)を実行。

応答テキストが返ってきたらセットアップ完了です。

---

## トラブルシュート

| 症状 | 原因 / 対処 |
|---|---|
| `AccessDeniedException` | IAMで `bedrock:InvokeModel` が許可されていない、またはAnthropic製モデル利用時に使用フォーム未提出 |
| `Could not connect to the endpoint URL` | `AWS_REGION` の設定誤り、またはリージョンでモデル未提供 |
| `Unable to locate credentials` | ホストで `aws sso login` していない、または `AWS_PROFILE` 名が違う |
| `ValidationException: ... on-demand throughput isn't supported` | クロスリージョン推論プロファイル付きモデルID(`us.` / `apac.` / `eu.` プレフィックス)を使う必要あり |
| `ValidationException: The provided model identifier is invalid` | `BEDROCK_CHAT_MODEL_ID` のプレフィックスと `AWS_REGION` の地域が不一致(上の対応表を確認) |

---

次へ → [01_basics/](../01_basics/)
