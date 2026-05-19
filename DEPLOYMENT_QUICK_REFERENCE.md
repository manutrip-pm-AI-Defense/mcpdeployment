# Deployment Quick Reference

Quick commands for deploying and testing your MCP server.

## Local Development (stdio)

```bash
# Start server for IDE integration
uv run mcp-server
```

Use with: Cursor, Claude Desktop, VS Code MCP plugins

## Local Testing (HTTP)

```bash
# Test HTTP server on localhost
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote

# Or use the test script
./scripts/test_http_local.sh

# Run automated tests
uv run python tests/test_http_server.py
```

## Remote Deployment (HTTP)

```bash
# Deploy to cloud/remote server
MCP_REMOTE_HOST=0.0.0.0 MCP_REMOTE_PORT=8000 uv run mcp-server-remote
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_REMOTE_HOST` | `0.0.0.0` | Server binding address |
| `MCP_REMOTE_PORT` | `8000` | Server port |

### Using .env.remote

```bash
# Create config file
cp .env.remote.example .env.remote

# Edit configuration
nano .env.remote

# Load and run
set -a; source .env.remote; set +a
uv run mcp-server-remote
```

## Verification Checklist

- [ ] stdio server works: `uv run mcp-server`
- [ ] HTTP server starts: `MCP_REMOTE_HOST=127.0.0.1 uv run mcp-server-remote`
- [ ] Tests pass: `uv run python tests/test_http_server.py`
- [ ] Both commands exist: `which mcp-server && which mcp-server-remote`

## Server Capabilities

Both transport modes expose:
- **6 Tools**: add, reverse_text, format_json, calculate, scan_mcp_server, check_scanner_status
- **4 Resources**: demo://info, demo://timestamp, demo://examples, demo://file/data
- **3 Prompts**: code_review, summarize, debug_helper

## Documentation

- **Full Guide**: [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md)
- **Architecture**: [CLAUDE.md](CLAUDE.md)
- **Overview**: [README.md](README.md)

## Troubleshooting

**Port already in use?**
```bash
# Use different port
MCP_REMOTE_PORT=9000 uv run mcp-server-remote
```

**Can't connect remotely?**
```bash
# Check firewall and use 0.0.0.0
MCP_REMOTE_HOST=0.0.0.0 uv run mcp-server-remote
```

**Need to keep server running?**
```bash
# Use tmux/screen or systemd
tmux new -s mcp-server
uv run mcp-server-remote
# Detach: Ctrl+B, D
```

## Next Steps

1. ✅ Test locally with HTTP client
2. ✅ Deploy to cloud platform
3. 🔜 Add authentication
4. 🔜 Enable HTTPS
5. 🔜 Set up monitoring
