# 05 LangGraph + LangSmith(所要時間: 90〜120分)

## このステップのゴール
- **LangGraph** で「状態を持つエージェント」を組み立てられる
- prebuilt の `create_react_agent` と、手書きの `StateGraph` の両方を体験
- **LangSmith** にトレースを送り、エージェント内部の動きを可視化できる

## 事前準備

1. [LangSmithセットアップガイド](../docs/05_langsmith_setup.md) を実施し、`.env` に `LANGSMITH_API_KEY` を設定
   - 未設定でも Notebook は動きます(トレース確認だけスキップ)
2. リポジトリルートでパッケージを更新(DevContainer再ビルド済みなら不要):
   ```bash
   pip install -r requirements.txt
   ```

## やること

[langgraph_langsmith.ipynb](langgraph_langsmith.ipynb) を上から順に実行。

含まれる内容:
1. **準備とトレース有効化** - LangSmith 環境変数の確認
2. **prebuilt エージェント** - `create_react_agent` で 1 行 Agent
3. **LangSmith でトレース確認** - ダッシュボード閲覧
4. **手書き StateGraph** - ノード/エッジを自分で書く
5. **グラフの可視化** - `print_ascii()` / Mermaid 出力
6. **会話履歴(MemorySaver)** - 複数ターン会話

## Done条件

- prebuilt / 手書きのどちらでもツール呼び出しを伴う応答が返る
- LangSmith ダッシュボードに自分の実行がツリー形式で表示される
- MemorySaver で「私の名前を覚えて」が次のターンで参照される

---

← [04 中間まとめ](../04_wrapup/README.md) | 次へ → [06 RAG深掘り](../06_rag_advanced/README.md)
