from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperDineshDash")


@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 개발자 디네시입니다"
