# HTTP Deployment Guide

This guide explains how to deploy the MCP server with HTTP transport for remote access.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Local Testing](#local-testing)
- [Remote Deployment](#remote-deployment)
- [Client Connection](#client-connection)
- [Platform-Specific Guides](#platform-specific-guides)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Overview

### Transport Modes

The MCP server supports two transport modes:

| Transport | Command | Use Case | Deployment |
|-----------|---------|----------|------------|
| **stdio** | `mcp-server` | Local IDE integration (Cursor, Claude Desktop, VS Code) | Local only |
| **HTTP** | `mcp-server-remote` | Remote deployment, web clients, cloud platforms | Local + Remote |

### When to Use HTTP Transport

Use HTTP transport (`mcp-server-remote`) when you need:

- ✅ Remote access from cloud platforms (MCP JAM, Glama.ai, Railway, Render)
- ✅ Web-based MCP clients
- ✅ Resource scanning with the Cisco AI MCP Scanner
- ✅ Multiple clients connecting to the same server
- ✅ RESTful API access to MCP capabilities

Continue using stdio transport (`mcp-server`) for:

- ✅ Local development with IDEs (Cursor, Claude Desktop)
- ✅ Direct process communication
- ✅ Simpler local setup

## Quick Start

### 1. Install the Package

```bash
# From the project directory
cd /path/to/mcpdeployment
uv sync
```

### 2. Start HTTP Server (Localhost)

```bash
# Test locally first
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote
```

### 3. Verify Server is Running

In another terminal:

```bash
# Check if server responds
curl http://127.0.0.1:8000
```

### 4. Connect with MCP Client

Configure your MCP client to connect to:
```
http://127.0.0.1:8000
```

## Configuration

### Environment Variables

The HTTP server is configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_REMOTE_HOST` | `0.0.0.0` | Server binding address |
| `MCP_REMOTE_PORT` | `8000` | Server port |
| `MCP_SCANNER_API_KEY` | _(none)_ | Cisco AI Defense API key (optional) |
| `MCP_SCANNER_ENDPOINT` | US endpoint | Cisco API endpoint (optional) |
| `MCP_SCANNER_LLM_API_KEY` | _(none)_ | OpenAI API key (optional) |

### Host Binding Options

- **`127.0.0.1`** - Localhost only (local testing)
- **`0.0.0.0`** - All network interfaces (remote access)
- **Specific IP** - Bind to specific network interface

### Using .env.remote File

Create a configuration file:

```bash
# Copy template
cp .env.remote.example .env.remote

# Edit configuration
nano .env.remote
```

Set values:

```bash
MCP_REMOTE_HOST=0.0.0.0
MCP_REMOTE_PORT=8000
MCP_SCANNER_API_KEY=your_api_key_here
```

Load and run:

```bash
# Load environment variables
set -a
source .env.remote
set +a

# Start server
uv run mcp-server-remote
```

## Local Testing

### Using the Test Script

```bash
# Run with defaults (127.0.0.1:8000)
./scripts/test_http_local.sh

# Custom port
MCP_REMOTE_PORT=9000 ./scripts/test_http_local.sh
```

### Manual Testing

**Terminal 1 - Start Server:**
```bash
MCP_REMOTE_HOST=127.0.0.1 MCP_REMOTE_PORT=8000 uv run mcp-server-remote
```

**Terminal 2 - Test Connection:**
```bash
# Basic connectivity
curl http://127.0.0.1:8000

# Test with MCP client (example with httpx)
python -c "
import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000')
        print(f'Status: {response.status_code}')
        print(f'Response: {response.text[:200]}')

asyncio.run(test())
"
```

### Verify Server Capabilities

The server should expose:
- **6 Tools**: `add`, `reverse_text`, `format_json`, `calculate`, `scan_mcp_server`, `check_scanner_status`
- **4 Resources**: `demo://info`, `demo://timestamp`, `demo://examples`, `demo://file/data`
- **3 Prompts**: `code_review`, `summarize`, `debug_helper`

## Remote Deployment

### Prerequisites

- Python 3.11+
- `uv` package manager (or `pip`)
- Network connectivity
- Open port (default: 8000)

### Generic Cloud Deployment Steps

1. **Prepare Environment:**
   ```bash
   git clone https://github.com/manutri1986/mcpdeployment.git
   cd mcpdeployment
   ```

2. **Install Dependencies:**
   ```bash
   uv sync
   # OR with pip:
   # pip install -e .
   ```

3. **Configure Environment:**
   ```bash
   export MCP_REMOTE_HOST=0.0.0.0
   export MCP_REMOTE_PORT=8000
   export MCP_SCANNER_API_KEY=your_key_here
   ```

4. **Start Server:**
   ```bash
   uv run mcp-server-remote
   ```

5. **Configure Firewall:**
   - Allow inbound connections on port 8000
   - Restrict by IP if possible

### Keep Server Running

Use a process manager to keep the server running:

**Option 1: systemd (Linux)**
```bash
# Create service file: /etc/systemd/system/mcp-server.service
[Unit]
Description=MCP Server (HTTP)
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/mcpdeployment
Environment="MCP_REMOTE_HOST=0.0.0.0"
Environment="MCP_REMOTE_PORT=8000"
ExecStart=/usr/local/bin/uv run mcp-server-remote
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

**Option 2: tmux/screen (Quick Testing)**
```bash
tmux new -s mcp-server
uv run mcp-server-remote
# Detach: Ctrl+B, D
```

**Option 3: nohup (Simple Background)**
```bash
nohup uv run mcp-server-remote > mcp-server.log 2>&1 &
```

## Client Connection

### MCP Client Configuration

Configure your MCP client to connect via HTTP:

**Example: Python MCP Client**
```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client("http://your-server:8000") as (read, write):
    async with ClientSession(read, write) as session:
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")
```

**Example: JavaScript/TypeScript Client**
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const transport = new SSEClientTransport(
  new URL("http://your-server:8000")
);

const client = new Client({
  name: "my-mcp-client",
  version: "1.0.0",
}, {
  capabilities: {}
});

await client.connect(transport);
```

### Testing with curl

```bash
# List capabilities (example - actual MCP protocol may differ)
curl -X POST http://your-server:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list", "params": {}}'
```

## Platform-Specific Guides

### MCP JAM

_Coming soon - MCP JAM deployment guide_

### Glama.ai

_Coming soon - Glama.ai deployment guide_

### Railway

1. **Create Railway Project:**
   ```bash
   railway init
   ```

2. **Configure Start Command:**
   ```bash
   railway run uv run mcp-server-remote
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set MCP_REMOTE_HOST=0.0.0.0
   railway variables set MCP_REMOTE_PORT=8000
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

### Render

1. **Create Web Service** from GitHub repo
2. **Build Command:** `pip install -e .`
3. **Start Command:** `mcp-server-remote`
4. **Environment Variables:**
   - `MCP_REMOTE_HOST=0.0.0.0`
   - `MCP_REMOTE_PORT=8000`

### Fly.io

1. **Create fly.toml:**
   ```toml
   app = "mcp-server"
   
   [build]
     builder = "paketobuildpacks/builder:base"
   
   [env]
     MCP_REMOTE_HOST = "0.0.0.0"
     MCP_REMOTE_PORT = "8000"
   
   [[services]]
     internal_port = 8000
     protocol = "tcp"
   
     [[services.ports]]
       port = 80
       handlers = ["http"]
   
     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

2. **Deploy:**
   ```bash
   fly deploy
   ```

## Security Considerations

### Current State: Development Only

The current implementation has **NO authentication** and is intended for:
- ✅ Local testing (127.0.0.1)
- ✅ Trusted private networks
- ❌ **NOT for public internet exposure**

### Future Security Enhancements

Before deploying to production, implement:

1. **Authentication:**
   - API key validation
   - OAuth 2.0 integration
   - JWT tokens

2. **HTTPS/TLS:**
   - Use reverse proxy (nginx, caddy)
   - Platform-provided SSL certificates
   - Let's Encrypt certificates

3. **Network Security:**
   - Firewall rules
   - IP whitelisting
   - Private networks/VPNs
   - Rate limiting

4. **Monitoring:**
   - Access logs
   - Error tracking
   - Performance monitoring
   - Alerting

### Reverse Proxy Setup (nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name mcp.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For Server-Sent Events
        proxy_buffering off;
        proxy_cache off;
    }
}
```

## Troubleshooting

### Server Won't Start

**Problem:** Port already in use
```bash
Error: Address already in use
```

**Solution:**
```bash
# Check what's using the port
lsof -i :8000

# Use different port
MCP_REMOTE_PORT=9000 uv run mcp-server-remote
```

---

**Problem:** Permission denied binding to port
```bash
Error: Permission denied (port < 1024)
```

**Solution:**
```bash
# Use port >= 1024, or run with sudo (not recommended)
MCP_REMOTE_PORT=8000 uv run mcp-server-remote
```

### Can't Connect from Remote Client

**Problem:** Connection refused from remote machine

**Check:**
1. **Firewall:** Port 8000 open?
   ```bash
   # Linux (ufw)
   sudo ufw allow 8000
   
   # macOS
   # System Preferences → Security → Firewall → Options
   ```

2. **Binding:** Using 0.0.0.0 not 127.0.0.1?
   ```bash
   MCP_REMOTE_HOST=0.0.0.0 uv run mcp-server-remote
   ```

3. **Network:** Can you reach the machine?
   ```bash
   ping your-server-ip
   ```

### Scanner Tools Not Working

**Problem:** `scan_mcp_server` returns errors

**Check:**
1. **API Keys Set:**
   ```bash
   echo $MCP_SCANNER_API_KEY
   ```

2. **Network Access:** Can reach Cisco API endpoint?
   ```bash
   curl https://us.api.inspect.aidefense.security.cisco.com/api/v1
   ```

3. **Try YARA analyzer first** (no API key needed):
   ```bash
   # Via MCP client
   scan_mcp_server("http://target", analyzers="yara")
   ```

### Resource Not Found Errors

**Problem:** Resources not accessible via HTTP

This is expected in current implementation. Resources are defined but may need proper HTTP routing configuration for external access via certain MCP clients.

### High Memory Usage

**Problem:** Server consumes lots of memory

**Solutions:**
- Restart server periodically
- Monitor with `htop` or similar
- Consider container resource limits
- Review scanner tool usage (large scans can consume memory)

## Next Steps

After successful HTTP deployment:

1. **Add authentication** - Secure your server
2. **Enable HTTPS** - Encrypt traffic
3. **Set up monitoring** - Track usage and errors
4. **Create health checks** - Monitor uptime
5. **Document platform deployments** - Share your experience

## Support

For issues or questions:
- GitHub Issues: [mcpdeployment/issues](https://github.com/manutri1986/mcpdeployment/issues)
- Documentation: See `README.md` and `CLAUDE.md`
- MCP Protocol: [Model Context Protocol](https://modelcontextprotocol.io/)

## Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Cisco AI MCP Scanner](https://github.com/cisco/cisco-ai-mcp-scanner)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
