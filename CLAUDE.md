# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) demonstration server that showcases how to build servers exposing **Tools**, **Resources**, and **Prompts** to AI assistants. It also integrates the Cisco AI MCP Scanner for security vulnerability analysis.

**Key Architecture Decision**: Built with [FastMCP](https://github.com/jlowin/fastmcp), a Python framework that simplifies MCP server development through decorators.

## Development Setup

### Prerequisites
- Python 3.11+ (required for Cisco AI MCP Scanner)
- `uv` package manager

### Running the Server

**Local Development (stdio):**
```bash
# Start MCP server (stdio mode for IDEs)
uv run mcp-server

# Alternative: Run as module
uv run python -m mcpserver
```

**Remote Deployment (HTTP):**
```bash
# Start HTTP server for remote access
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote

# Or use test script
./scripts/test_http_local.sh
```

The server supports two transport modes:
- **stdio** (default) - For local IDE integration (Cursor, Claude Desktop)
- **HTTP** (streamable-http) - For remote deployment to cloud platforms

See [docs/HTTP_DEPLOYMENT.md](docs/HTTP_DEPLOYMENT.md) for full HTTP deployment guide.

### Security Scanner

```bash
# Run security scan (YARA - fast, no API key)
uv run python scripts/scanners/yara_scanner.py

# Quick scan (sample components)
uv run python scripts/scanners/yara_scanner.py --quick

# Advanced scanners (require API keys)
uv run python scripts/scanners/llm_api_scanner.py       # OpenAI LLM
uv run python scripts/scanners/cisco_api_scanner.py     # Cisco AI Defense

# Test scanner configuration
uv run python tests/test_scanner.py
```

**Scanner Coverage:**
- ✅ Tools (6) - Fully scanned
- ✅ Prompts (3) - Fully scanned
- ⚠️ Resources (4) - Cannot scan via stdio (package limitation)

**Optional**: Set `MCP_SCANNER_API_KEY` and `MCP_SCANNER_ENDPOINT` environment variables for advanced analyzers (LLM, API). YARA analyzer works without API keys.

### Testing in MCP Clients

**Cursor IDE**: Configuration at `.cursor/mcp.json` uses absolute paths. Must use `["run", "--", "python", "-m", "mcpserver"]` format, not the `mcp-server` script. Restart Cursor completely after config changes.

**Claude Desktop/Others**: See README.md for host-specific config file locations.

## Architecture

### Core Structure

```
src/mcpserver/
├── __init__.py
├── __main__.py         # Entry point (stdio): imports mcp from server.py and calls mcp.run()
├── __main_remote__.py  # Entry point (HTTP): imports mcp and calls mcp.run(transport="streamable-http")
└── server.py           # Main implementation: defines all tools, resources, prompts
```

### FastMCP Pattern

The server is defined as a single `FastMCP` instance in `server.py`:

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Demo")

# Tools - Callable functions
@mcp.tool()
def function_name(args) -> return_type:
    """Docstring becomes tool description"""
    return result

# Resources - Read-only data endpoints
@mcp.resource("uri://path")
def resource_name() -> str:
    """Returns string data (typically JSON)"""
    return json.dumps(data)

# Prompts - Template generators
@mcp.prompt()
def prompt_name(args) -> str:
    """Returns formatted prompt string"""
    return f"Prompt text with {args}"
```

**Critical**: All three component types are defined in `server.py`. The `mcp` instance is imported by:
- `__main__.py` (stdio transport) - calls `mcp.run()` 
- `__main_remote__.py` (HTTP transport) - modifies settings and calls `mcp.run(transport="streamable-http")`

Both entry points use the same server instance, ensuring all tools/resources/prompts are available in both modes.

### Component Categories

**Tools** (6 total):
- Demo tools: `add`, `reverse_text`, `format_json`, `calculate`
- Scanner tools: `scan_mcp_server`, `check_scanner_status`

**Resources** (4 total):
- `demo://info` - Server capabilities
- `demo://timestamp` - Time/uptime
- `demo://examples` - Usage docs
- `demo://file/data` - Reads `data/sample_data.json`

**Prompts** (3 total):
- `code_review` - Code review template
- `summarize` - Summarization template
- `debug_helper` - Debugging template

### Scanner Integration

The `scan_mcp_server` and `check_scanner_status` tools wrap the `cisco-ai-mcp-scanner` package (imported as `mcpscanner`). 

**Key Implementation Details:**
- Scanner supports stdio servers via `Scanner.scan_stdio_server_tool()` and `Scanner.scan_stdio_server_prompt()`
- NO `scan_stdio_server_resource()` method exists - resources require HTTP endpoints
- **HTTP transport enables resource scanning** via `scan_remote_server_resources()` method
- Scanner config loads from environment: `MCP_SCANNER_API_KEY`, `MCP_SCANNER_ENDPOINT`
- YARA analyzer works without API keys; LLM/API analyzers require keys

**Scanner Scripts:**
- `scripts/scanners/yara_scanner.py` - YARA pattern-based scanning (no API key)
- `scripts/scanners/llm_api_scanner.py` - OpenAI LLM-powered analysis
- `scripts/scanners/cisco_api_scanner.py` - Cisco AI Defense cloud analysis
- All support `--quick` flag for sample scans
- Uses async/await pattern: `await scanner.scan_stdio_server_tool()`
- Results use `ToolScanResult` and `PromptScanResult` with fields: `tool_name`/`prompt_name`, `tool_description`/`prompt_description`, `status`, `analyzers`, `findings`

## Adding New Components

### New Tool

Add to `server.py`:
```python
@mcp.tool()
def your_tool(param: type) -> return_type:
    """Clear description for AI"""
    # Implementation
    return result
```

### New Resource

Add to `server.py`:
```python
@mcp.resource("demo://your-resource")
def your_resource() -> str:
    """Description"""
    data = {"key": "value"}
    return json.dumps(data, indent=2)
```

Resources should return JSON strings for consistency.

### New Prompt

Add to `server.py`:
```python
@mcp.prompt()
def your_prompt(param: type) -> str:
    """Description"""
    return f"""Formatted prompt text
    with {param}"""
```

**Important**: After adding tools/prompts, update scanner scripts to include them in the scan lists.

## Security Scanner Details

### Scanning New Components

When adding tools or prompts, update scanner scripts in `scripts/scanners/`:
- Add to `tools_to_scan` or `prompts_to_scan` lists in each scanner file
- Update both full scan mode and quick scan mode sections
- All three scanners (yara_scanner.py, llm_api_scanner.py, cisco_api_scanner.py) should be updated

### Scanner Result Structure

```python
# Tools and Prompts share similar result structure
result = await scanner.scan_stdio_server_tool(...)
# result.tool_name / result.prompt_name
# result.tool_description / result.prompt_description
# result.status  # "completed", "failed"
# result.analyzers  # ["yara"]
# result.findings  # List[SecurityFinding]
```

Mark results with `result.component_type = "tool"` or `"prompt"` before adding to `all_results` for proper JSON report generation.

### Why Resources Aren't Scanned

The `mcpscanner` package does NOT provide `scan_stdio_server_resource()` or `scan_stdio_server_resources()`. Resource scanning only available via `scan_remote_server_resources()` for HTTP endpoints. This is a known package limitation, not a bug.

Resources present minimal security risk (structured data, not executable code). See `docs/SCANNER_LIMITATIONS.md` for detailed explanation.

## Deployment Considerations

### Package Installation

Users install via:
```bash
uvx --from git+https://github.com/manutri1986/mcpdeployment.git mcp-server
```

This requires:
- `pyproject.toml` defines `[project.scripts]` entry: `mcp-server = "mcpserver.__main__:main"`
- `setuptools` build backend configured
- Package finds code via `package-dir = {"" = "src"}`

### MCP Protocol Transport

Server defaults to stdio transport (process communication). To use HTTP/SSE:
```python
# In __main__.py or when calling mcp.run()
mcp.run(transport="sse")
```

Stdio is preferred for local development and simple deployments. HTTP required for resource scanning.

## Common Issues

### "No module named mcpserver"
- Check `PYTHONPATH` or run from project root
- Verify `src/mcpserver/__init__.py` exists
- Use `uv run` to ensure correct environment

### Scanner Import Errors
- Package name is `mcpscanner` not `mcp_scanner` or `cisco_ai_mcp_scanner`
- Import: `from mcpscanner import Scanner, Config, AnalyzerEnum`
- Scanner methods are async: must use `await`

### Cursor Not Loading Server
- Must restart Cursor completely (Cmd+Q/Ctrl+Q and reopen)
- Config requires absolute paths: `which uv` for command path
- Use module invocation: `["run", "--", "python", "-m", "mcpserver"]`
- Check Cursor logs: View → Output → "MCP" dropdown

## Documentation Structure

- `README.md` - User-facing overview and quick start
- `CLAUDE.md` - Development guide (this file)
- `docs/SCANNER_SETUP.md` - Detailed scanner configuration
- `docs/SCANNER_LIMITATIONS.md` - Technical explanation of what can/cannot be scanned

When updating scanner functionality, keep these docs synchronized.
