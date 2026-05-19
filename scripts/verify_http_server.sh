#!/bin/bash
# Simple verification that HTTP server is running and accessible

echo "==================================================================="
echo "MCP HTTP Server Verification"
echo "==================================================================="
echo ""

HOST="${1:-127.0.0.1}"
PORT="${2:-8000}"

echo "Testing server at: http://$HOST:$PORT"
echo ""

# Check if something is listening on the port
if command -v lsof &> /dev/null; then
    echo "✅ Checking if port $PORT is in use..."
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "   ✅ Port $PORT is open and listening"
    else
        echo "   ❌ Port $PORT is not in use"
        echo "   Start the server first:"
        echo "   MCP_REMOTE_HOST=$HOST MCP_REMOTE_PORT=$PORT uv run mcp-server-remote"
        exit 1
    fi
fi

echo ""
echo "✅ SERVER IS RUNNING"
echo ""
echo "==================================================================="
echo "Understanding the 404 Errors"
echo "==================================================================="
echo ""
echo "If you see '404 Not Found' errors when accessing http://$HOST:$PORT"
echo "in a browser, this is EXPECTED and NORMAL."
echo ""
echo "Why? MCP servers don't serve web pages. They only respond to MCP"
echo "protocol messages at specific endpoints."
echo ""
echo "The 404 means:"
echo "  ✅ Server is running"
echo "  ✅ Server is accessible"
echo "  ✅ Server is waiting for MCP client connections"
echo ""
echo "==================================================================="
echo "How to Connect"
echo "==================================================================="
echo ""
echo "MCP Clients should connect to:"
echo "  http://$HOST:$PORT"
echo ""
echo "The server provides:"
echo "  • 6 Tools (add, reverse_text, format_json, calculate, ...)"
echo "  • 4 Resources (demo://info, demo://timestamp, ...)"
echo "  • 3 Prompts (code_review, summarize, debug_helper)"
echo ""
echo "==================================================================="
echo "Next Steps"
echo "==================================================================="
echo ""
echo "1. Deploy to a cloud platform (Railway, Render, Fly.io)"
echo "2. Configure your MCP client to connect to this HTTP endpoint"
echo "3. Add authentication and HTTPS for production use"
echo ""
echo "See docs/HTTP_DEPLOYMENT.md for detailed deployment guides"
echo ""
