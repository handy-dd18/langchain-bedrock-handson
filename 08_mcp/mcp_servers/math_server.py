"""ハンズオン用の最小 MCP サーバ実装(stdio transport)。

FastMCP を使うと、関数を @mcp.tool() でデコレートするだけで MCP ツールとして公開できる。
LangChain や Claude Desktop など、MCP に対応したクライアントから呼び出せる。
"""
from mcp.server.fastmcp import FastMCP

# サーバの名前("math")はクライアントがツールを識別する際の prefix に使われる
mcp = FastMCP("math")


@mcp.tool()
def add(a: float, b: float) -> float:
    """2 つの数値を加算した結果を返す。"""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """2 つの数値を乗算した結果を返す。"""
    return a * b


if __name__ == "__main__":
    # stdio で起動。クライアントはこのプロセスを subprocess として起動し、
    # 標準入出力で JSON-RPC メッセージをやり取りする。
    mcp.run(transport="stdio")
