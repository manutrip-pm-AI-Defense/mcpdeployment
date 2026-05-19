# YARA Scanning Quick Reference

One-page cheat sheet for YARA scanning in the MCP deployment project.

---

## 🚀 Commands

```bash
# Quick scan (2 tools, 1 prompt) - ~4 seconds
uv run python scripts/scan.py --quick

# Full scan (6 tools, 3 prompts) - ~10 seconds
uv run python scripts/scan.py

# Test scanner setup
uv run python tests/test_scanner.py
```

---

## 📊 Project Coverage

| Component | Count | Scannable | Status |
|-----------|-------|-----------|--------|
| Tools | 6 | ✅ Yes | All clean |
| Prompts | 3 | ✅ Yes | All clean |
| Resources | 4 | ❌ No (stdio limitation) | Manual review |

---

## 🎯 10 YARA Rule Categories

| Rule File | Detects | Example |
|-----------|---------|---------|
| code_execution.yara | `eval()`, `exec()`, `os.system()` | ⚠️ Line 87: `eval(expression, ...)` |
| command_injection.yara | Shell commands, `nc`, `wget` | `subprocess.run(..., shell=True)` |
| prompt_injection.yara | "Ignore instructions", hidden directives | `<!-- SYSTEM OVERRIDE -->` |
| sql_injection.yara | SQL patterns, union attacks | `SELECT * FROM users WHERE id = {user_id}` |
| data_exfiltration.yara | Network uploads, DNS tunneling | `requests.post(external_url, data=...)` |
| credential_harvesting.yara | Credential theft patterns | Reading `.env`, `.aws/credentials` |
| script_injection.yara | XSS, JavaScript injection | `<script>alert('XSS')</script>` |
| system_manipulation.yara | File deletion, permission changes | `os.remove()`, `chmod 777` |
| tool_poisoning.yara | MCP protocol abuse | Falsifying tool responses |
| coercive_injection.yara | Social engineering | "As your administrator..." |

---

## ✅ Interpreting Results

```bash
[2/9] calculate... ✅ Clean        # No issues
[3/9] dangerous... ⚠️ 2 finding(s) # Security issues found
[4/9] broken... ❌ Error           # Scan failed
```

### Severity Levels

| Severity | Action | Timeline |
|----------|--------|----------|
| **CRITICAL** | Block deployment, fix immediately | < 1 day |
| **HIGH** | Priority fix, may block deployment | < 1 week |
| **MEDIUM** | Schedule fix in sprint | < 1 month |
| **LOW** | Document and plan fix | Backlog |
| **INFO** | Review and acknowledge | Optional |

---

## 🔍 Example: Safe vs. Unsafe Code

### ❌ Vulnerable
```python
def calculate_unsafe(expr: str) -> float:
    return eval(expr)  # CRITICAL: No validation
```

### ✅ Safe (Our Implementation)
```python
def calculate(expr: str) -> float:
    # ✅ Input validation
    allowed = set("0123456789+-*/().% ")
    if not all(c in allowed for c in expr):
        raise ValueError("Invalid characters")
    
    # ✅ Restricted namespace
    return eval(expr, {"__builtins__": {}}, {})
```

---

## 📈 Performance

- **Full scan:** ~10-12 seconds (9 components)
- **Quick scan:** ~4-5 seconds (3 components)
- **Per component:** ~1-1.5 seconds
- **Per rule:** ~10-15ms

---

## 🛠️ Common Fixes

### Fix 1: eval() → ast.literal_eval()
```python
# Before
result = eval(user_input)

# After
import ast
result = ast.literal_eval(user_input)  # Safer for literals
```

### Fix 2: shell=True → shell=False
```python
# Before
subprocess.run(cmd, shell=True)  # Dangerous

# After
subprocess.run(["git", "status"])  # Safe
```

### Fix 3: SQL Injection → Parameterized Query
```python
# Before
query = f"SELECT * FROM users WHERE id = {user_id}"

# After
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### Fix 4: Prompt Sanitization
```python
# Before
prompt = f"Process: {user_input}"  # Can inject instructions

# After
forbidden = ["ignore", "disregard", "admin"]
if any(word in user_input.lower() for word in forbidden):
    raise ValueError("Forbidden pattern")
prompt = f"Process (literal): {user_input}"
```

---

## 🔗 CI/CD Integration

### GitHub Actions
```yaml
- name: Security Scan
  run: uv run python scripts/scan.py

- name: Check Exit Code
  run: |
    if [ $? -ne 0 ]; then
      echo "Security issues found"
      exit 1
    fi
```

### Pre-commit Hook
```bash
#!/bin/bash
uv run python scripts/scan.py --quick || exit 1
```

---

## 🎓 Reading Guide

| For | Start With | Time |
|-----|------------|------|
| **Beginners** | [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) Ex 1-2 | 15 min |
| **Security** | [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md) Rules | 30 min |
| **Developers** | [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md) Integration | 20 min |
| **Visual learners** | [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md) | 15 min |

---

## 📞 Quick Links

- **Full Methodology:** [YARA_SCANNING_METHODOLOGY.md](./YARA_SCANNING_METHODOLOGY.md)
- **Flow Diagrams:** [SCANNING_FLOW_DIAGRAM.md](./SCANNING_FLOW_DIAGRAM.md)
- **Practical Examples:** [PRACTICAL_EXAMPLES.md](./PRACTICAL_EXAMPLES.md)
- **Setup Guide:** [../docs/SCANNER_SETUP.md](../docs/SCANNER_SETUP.md)
- **Limitations:** [../docs/SCANNER_LIMITATIONS.md](../docs/SCANNER_LIMITATIONS.md)

---

## 🎯 Our Project Status

### All 6 Tools: ✅ Clean
1. `add` - Simple arithmetic
2. `reverse_text` - String manipulation
3. `format_json` - JSON formatting
4. `calculate` - Math evaluator (mitigated eval)
5. `scan_mcp_server` - Scanner integration
6. `check_scanner_status` - Status checker

### All 3 Prompts: ✅ Clean
1. `code_review` - Code review template
2. `summarize` - Summarization template
3. `debug_helper` - Debugging template

### 4 Resources: ⚠️ Manual Review
(Cannot scan via stdio - package limitation)

**Overall:** 🎉 No security vulnerabilities found

---

## ❓ FAQ Quick Answers

**Q: Why can't resources be scanned?**  
A: Stdio limitation. Only HTTP endpoints support resource scanning.

**Q: Is eval() always bad?**  
A: No. Our `calculate` tool uses it safely with validation + restricted namespace.

**Q: How often should I scan?**  
A: Every commit (quick), every PR (full), before deployment (full+LLM).

**Q: Can I customize rules?**  
A: Yes. Create `.yara` files and configure scanner to load them.

**Q: YARA vs LLM vs API analyzer?**  
A: YARA = Fast patterns, LLM = Context analysis, API = Comprehensive (needs key).

---

## 🔑 Key Takeaways

1. ✅ **YARA is fast** - Seconds, not minutes
2. ✅ **Context matters** - Dangerous functions can be safe with mitigations
3. ✅ **10 rule categories** - Covers major threat types
4. ✅ **Easy integration** - CLI, CI/CD, programmatic
5. ✅ **No API key needed** - YARA works offline

---

**Start scanning:** `uv run python scripts/scan.py --quick`

**Need help?** Read [README.md](./README.md) for full guide.
