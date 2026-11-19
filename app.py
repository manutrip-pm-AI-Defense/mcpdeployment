"""ASGI application wrapper for Azure App Service deployment."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcpserver.server import mcp

app = mcp.streamable_http_app(host="0.0.0.0")

if __name__ == "__main__":
    host = os.getenv("MCP_REMOTE_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_REMOTE_PORT", "8000"))
    print(f"Starting MCP Server on {host}:{port}")
    mcp.run(transport="streamable-http", host=host, port=port)
