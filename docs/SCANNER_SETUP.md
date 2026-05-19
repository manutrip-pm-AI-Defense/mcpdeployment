# Cisco AI MCP Scanner Setup Guide

This guide will help you integrate the Cisco AI MCP Scanner into your MCP server for security analysis and vulnerability scanning.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Getting Your API Key](#getting-your-api-key)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Overview

The Cisco AI MCP Scanner provides two types of security scanning:

1. **Basic Scan**: Local security analysis without requiring an API key
2. **Deep Scan**: Comprehensive API-based analysis (requires Cisco AI Defense API key)

## Prerequisites

- Python 3.11 or higher
- `cisco-ai-mcp-scanner` package (already installed via `uv add cisco-ai-mcp-scanner`)
- Cisco AI Defense account (for deep scanning)

## Getting Your API Key

### Step 1: Create a Cisco AI Defense Account

1. Visit [Cisco AI Defense](https://aidefense.security.cisco.com/)
2. Click **Sign Up** or **Log In** if you already have an account
3. Complete the registration process

### Step 2: Generate an API Key

1. Once logged in, navigate to your **Account Settings** or **API Management**
2. Look for the **API Keys** or **Credentials** section
3. Click **Create API Key** or **Generate New Key**
4. Give it a descriptive name (e.g., "MCP Scanner - Development")
5. **Important**: Copy the API key immediately - you may not be able to see it again!

### Step 3: Note Your Endpoint Region

Select the appropriate endpoint based on your region:

- **US** (default): `https://us.api.inspect.aidefense.security.cisco.com/api/v1`
- **EU**: `https://eu.api.inspect.aidefense.security.cisco.com/api/v1`
- **Other regions**: Check the [Getting Started Guide](https://developer.cisco.com/docs/ai-defense/getting-started)

## Configuration

### Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
cd /Users/manutripathi/Documents/Projects/mcpdeployment
./scripts/setup_scanner.sh
```

The script will:
- Create a `.env` file from the template
- Prompt you for your API key and endpoint
- Configure the environment variables
- Provide next steps

### Option 2: Manual Setup

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file**:
   ```bash
   nano .env
   ```

3. **Set your credentials**:
   ```env
   MCP_SCANNER_API_KEY=your_actual_api_key_here
   MCP_SCANNER_ENDPOINT=https://us.api.inspect.aidefense.security.cisco.com/api/v1
   ```

4. **Load the environment variables**:
   ```bash
   source .env
   # Or export them directly:
   export MCP_SCANNER_API_KEY="your_actual_api_key_here"
   export MCP_SCANNER_ENDPOINT="https://us.api.inspect.aidefense.security.cisco.com/api/v1"
   ```

### Option 3: System-Wide Configuration

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Cisco AI MCP Scanner Configuration
export MCP_SCANNER_API_KEY="your_actual_api_key_here"
export MCP_SCANNER_ENDPOINT="https://us.api.inspect.aidefense.security.cisco.com/api/v1"
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Usage

### Starting the MCP Server

```bash
# Make sure environment variables are loaded
source .env  # if using .env file

# Start the server
uv run mcp-server
```

### Available Tools

The server now includes two scanner-related tools:

#### 1. `check_scanner_status`

Check if the scanner is properly configured:

```python
# Returns status information including:
# - Whether scanner is installed
# - Scanner version
# - API key configuration status
# - Available capabilities
# - Setup instructions
```

#### 2. `scan_mcp_server`

Scan an MCP server for vulnerabilities:

```python
# Basic scan (no API key required)
scan_mcp_server(
    server_url="http://localhost:8000",
    scan_type="basic"
)

# Deep scan (requires API key)
scan_mcp_server(
    server_url="http://localhost:8000",
    scan_type="deep"
)
```

### Example: Using the Scanner via MCP Client

If you're connecting to this server from Claude Desktop or another MCP client:

1. **Check scanner status**:
   - Call the `check_scanner_status` tool
   - Verify that `api_key_configured: true` (for deep scans)

2. **Run a basic scan**:
   ```
   Use the scan_mcp_server tool with:
   - server_url: "http://localhost:8000"
   - scan_type: "basic"
   ```

3. **Run a deep scan**:
   ```
   Use the scan_mcp_server tool with:
   - server_url: "http://localhost:8000"
   - scan_type: "deep"
   ```

## Testing

### Test 1: Verify Installation

```bash
python -c "from mcp_scanner import MCPScanner; print('Scanner installed successfully!')"
```

### Test 2: Check Environment Variables

```bash
echo "API Key: ${MCP_SCANNER_API_KEY:0:10}..."  # Shows first 10 chars
echo "Endpoint: $MCP_SCANNER_ENDPOINT"
```

### Test 3: Test Scanner Programmatically

```python
from mcp_scanner import MCPScanner
import os

api_key = os.getenv("MCP_SCANNER_API_KEY")
endpoint = os.getenv("MCP_SCANNER_ENDPOINT")

print(f"API Key configured: {bool(api_key)}")
print(f"Endpoint: {endpoint}")

# Try initializing scanner
scanner = MCPScanner(api_key=api_key, endpoint=endpoint)
print("Scanner initialized successfully!")
```

### Test 4: Test via MCP Server

```bash
# Start the server
uv run mcp-server

# In another terminal or via MCP client, call check_scanner_status tool
```

## Troubleshooting

### Issue: "API key not configured" error

**Solution**:
```bash
# Verify environment variable is set
echo $MCP_SCANNER_API_KEY

# If empty, set it:
export MCP_SCANNER_API_KEY="your_api_key"

# Or load from .env file:
source .env
```

### Issue: "cisco-ai-mcp-scanner package not installed"

**Solution**:
```bash
uv add cisco-ai-mcp-scanner
```

### Issue: "Invalid API key" or authentication errors

**Solutions**:
1. Verify your API key is correct (copy-paste from Cisco AI Defense portal)
2. Check that your API key hasn't expired
3. Ensure you're using the correct endpoint for your region
4. Try regenerating a new API key

### Issue: Connection timeout or endpoint errors

**Solutions**:
1. Check your internet connection
2. Verify the endpoint URL is correct for your region
3. Check if there are any firewall restrictions
4. Try the alternate endpoint (US vs EU)

### Issue: Environment variables not persisting

**Solution**:
Add them to your shell profile for permanent configuration:
```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export MCP_SCANNER_API_KEY="your_key"' >> ~/.zshrc
echo 'export MCP_SCANNER_ENDPOINT="your_endpoint"' >> ~/.zshrc
source ~/.zshrc
```

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never commit your `.env` file** - It's already in `.gitignore`
2. **Keep your API key secret** - Don't share it or include it in code
3. **Rotate keys regularly** - Generate new keys periodically
4. **Use environment variables** - Don't hardcode credentials
5. **Limit key permissions** - Use the minimum required permissions

## Additional Resources

- **Cisco AI Defense Portal**: https://aidefense.security.cisco.com/
- **Developer Documentation**: https://developer.cisco.com/docs/ai-defense/
- **Getting Started Guide**: https://developer.cisco.com/docs/ai-defense/getting-started
- **API Documentation**: https://developer.cisco.com/docs/ai-defense/api/

## Support

For issues with:
- **The scanner itself**: Contact Cisco AI Defense support
- **This MCP server integration**: Create an issue in this repository
- **MCP protocol**: Visit the [MCP documentation](https://modelcontextprotocol.io/)

## What's Next?

After setting up the scanner:

1. ✅ Test the scanner with your MCP server
2. ✅ Integrate scanning into your development workflow
3. ✅ Set up automated scans for CI/CD pipelines
4. ✅ Review scan results and fix vulnerabilities
5. ✅ Monitor scanner status and API usage

Happy scanning! 🔒
