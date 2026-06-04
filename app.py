"""
ASGI application wrapper for Azure App Service deployment
This file creates an ASGI app that can be served by Gunicorn + Uvicorn
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcpserver.server import mcp

# Configure for remote deployment with streamable-http transport
host = os.getenv("MCP_REMOTE_HOST", "0.0.0.0")
port = int(os.getenv("MCP_REMOTE_PORT", "8000"))

mcp.settings.host = host
mcp.settings.port = port

# FastMCP instance IS the ASGI app - no need for get_asgi_app()
# The mcp object from server.py is already configured with all tools/resources/prompts
app = mcp

if __name__ == "__main__":
    # For local testing - use streamable-http transport
    import uvicorn
    print(f"Starting MCP Server on {host}:{port} with streamable-http transport")
    mcp.run(transport="streamable-http")
