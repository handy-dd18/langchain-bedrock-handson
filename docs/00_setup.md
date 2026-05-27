# 00 セットアップ(所要時間: 約15分)

## このステップのゴール
- DevContainer が起動でき、Notebookが実行可能
- AWS Bedrock に Notebook から接続できる

## 1. AWS Bedrock モデルアクセスを有効化

AWSコンソールで以下のモデルへのアクセスを **事前に申請** してください(リージョン: 例 `us-east-1`)。

- `Amazon Nova Lite`(チャット用)
- `Amazon Titan Text Embeddings V2`(埋め込み用)

手順:
1. AWSコンソール → Amazon Bedrock → 左メニュー「Model access」
2. 「Modify model access」から上記モデルを選択し、リクエスト
3. ステータスが「Access granted」になっていることを確認

> Amazon純正モデルは通常すぐに承認されます。

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
- `AWS_REGION` = モデルアクセスを有効化したリージョン(例 `us-east-1`)

## 5. 疎通確認

`01_basics/basics.ipynb` を開き、最初のセル(`Hello Bedrock`)を実行。

応答テキストが返ってきたらセットアップ完了です。

---

## トラブルシュート

| 症状 | 原因 / 対処 |
|---|---|
| `AccessDeniedException` | モデルアクセスが未承認。手順1を再確認 |
| `Could not connect to the endpoint URL` | `AWS_REGION` の設定誤り、またはリージョンでモデル未提供 |
| `Unable to locate credentials` | ホストで `aws sso login` していない、または `AWS_PROFILE` 名が違う |
| `ValidationException: ... on-demand throughput isn't supported` | `us.` 等のクロスリージョン推論プロファイル付きモデルIDを使う必要あり(本教材のデフォルトは `us.amazon.nova-lite-v1:0`) |

---

次へ → [01_basics/](../01_basics/)
