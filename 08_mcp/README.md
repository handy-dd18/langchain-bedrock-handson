# 08 MCP 連携(所要時間: 60〜90分)

## このステップのゴール
- **MCP (Model Context Protocol)** の位置づけと基本構成を理解する
- LangGraph エージェントに、MCP サーバ提供のツールを取り込む最小構成を作る
- **自作 MCP サーバ** と **公式 filesystem MCP サーバ** の 2 つを同時に接続する

## 事前準備

- [05章 LangGraph + LangSmith](../05_langgraph/README.md) を実施済みであること
- DevContainer に **Node.js** がインストール済みであること(`devcontainer.json` の features で自動セットアップ)
- 動作確認:
  ```bash
  node --version    # v18 以上
  npx --version
  python --version  # 3.11 以上
  ```

## やること

[mcp_intro.ipynb](mcp_intro.ipynb) を上から順に実行。

### 含まれる内容

1. **MCP とは** - Anthropic 発の標準。Server / Client / Transport の関係
2. **自作 MCP サーバ** - `mcp_servers/math_server.py` の中身確認
3. **MultiServerMCPClient で接続** - stdio 経由で math サーバを起動 → ツール取得
4. **LangGraph に統合** - `create_agent` に MCP ツールを渡す
5. **公式 filesystem MCP** - `@modelcontextprotocol/server-filesystem` を `npx` 経由で起動
6. **複数サーバ同時利用** - math と filesystem 両方のツールをエージェントが使い分ける

## ディレクトリ構成

```
08_mcp/
├── README.md
├── mcp_intro.ipynb
├── mcp_servers/
│   └── math_server.py        ← 自作 MCP サーバ(Python FastMCP)
└── data/                     ← filesystem MCP サーバが公開するディレクトリ
    ├── note1.txt
    └── note2.txt
```

## Done条件

- 自作 math サーバ経由でエージェントが `add` / `multiply` を呼び出して計算できる
- filesystem サーバ経由でエージェントが `data/` 配下のファイルを一覧・読み出しできる
- LangSmith のトレースで MCP ツール呼び出しが可視化される

## トラブルシュート

| 症状 | 対処 |
|---|---|
| `npx: command not found` | DevContainer の Node.js feature が入っていない。`Dev Containers: Rebuild Container` で再ビルド |
| `Connection closed` などの stdio エラー | サーバ側スクリプトが起動失敗。`python mcp_servers/math_server.py` をターミナルで単独実行してエラー確認 |
| filesystem MCP がパーミッションで失敗 | 公式 filesystem サーバは「許可されたディレクトリ外」へのアクセスを拒否する。Notebook では `08_mcp/data/` だけを公開 |

---

← [07 マルチエージェント](../07_multi_agent/README.md) | 次へ → [09 総まとめ](../09_wrapup/README.md)
