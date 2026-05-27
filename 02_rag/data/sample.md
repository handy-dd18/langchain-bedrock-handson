# LangChain と関連技術メモ

## LangChain とは
LangChain は大規模言語モデル(LLM)を使ったアプリケーションを構築するためのフレームワークです。
プロンプト管理、モデル抽象化、外部データ接続、エージェント機構、ベクトル検索との統合など、
LLMアプリでよく必要になる要素を共通インタフェースで提供します。
Python 版と JavaScript/TypeScript 版があります。

## LCEL (LangChain Expression Language)
LCEL は LangChain のコンポーネントを `|`(パイプ)演算子で繋いで宣言的にチェーンを構築する記法です。
組み立てたチェーンは Runnable インタフェースを実装しており、
`invoke` / `batch` / `stream` / `ainvoke` を統一的に利用できます。
これにより同期/非同期、ストリーミングの切替がコードをほぼ変えずに行えます。

## RAG (Retrieval Augmented Generation)
RAG は外部の知識ベースから関連情報を検索して、その内容をプロンプトに組み込んで LLM に回答させる手法です。
モデルの学習データに含まれない最新情報や、社内文書のような独自情報を扱う際に有効です。
典型的な構成は「文書ロード → 分割 → 埋め込み → ベクトル DB に保存 → 質問時に類似検索 → 結果をプロンプトに注入 → 生成」です。

## エージェント
LangChain におけるエージェントとは、LLM 自身に「次にどのツール(関数)を呼ぶか」を判断させる仕組みです。
ユーザーからの問いに対し、計算が必要なら計算ツール、検索が必要なら検索ツール、というように
LLM が動的にツールを選択し、その結果を踏まえて最終回答を生成します。
Tool Calling 対応モデル(Claude 3 系、Amazon Nova 系など)と相性が良いです。

## Bedrock 連携
LangChain で Amazon Bedrock を使う場合は `langchain-aws` パッケージを利用します。
チャットモデルは `ChatBedrockConverse`、埋め込みは `BedrockEmbeddings` を使うのが標準的です。
認証は通常の AWS SDK と同じで、環境変数や `~/.aws/` の設定が利用されます。
