# 07 マルチエージェント(所要時間: 60〜90分)

## このステップのゴール
- 役割の異なる **2 つのエージェント** を協調させる最小構成を体験する
- **Supervisor パターン**(中央集権型)の動作原理を理解する
- LangSmith のトレースで「誰がいつ何をしたか」を可視化できる

## 事前準備

- [06章 RAG深掘り](../06_rag_advanced/README.md) を実施済みであること
  - 本章で **Researcher エージェントが 06章のベクトルDB(`06_rag_advanced/.chroma_v2`)を検索ツールとして使います**
  - 06章の Notebook を一度通しで実行し、`.chroma_v2/` が生成された状態にしておいてください

## やること

[multi_agent.ipynb](multi_agent.ipynb) を上から順に実行。

### 含まれる内容

1. **マルチエージェントの動機** - 単独エージェントとの違い、Supervisor / Swarm の比較
2. **Researcher エージェント** - 06章の Retriever をツール化、`create_agent` で構築
3. **Writer エージェント** - ツールなし、集めた情報を文章にまとめる
4. **Supervisor 構築** - `create_supervisor` で 2 エージェントをオーケストレーション
5. **実行** - `.invoke()` と `.stream()` で動作観察
6. **LangSmith トレース確認** - エージェント間の hand-off が可視化されるはず

## サンプル課題

> 「LCEL について、社内文書を踏まえて初心者向けに 300 字で説明して」

このような複合タスクで:
1. Supervisor がまず **Researcher** に「文書から情報を集めて」と依頼
2. Researcher が `retrieve_company_docs` ツールを使って関連チャンクを取得
3. Supervisor が **Writer** に「集めた情報を 300 字にまとめて」と依頼
4. Writer がまとまった文章を生成
5. Supervisor が最終回答としてユーザーに返す

## Done条件

- 単発の質問で Researcher → Writer の順にエージェントが呼ばれ、最終文章が返る
- `stream` で各ステップ(どのエージェントが今喋っているか)が観察できる
- LangSmith に supervisor → researcher → ツール → supervisor → writer → 終了 のツリーが現れる

---

← [06 RAG深掘り](../06_rag_advanced/README.md) | 次へ → [08 MCP連携](../08_mcp/README.md)
