# 01 LangChain 基礎(所要時間: 約20分)

## このステップのゴール
- LangChain経由でBedrockのLLMを呼び出せる
- PromptTemplateで入力を整形できる
- LCEL(`prompt | model | parser`)でチェーンを組める

## やること

[basics.ipynb](basics.ipynb) を開き、上から順にセルを実行してください。

含まれる内容:

1. **Hello Bedrock** - `ChatBedrockConverse` で最小呼び出し
2. **PromptTemplate** - System/Userメッセージのテンプレ化
3. **LCEL チェーン** - `prompt | llm | StrOutputParser`
4. **ストリーミング** - 応答をトークン単位で受け取る

## Done条件

最後のセルでストリーミング応答が文字単位で表示されればOK。

---

← [00 セットアップ](../docs/00_setup.md) | 次へ → [02 RAG](../02_rag/)
