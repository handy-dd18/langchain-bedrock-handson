# 06 RAG 深掘り(所要時間: 90〜120分)

## このステップのゴール
- 第2章の素朴な top-k 検索の限界を体感する
- 検索精度を上げる3つの手法 — **MultiQuery / Ensemble / Rerank** — を試す
- 複数 Loader(Markdown, PDF)から統合インデックスを構築できる
- RAG を **LangGraph でノード化** し、LangSmith でトレースする
- LangSmith の `evaluate` で **RAG の精度を数値化** する

## 事前準備

- [05章 LangGraph + LangSmith](../05_langgraph/README.md) を先に完了させてください(本章で LangGraph と LangSmith を活用します)
- DevContainer が `requirements.txt` 最新版で再ビルド済みであること

## やること

[rag_advanced.ipynb](rag_advanced.ipynb) を上から順に実行。

### 含まれる内容

1. **複数 Loader でインデックス構築** - Markdown + PDF を統合
2. **素朴な top-k 検索のベースライン** - 02章と同じ方式
3. **手法1: MultiQueryRetriever** - LLM に質問を言い換えさせて検索漏れを減らす
4. **手法2: EnsembleRetriever** - 密ベクトル + BM25 のハイブリッド検索
5. **手法3: Reranker** - Bedrock Rerank で上位N件を並び替え
6. **LangGraph で RAG を再構築** - `retrieve_node` → `generate_node`
7. **LangSmith で評価** - データセットを作って各手法のスコアを比較

## サンプル文書

`data/` に2つの Markdown と、Notebook 内で動的生成する1つの PDF を使用します:

- `data/company_handbook.md` — 架空の会社の社内ハンドブック(勤務時間、リモートワーク、経費等)
- `data/product_faq.md` — 製品のFAQ(SmartLogger Pro)
- `data/generated_sample.pdf` — Notebook 実行時に `reportlab` で自動生成される技術文書

## Done条件

- 同じ質問に対し、ベースラインより改善版 Retriever の方が関連チャンクを上位に返すケースが確認できる
- LangSmith にトレース・評価結果が記録される(API キーを設定している場合)

## トラブルシュート

| 症状 | 対処 |
|---|---|
| Bedrock Rerank のセルで `AccessDeniedException` | リージョンによっては Rerank モデル未提供。`.env` の `BEDROCK_RERANK_MODEL_ID` を確認、もしくはセルをスキップ |
| 同セルで `ValidationException: The provided model identifier is invalid` | Rerank のリージョン別IDが Nova Lite と異なる場合あり。`amazon.rerank-v1:0` をそのまま試し、ダメなら該当セクションをスキップして次に進む |
| LangSmith に評価結果が出ない | `.env` の `LANGSMITH_API_KEY` 未設定。詳細は [LangSmithセットアップガイド](../docs/05_langsmith_setup.md) |

---

← [05 LangGraph + LangSmith](../05_langgraph/README.md) | 次へ → [07 マルチエージェント](../07_multi_agent/README.md)
