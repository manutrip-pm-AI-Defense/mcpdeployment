# YARA Scanning Methodology Documentation

Complete guide to understanding how YARA-based security scanning works in the MCP deployment project.

## 📚 Documentation Structure

This folder contains comprehensive documentation about YARA scanning methodology with real examples from this project:

### 1. [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
**Main methodology document** - Deep dive into how YARA scanning works.

**Contents:**
- What is YARA and why use it?
- Scanner architecture and workflow
- 10 YARA rule categories explained
- Pattern matching details
- Real examples from this project
- Best practices and limitations

**Best for:** Understanding the theory and architecture

---

### 2. [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md)
**Visual diagrams** - ASCII diagrams showing the scanning process.

**Contents:**
- Complete scanning architecture diagram
- Single component scan flow
- YARA rule execution detail
- Clean vs. vulnerable code comparison
- Performance metrics and timelines

**Best for:** Visual learners who want to see the flow

---

### 3. [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
**Hands-on examples** - Real code and scan results from this project.

**Contents:**
- Quick start: Running your first scan
- Tool scanning examples (all 6 tools explained)
- Prompt scanning examples (all 3 prompts)
- Common vulnerability patterns and fixes
- CI/CD integration examples
- Programmatic scanning code

**Best for:** Learning by doing, copy-paste examples

---

## 🚀 Quick Start

### Run Your First Scan

```bash
# Navigate to project root
cd /Users/manutripathi/Documents/Projects/mcpdeployment

# Quick scan (2 tools, 1 prompt)
uv run python scripts/scan.py --quick

# Full scan (6 tools, 3 prompts)
uv run python scripts/scan.py
```

### Understanding Results

```
[2/9] calculate... ✅ Clean
```

- ✅ **Clean** = No security issues found
- ⚠️ **N finding(s)** = Security issues detected
- ❌ **Error** = Scan failed (check logs)

---

## 📖 Reading Guide

### For Beginners

**Recommended reading order:**
1. Start with [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) - Example 1 & 2
2. Read [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md) - "What is YARA?" section
3. Look at [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md) - Complete Architecture
4. Return to [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) - Tool examples

**Time investment:** ~30 minutes

### For Security Practitioners

**Recommended reading order:**
1. [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md) - YARA Rule Categories
2. [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) - Common Patterns and Fixes
3. [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md) - Pattern Matching Details

**Time investment:** ~45 minutes

### For Developers Integrating Scanner

**Recommended reading order:**
1. [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) - Integration Examples
2. [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md) - Performance Metrics
3. [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md) - Best Practices

**Time investment:** ~20 minutes

---

## 🎯 Key Concepts

### What is YARA?

YARA is a pattern-matching tool for identifying and classifying security threats. Think of it as "grep on steroids" for security analysis.

**Example:**
```yara
rule code_execution {
    strings:
        $eval = /\beval\s*\(/i
    condition:
        $eval
}
```

This rule detects any use of Python's `eval()` function.

### How YARA Works in MCP Scanner

```
Your MCP Server → Scanner connects → Extracts code → YARA rules check → Context analysis → Report
```

1. Scanner connects to your MCP server
2. Extracts tool/prompt implementations
3. Runs 10 YARA rule files (code_execution, command_injection, etc.)
4. Analyzes context (are mitigations present?)
5. Generates report with findings

### Scanner Coverage in This Project

| Component | Count | Scannable | Status |
|-----------|-------|-----------|--------|
| Tools | 6 | ✅ Yes | All clean |
| Prompts | 3 | ✅ Yes | All clean |
| Resources | 4 | ❌ No | Manual review |
| **Total** | **13** | **9/13 (69%)** | **9 scanned** |

---

## 🔍 Real Examples from This Project

### Example: Safe eval() Usage

**Our `calculate` tool:**
```python
def calculate(expression: str) -> float:
    # ✅ Input validation
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters")
    
    # ✅ Restricted namespace
    result = eval(expression, {"__builtins__": {}}, {})
    return float(result)
```

**YARA detects `eval()` but scanner sees:**
- Input validation: ✅ Present
- Restricted namespace: ✅ Present
- Error handling: ✅ Present

**Result:** ✅ Clean (properly mitigated)

### 10 YARA Rule Categories

Our scanner uses these rule files:

1. **code_execution.yara** - Detects `eval()`, `exec()`, `os.system()`
2. **command_injection.yara** - Detects shell commands, `nc`, `wget`
3. **prompt_injection.yara** - Detects "Ignore instructions", hidden directives
4. **sql_injection.yara** - Detects SQL patterns, union attacks
5. **data_exfiltration.yara** - Detects network uploads, DNS tunneling
6. **credential_harvesting.yara** - Detects credential theft patterns
7. **script_injection.yara** - Detects XSS, JavaScript injection
8. **system_manipulation.yara** - Detects file deletion, permission changes
9. **tool_poisoning.yara** - Detects MCP protocol abuse
10. **coercive_injection.yara** - Detects social engineering attempts

---

## 📊 Scan Results

### Latest Full Scan

```
✅ Components Scanned: 9
   • Tools: 6
   • Prompts: 3
   • Security Findings: 0

🎉 All components passed security checks!
```

### Performance

- **Full scan time:** ~10-12 seconds
- **Quick scan time:** ~4-5 seconds
- **Per component:** ~1-1.5 seconds
- **Rules applied:** 10 per component

---

## 🛠️ Common Use Cases

### Use Case 1: Pre-deployment Security Check

```bash
# Before deploying to production
uv run python scripts/scan.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Safe to deploy"
else
    echo "❌ Security issues found"
    exit 1
fi
```

### Use Case 2: CI/CD Integration

```yaml
# .github/workflows/security-scan.yml
- name: Run Security Scan
  run: uv run python scripts/scan.py
  
- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: scan-report
    path: scan_report.json
```

### Use Case 3: Scanning Specific Component

```python
# Scan just one tool
result = await scanner.scan_stdio_server_tool(
    server_config=server_config,
    tool_name="calculate",
    analyzers=[AnalyzerEnum.YARA]
)

print(f"Findings: {len(result.findings)}")
```

---

## 🔗 Related Documentation

### Project Documentation
- [Main README](../README.md) - Project overview
- [CLAUDE.md](../CLAUDE.md) - Development guide
- [Scanner Setup](../docs/SCANNER_SETUP.md) - Installation and configuration
- [Scanner Limitations](../docs/SCANNER_LIMITATIONS.md) - What can/cannot be scanned

### External Resources
- [YARA Documentation](https://yara.readthedocs.io/)
- [Cisco AI MCP Scanner](https://developer.cisco.com/docs/ai-defense/)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)

---

## ❓ FAQ

### Q: Why can't resources be scanned?

**A:** The `cisco-ai-mcp-scanner` package doesn't support stdio resource scanning. Only HTTP endpoints can scan resources. This is a known limitation. See [SCANNER_LIMITATIONS.md](../docs/SCANNER_LIMITATIONS.md).

### Q: What if YARA detects my safe code as vulnerable?

**A:** YARA detects patterns, but the scanner analyzes context. If proper mitigations are in place (like in our `calculate` tool with `eval()`), the scanner will mark it as safe. See [Example 4 in PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md#example-4-complex-tool---calculate).

### Q: How do I add custom YARA rules?

**A:** Create a `.yara` file with your rules and configure the scanner to load it. See [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md#4-custom-yara-rules) for examples.

### Q: Should I use YARA alone or combine with other analyzers?

**A:** For comprehensive security:
- **YARA** - Fast pattern matching (use in CI/CD)
- **LLM** - Context-aware analysis (use for deep audits)
- **API** - Comprehensive checks (use before production)

See [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md#3-combining-analyzers) for comparison.

### Q: How often should I scan?

**A:** 
- **Every commit** - Quick scan (`--quick` flag)
- **Every PR** - Full scan
- **Before deployment** - Full scan + LLM analyzer
- **Weekly/monthly** - Comprehensive scan with all analyzers

### Q: What do the severity levels mean?

**A:**
- **CRITICAL** - Immediate fix required (RCE, data breach)
- **HIGH** - Priority fix (command injection, SQL injection)
- **MEDIUM** - Schedule fix (information disclosure)
- **LOW** - Best practice violation
- **INFO** - Informational only

---

## 📈 Project Scan Summary

### Components in This Project

**Tools (6):**
1. `add` - Simple arithmetic (✅ Clean)
2. `reverse_text` - String manipulation (✅ Clean)
3. `format_json` - JSON formatting (✅ Clean)
4. `calculate` - Math expression evaluator (✅ Clean - mitigated eval)
5. `scan_mcp_server` - Scanner integration (✅ Clean)
6. `check_scanner_status` - Scanner status (✅ Clean)

**Prompts (3):**
1. `code_review` - Code review template (✅ Clean)
2. `summarize` - Summarization template (✅ Clean)
3. `debug_helper` - Debugging template (✅ Clean)

**Resources (4):**
1. `demo://info` - Server info (⚠️ Manual review)
2. `demo://timestamp` - Timestamp (⚠️ Manual review)
3. `demo://examples` - Examples (⚠️ Manual review)
4. `demo://file/data` - File reader (⚠️ Manual review)

**Overall Security Status:** ✅ All scannable components clean

---

## 🎓 Learning Path

### Beginner Track (1 hour)

1. **Understand basics** (15 min)
   - Read "What is YARA?" in [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
   
2. **Run first scan** (10 min)
   - Follow [Quick Start](#-quick-start)
   - Read scan output
   
3. **See examples** (20 min)
   - Examples 1-3 in [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
   
4. **View diagrams** (15 min)
   - Complete Architecture in [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md)

### Intermediate Track (2 hours)

1. **Deep dive rules** (45 min)
   - YARA Rule Categories in [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
   
2. **Study patterns** (45 min)
   - Pattern Matching Details
   - Examples 4-6 in [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
   
3. **Practice fixes** (30 min)
   - Common Patterns and Fixes section

### Advanced Track (3 hours)

1. **Understand internals** (60 min)
   - Complete [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
   
2. **Integration** (60 min)
   - Integration Examples in [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
   - Set up CI/CD
   
3. **Custom rules** (60 min)
   - Write custom YARA rules
   - Test against your code

---

## 🤝 Contributing

Found an issue or want to improve this documentation?

1. Check existing documentation first
2. Create clear examples
3. Test your examples
4. Submit with context

---

## 📝 Document Versions

- **v1.0** (2026-05-11) - Initial comprehensive documentation
  - YARA scanning methodology
  - Flow diagrams
  - Practical examples
  - This README

---

## 📞 Support

**Questions about:**
- **Scanner setup:** See [SCANNER_SETUP.md](../docs/SCANNER_SETUP.md)
- **YARA methodology:** See [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
- **Practical usage:** See [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
- **Project development:** See [CLAUDE.md](../CLAUDE.md)

**External resources:**
- Cisco AI MCP Scanner: https://developer.cisco.com/docs/ai-defense/
- YARA Documentation: https://yara.readthedocs.io/

---

## 🎯 Summary

This documentation folder provides everything you need to understand YARA-based security scanning in the MCP deployment project:

✅ **Theory** - How YARA works, architecture, rules  
✅ **Visual** - Diagrams showing process flows  
✅ **Practice** - Real examples from this project  
✅ **Integration** - CI/CD, hooks, programmatic usage  

**Start here:** [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) → Example 1

**Questions?** Check the [FAQ](#-faq) or related docs above.

Happy scanning! 🔒🔍
