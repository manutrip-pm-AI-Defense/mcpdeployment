# Quick Start

## 🚀 Run the Server

**Local (stdio for IDEs):**
```bash
uv run mcp-server
```

**Remote (HTTP for cloud deployment):**
```bash
# Test locally
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote

# Or use test script
./scripts/test_http_local.sh
```

See [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md) for full deployment guide.

## 🔍 Security Scan

```bash
# Full scan
uv run python scripts/scan.py

# Quick scan
uv run python scripts/scan.py --quick
```

## 📁 Where is Everything?

| What | Where |
|------|-------|
| **MCP Server** | `src/mcpserver/server.py` |
| **Entry Point (stdio)** | `src/mcpserver/__main__.py` |
| **Entry Point (HTTP)** | `src/mcpserver/__main_remote__.py` |
| **Scanner** | `scripts/scanners/` |
| **Setup Scanner** | `scripts/setup_scanner.sh` |
| **HTTP Test Script** | `scripts/test_http_local.sh` |
| **Documentation** | `docs/` |

## 🛠️ Common Tasks

### Add a New Tool
Edit `src/mcpserver/server.py`:
```python
@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"
```

Then add to `scripts/scan.py` scan list.

### Add a New Resource
Edit `src/mcpserver/server.py`:
```python
@mcp.resource("demo://my-resource")
def my_resource() -> str:
    """Resource description"""
    return json.dumps({"data": "value"})
```

### Add a New Prompt
Edit `src/mcpserver/server.py`:
```python
@mcp.prompt()
def my_prompt(text: str) -> str:
    """Prompt description"""
    return f"Analyze this: {text}"
```

## 📚 Documentation

- [README.md](README.md) - Full documentation
- [CLAUDE.md](CLAUDE.md) - Development guide
- [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md) - HTTP deployment
- [docs/SCANNER_SETUP.md](docs/SCANNER_SETUP.md) - Scanner config
- [docs/SCANNER_LIMITATIONS.md](docs/SCANNER_LIMITATIONS.md) - Limitations

## 🧪 Test

```bash
# Test scanner setup
uv run python tests/test_scanner.py

# Verify server starts
uv run mcp-server
```

## 🎯 That's It!

Your MCP server code is in `src/mcpserver/server.py` - that's the only file you need to edit for adding tools, resources, and prompts.
