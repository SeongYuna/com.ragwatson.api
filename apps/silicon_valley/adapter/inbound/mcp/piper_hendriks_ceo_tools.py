from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperHendricksCeo")


@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 CEO 헨드릭스입니다"