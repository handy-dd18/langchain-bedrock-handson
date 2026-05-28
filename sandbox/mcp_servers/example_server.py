"""sandbox 用の自作 MCP サーバ(stdio transport)。

08章の math_server をベースにした実験用テンプレート。
@mcp.tool() で関数を増やせば、そのまま MCP ツールとして使える。

使い方(Notebook 側):
    from langchain_mcp_adapters.client import MultiServerMCPClient
    client = MultiServerMCPClient({
        "sandbox": {
            "command": "python",
            "args": ["mcp_servers/example_server.py"],
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sandbox")


@mcp.tool()
def add(a: float, b: float) -> float:
    """2つの数値を加算した結果を返す。"""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """2つの数値を乗算した結果を返す。"""
    return a * b


@mcp.tool()
def echo(text: str) -> str:
    """渡された文字列をそのまま返す(動作確認用)。"""
    return text


# ここに @mcp.tool() を付けた関数を追加すれば、ツールを増やせる
# 例:
# @mcp.tool()
# def word_count(text: str) -> int:
#     """文字列の単語数を返す。"""
#     return len(text.split())


if __name__ == "__main__":
    mcp.run(transport="stdio")
