# MCP Demo Server

A demonstration MCP (Model Context Protocol) server showcasing **Tools**, **Resources**, and **Prompts** with integrated security scanning.

## Features

### 🛠️ Tools (6)
- `add` - Add two numbers
- `reverse_text` - Reverse a string
- `format_json` - Pretty-print JSON
- `calculate` - Evaluate mathematical expressions
- `scan_mcp_server` - Scan MCP servers for vulnerabilities
- `check_scanner_status` - Check scanner configuration

### 📚 Resources (4)
- `demo://info` - Server metadata
- `demo://timestamp` - Current time and uptime
- `demo://examples` - Usage examples
- `demo://file/data` - Read sample data

### 💬 Prompts (3)
- `code_review` - Code review template
- `summarize` - Text summarization template
- `debug_helper` - Debugging assistance template

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/manutri1986/mcpdeployment.git
cd mcpdeployment

# Install dependencies (automatic with uv)
uv sync
```

### Run the Server

**Local Development (stdio transport):**
```bash
# Start MCP server for IDE integration
uv run mcp-server
```

The server communicates via stdio and will wait for MCP protocol connections.

**Remote Deployment (HTTP transport):**
```bash
# Start HTTP server for remote access
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote

# Or use the test script
./scripts/test_http_local.sh
```

📖 Full HTTP deployment guide: [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md)

## Security Scanning

### Quick Scan

```bash
# Run security scan (YARA analyzer - fast, no API key needed)
uv run python scripts/scanners/yara_scanner.py

# Quick scan (sample components only)
uv run python scripts/scanners/yara_scanner.py --quick

# Advanced scanners (require API keys)
uv run python scripts/scanners/llm_api_scanner.py       # OpenAI LLM analysis
uv run python scripts/scanners/cisco_api_scanner.py     # Cisco AI Defense
```

**Scanner Coverage:**
- ✅ Tools (6) - All scanned
- ✅ Prompts (3) - All scanned
- ⚠️ Resources (4) - Cannot scan via stdio

### Setup Advanced Scanning (Optional)

For deeper analysis with LLM and API analyzers:

```bash
# Run setup script
./scripts/setup_scanner.sh

# Or set environment variables manually
export MCP_SCANNER_API_KEY="your_api_key"
export MCP_SCANNER_ENDPOINT="https://us.api.inspect.aidefense.security.cisco.com/api/v1"
```

Get your API key: [Cisco AI Defense](https://aidefense.security.cisco.com/)

📖 Full documentation: [docs/SCANNER_SETUP.md](docs/SCANNER_SETUP.md)

## Using with MCP Clients

### Cursor IDE

Configuration included at `.cursor/mcp.json`. After setup:

1. Restart Cursor IDE
2. Test: "Use the add tool to calculate 5 + 3"
3. Or: "Access the demo://info resource"

### Claude Desktop, VS Code, Windsurf

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "mcpdeployment": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/manutri1986/mcpdeployment.git",
        "mcp-server"
      ]
    }
  }
}
```

**Configuration file locations:**

| Client | Config Path |
|--------|-------------|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global) |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| VS Code | `.vscode/mcp.json` or User settings |
| Claude Code | `.claude/mcp.json` (project) or `~/.claude/mcp.json` (global) |

## Project Structure

```
mcpdeployment/
├── src/mcpserver/          # MCP server implementation
│   ├── __init__.py
│   ├── __main__.py         # Entry point (stdio transport)
│   ├── __main_remote__.py  # Entry point (HTTP transport)
│   └── server.py           # Tools, resources, prompts
├── scripts/                # Utility scripts
│   ├── scanners/          # Security scanner implementations
│   │   ├── yara_scanner.py
│   │   ├── llm_api_scanner.py
│   │   └── cisco_api_scanner.py
│   ├── setup_scanner.sh   # Scanner configuration
│   └── test_http_local.sh # Local HTTP testing
├── tests/                  # Test files
│   └── test_scanner.py    # Test scanner setup
├── reports/                # Generated scan reports (gitignored)
├── docs/                   # Documentation
│   ├── methodology/       # Scanner methodology docs
│   ├── SCANNER_SETUP.md
│   ├── SCANNER_LIMITATIONS.md
│   └── HTTP_DEPLOYMENT.md # Remote deployment guide
├── data/                   # Sample data
│   └── sample_data.json
├── STRUCTURE.md           # Detailed structure guide
├── CLAUDE.md              # AI assistant guidance
├── README.md              # This file
└── pyproject.toml         # Project configuration
```

📖 See [STRUCTURE.md](STRUCTURE.md) for detailed directory structure and purpose.

## Architecture

Built with [FastMCP](https://github.com/jlowin/fastmcp), a Python framework for MCP servers.

**Key Pattern:**
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Demo")

@mcp.tool()
def your_tool(arg: type) -> type:
    """Tool description"""
    return result

@mcp.resource("uri://path")
def your_resource() -> str:
    """Resource description"""
    return json.dumps(data)

@mcp.prompt()
def your_prompt(arg: type) -> str:
    """Prompt description"""
    return f"Prompt text with {arg}"
```

See [CLAUDE.md](CLAUDE.md) for detailed architecture notes.

## Development

### Test Scanner

```bash
# Verify scanner is configured
uv run python tests/test_scanner.py
```

### Adding Components

Edit `src/mcpserver/server.py`:

1. Add function with appropriate decorator (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`)
2. Update scanner scripts in `scripts/scanners/` to include new tools/prompts in scan lists
3. Run security scan: `uv run python scripts/scanners/yara_scanner.py`

## Documentation

- [CLAUDE.md](CLAUDE.md) - Development guide for AI assistants
- [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md) - Remote HTTP deployment guide
- [docs/SCANNER_SETUP.md](docs/SCANNER_SETUP.md) - Scanner configuration
- [docs/SCANNER_LIMITATIONS.md](docs/SCANNER_LIMITATIONS.md) - What can/cannot be scanned

## Troubleshooting

### Server won't start
- Check Python version: `uv run python --version` (needs 3.11+)
- Reinstall dependencies: `uv sync`

### Tools not appearing in client
- Restart client completely
- Check client logs for errors
- Verify configuration file syntax

### Scanner errors
- Verify installation: `uv pip list | grep cisco-ai-mcp-scanner`
- Test setup: `uv run python tests/test_scanner.py`

## License

MIT
