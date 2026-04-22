# MCP Deployment Server

## Installation

This server can be used with any MCP-compatible host (Claude Desktop, Cursor, Windsurf, VS Code, etc.).

Add the following to your MCP host's configuration file:

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

### Configuration file locations by host

| Host | Configuration File |
|------|--------------------|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global) |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| VS Code (Copilot) | `.vscode/mcp.json` (project) or User `settings.json` |
| Claude Code (CLI) | `.claude/mcp.json` (project) or `~/.claude/mcp.json` (global) |

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) must be installed (`uvx` is bundled with it)
