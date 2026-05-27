# 02 RAG 最小構成(所要時間: 約30分)

## このステップのゴール
- RAG (Retrieval Augmented Generation) の処理フローを理解する
- 文書をベクトル化してChromaに保存できる
- 質問に対し、文書から検索した内容を根拠に回答できる

## RAGの全体像

```
[文書ファイル]
      ↓ Load
[Document]
      ↓ Split
[小さなチャンク]
      ↓ Embed (Bedrock Titan Embeddings)
[ベクトル]
      ↓ Store (Chroma)
[ベクトルDB]  ←── 質問もEmbed → 類似検索 → 関連チャンク取得
                                            ↓
                                       [プロンプトに注入]
                                            ↓
                                       [LLM (Bedrock)]
                                            ↓
                                         回答
```

## やること

[rag.ipynb](rag.ipynb) を上から順に実行。

サンプル文書: [data/sample.md](data/sample.md)

## Done条件

サンプル文書の内容に関する質問(例: 「LangChainのLCELとは?」)に対し、文書を根拠にした回答が返る。

---

← [01 基礎](../01_basics/) | 次へ → [03 エージェント](../03_agent/)
