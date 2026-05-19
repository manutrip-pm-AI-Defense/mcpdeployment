#!/bin/bash
# ============================================================================
# Local HTTP Server Testing Script
# ============================================================================
# This script starts the MCP server in HTTP mode for local testing
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}MCP Server - Local HTTP Testing${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Configuration
export MCP_REMOTE_HOST="${MCP_REMOTE_HOST:-127.0.0.1}"
export MCP_REMOTE_PORT="${MCP_REMOTE_PORT:-8000}"

echo -e "${GREEN}Configuration:${NC}"
echo "  Host: $MCP_REMOTE_HOST"
echo "  Port: $MCP_REMOTE_PORT"
echo "  Endpoint: http://$MCP_REMOTE_HOST:$MCP_REMOTE_PORT"
echo ""

# Check if port is already in use
if lsof -Pi :$MCP_REMOTE_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Warning: Port $MCP_REMOTE_PORT is already in use${NC}"
    echo "  You may need to:"
    echo "  1. Stop the existing service"
    echo "  2. Use a different port: MCP_REMOTE_PORT=9000 $0"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}Starting MCP server...${NC}"
echo ""
echo -e "${YELLOW}Testing instructions:${NC}"
echo "  1. Server will start and display startup information"
echo "  2. In another terminal, test the endpoint:"
echo "     curl http://$MCP_REMOTE_HOST:$MCP_REMOTE_PORT"
echo ""
echo "  3. Or use an MCP client to connect to:"
echo "     http://$MCP_REMOTE_HOST:$MCP_REMOTE_PORT"
echo ""
echo "  4. Press Ctrl+C to stop the server"
echo ""
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Start the server
uv run mcp-server-remote
