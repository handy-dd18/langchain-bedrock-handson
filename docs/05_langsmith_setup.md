# LangSmith セットアップガイド

第5章以降のハンズオンで LangChain / LangGraph の実行トレースを **LangSmith** に送って可視化します。
無料枠で十分まかなえるので、05章を始める前に以下の手順を実施してください。

> 💡 **LangSmith API キーは必須ではありません。** 未設定でもNotebook自体は動きます。ただし「トレースを見る」体験はできません。

## 1. アカウントを作成

1. https://smith.langchain.com/ にアクセス
2. Google/GitHub アカウント、またはメールでサインアップ
3. ログイン後、初回プロジェクトが自動作成される

## 2. API キーを発行

1. 左下のアバター → **Settings**
2. 左メニュー **API keys** → **Create API Key**
3. 説明欄に任意の名前(例: `langchain-bedrock-handson`)を入力して作成
4. 表示された `lsv2_pt_xxxx...` のキーをコピー(**再表示できないので注意**)

## 3. `.env` に書き込む

リポジトリルートの `.env` を編集します。

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGSMITH_PROJECT=langchain-bedrock-handson
```

- `LANGSMITH_TRACING=true` を設定すると、Notebook 内で LangChain / LangGraph を実行するたびに自動でトレースが LangSmith に送信されます。
- `LANGSMITH_PROJECT` は LangSmith ダッシュボード上での束ね名。何でもOK(既存に同名があれば自動的にそこに集約)。

## 4. 動作確認

第5章の Notebook(`05_langgraph/langgraph_langsmith.ipynb`)の最初の方のセルを実行し、Bedrock 呼び出しが完了したら、LangSmith ダッシュボードを開きます。

1. LangSmith 左メニュー **Tracing Projects** → `langchain-bedrock-handson`
2. 直近のトレースがリストに現れる
3. クリックすると、入力プロンプト・LLMの出力・ツール呼び出しなど全ステップが見られる

## トラブルシュート

| 症状 | 対処 |
|---|---|
| トレースがプロジェクトに現れない | `.env` を編集後に Notebookカーネルを再起動。`load_dotenv()` は1度しか効かないため、編集前のキャッシュが残る |
| `LANGSMITH_API_KEY` がエラー | キー先頭が `lsv2_pt_` か確認。コピー時に余計な空白が入っていないか確認 |
| EU でホスティングしたい | `.env` に `LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com` を追加 |
| トレース送信を一時的に止めたい | `LANGSMITH_TRACING=false` にする(キーは残してOK) |
| 無料枠を使い切るのが心配 | 個人での学習用途であれば、無料の Developer プランで十分(月数千トレースまで) |

---

[← 戻る (00 セットアップ)](00_setup.md) | [05章へ進む →](../05_langgraph/README.md)
