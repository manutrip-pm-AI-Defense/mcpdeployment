# MCP Scanner Limitations and Workarounds

## Overview

The Cisco AI MCP Scanner can analyze different MCP server components with varying levels of support depending on the server type (stdio vs HTTP).

## What Can Be Scanned

### ✅ Fully Supported (Stdio Servers)

#### 1. **Tools** - Executable Functions
- **Scanner Support:** ✅ Full support via `scan_stdio_server_tool()`
- **Your Server:** 6 tools
  - `add`, `reverse_text`, `format_json`, `calculate`, `scan_mcp_server`, `check_scanner_status`
- **Security Risk:** HIGH - Tools execute code and can have vulnerabilities
- **Scan Command:** `uv run python scripts/detailed_scan.py`

#### 2. **Prompts** - Prompt Templates
- **Scanner Support:** ✅ Full support via `scan_stdio_server_prompt()`
- **Your Server:** 3 prompts
  - `code_review`, `summarize`, `debug_helper`
- **Security Risk:** MEDIUM - Prompts generate content but don't execute code
- **Scan Command:** `uv run python scripts/detailed_scan.py`

### ⚠️ Limited Support (Stdio Servers)

#### 3. **Resources** - Read-Only Data
- **Scanner Support:** ❌ Not supported for stdio servers
- **Your Server:** 4 resources
  - `demo://info` - Server metadata and capabilities
  - `demo://timestamp` - Current time and uptime
  - `demo://examples` - Usage examples
  - `demo://file/data` - Reads sample_data.json
- **Security Risk:** LOW - Resources provide structured data, not executable code
- **Reason:** Package limitation - `scan_stdio_server_resources()` doesn't exist

## Why Resources Can't Be Scanned (Stdio)

### Technical Explanation

The `cisco-ai-mcp-scanner` package provides different APIs for stdio and HTTP servers:

**Stdio Server Methods (Your Current Setup):**
```python
scanner.scan_stdio_server_tool()      # ✅ Exists
scanner.scan_stdio_server_tools()     # ✅ Exists
scanner.scan_stdio_server_prompt()    # ✅ Exists
scanner.scan_stdio_server_prompts()   # ✅ Exists
scanner.scan_stdio_server_resources() # ❌ Does NOT exist
```

**HTTP/Remote Server Methods:**
```python
scanner.scan_remote_server_tool()      # ✅ Exists
scanner.scan_remote_server_tools()     # ✅ Exists
scanner.scan_remote_server_prompt()    # ✅ Exists
scanner.scan_remote_server_prompts()   # ✅ Exists
scanner.scan_remote_server_resource()  # ✅ Exists
scanner.scan_remote_server_resources() # ✅ Exists
```

### Why This Limitation Exists

1. **Protocol Differences:** Stdio uses process communication, HTTP uses REST APIs
2. **Resource Streaming:** MCP resources can be streaming data sources
3. **Package Design:** The scanner was primarily designed for HTTP endpoints
4. **Current Version:** This is a known limitation in version 4.6.0

## Risk Assessment: Resources

### Why Resources Are Lower Risk

Your MCP server's resources contain **structured data**, not executable code:

1. **demo://info**
   - Type: JSON metadata
   - Content: Server capabilities, version info
   - Risk: Minimal - static configuration data

2. **demo://timestamp**
   - Type: JSON timestamp
   - Content: Current time, uptime calculation
   - Risk: Minimal - time data, no user input

3. **demo://examples**
   - Type: JSON documentation
   - Content: Usage examples and descriptions
   - Risk: Minimal - static documentation

4. **demo://file/data**
   - Type: JSON file reader
   - Content: Reads from `data/sample_data.json`
   - Risk: **Low-Medium** - File system access
   - Note: Most risky resource, but path is hardcoded

### Security Considerations

✅ **Safe Aspects:**
- No code execution
- No dynamic content generation
- No user input processing (in resource URIs)
- Mostly static/read-only data

⚠️ **Potential Concerns:**
- `demo://file/data` accesses file system
- If file paths were dynamic (they're not), path traversal risk
- If data contained sensitive info (currently demo data)

## Workarounds

### Option 1: Accept the Limitation (Recommended)

**Rationale:**
- Resources are lower risk than tools/prompts
- Your resources contain safe, structured data
- Manual security review is straightforward

**Manual Review Checklist:**
```bash
# Review resource implementations
grep -n "@mcp.resource" src/mcpserver/server.py

# Check for:
# - Hardcoded paths (good)
# - No user input in file paths (good)
# - Error handling for missing files (good)
# - No sensitive data exposure (verify)
```

### Option 2: Convert to HTTP Server

**To enable resource scanning:**

1. **Modify server to use HTTP mode:**
   ```python
   # In src/mcpserver/server.py
   # Change from stdio to HTTP
   if __name__ == "__main__":
       mcp.run(transport="sse")  # Use SSE transport
   ```

2. **Deploy as HTTP endpoint:**
   ```bash
   # Start server on HTTP
   uv run mcp-server --transport sse --port 8000
   ```

3. **Scan with remote API:**
   ```python
   scanner.scan_remote_server_resources(
       server_url="http://localhost:8000",
       analyzers=[AnalyzerEnum.YARA]
   )
   ```

**Trade-offs:**
- ✅ Can scan resources
- ❌ More complex deployment
- ❌ Need to manage HTTP server
- ❌ Different client configuration

### Option 3: Wait for Package Update

Monitor the `cisco-ai-mcp-scanner` package for updates:

```bash
# Check for new versions
uv pip list --outdated | grep cisco-ai-mcp-scanner

# Update when available
uv add cisco-ai-mcp-scanner --upgrade
```

**Check release notes for:**
- stdio resource scanning support
- New `scan_stdio_server_resources()` method

## Current Scan Coverage

Your MCP server components:

| Component Type | Count | Scannable | Risk Level | Status |
|----------------|-------|-----------|------------|--------|
| Tools | 6 | ✅ Yes | HIGH | ✅ Scanned |
| Prompts | 3 | ✅ Yes | MEDIUM | ✅ Scanned |
| Resources | 4 | ❌ No | LOW | Manual review |
| **Total** | **13** | **9/13 (69%)** | - | **9 scanned** |

## Recommendations

### Immediate Actions

1. ✅ **Continue using current scanner** for tools and prompts
2. ✅ **Manually review resources** (straightforward given their simplicity)
3. ✅ **Document the limitation** (this file)

### Manual Resource Security Review

For each resource, verify:

**demo://info:**
```python
# ✅ Safe - Returns static server metadata
# ✅ No user input
# ✅ No sensitive data
```

**demo://timestamp:**
```python
# ✅ Safe - Returns current time/uptime
# ✅ No user input
# ✅ No sensitive data
```

**demo://examples:**
```python
# ✅ Safe - Returns static documentation
# ✅ No user input
# ✅ No sensitive data
```

**demo://file/data:**
```python
# ⚠️ Review - File system access
# ✅ Path is hardcoded (project_root + "data/sample_data.json")
# ✅ Has error handling for missing files
# ✅ Returns JSON (not executing code)
# ⚠️ Verify: data/sample_data.json contains no secrets
```

### Long-term Strategy

1. **Monitor package updates** for stdio resource scanning
2. **Consider HTTP deployment** if resource scanning becomes critical
3. **Include resource review** in code review process
4. **Document resource security** in CLAUDE.md or similar

## Summary

**Current State:**
- 9/13 components (69%) can be automatically scanned
- All HIGH and MEDIUM risk components (tools, prompts) are scanned
- LOW risk components (resources) require manual review

**Recommendation:**
- ✅ Accept the limitation
- ✅ Manual review is sufficient for current resources
- ✅ Continue automated scanning for tools and prompts
- 📋 Document this as known limitation

**Bottom Line:**
Your security coverage is comprehensive where it matters most. Resources present minimal risk and are straightforward to review manually.

## Questions?

- **Package Documentation:** https://developer.cisco.com/docs/ai-defense/
- **Feature Requests:** Contact Cisco AI Defense support
- **MCP Protocol:** https://modelcontextprotocol.io/
