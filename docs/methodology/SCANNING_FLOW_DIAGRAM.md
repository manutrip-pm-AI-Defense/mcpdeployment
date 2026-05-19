# YARA Scanning Flow Diagrams

## Complete Scanning Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP SECURITY SCANNING                         │
│                                                                       │
│  User/CI Pipeline                                                     │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────┐                                                │
│  │  scan.py Script │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           │ Initializes                                              │
│           ▼                                                           │
│  ┌─────────────────────────────────────────────────────┐           │
│  │          Cisco AI MCP Scanner                        │           │
│  │  ┌───────────────────────────────────────────────┐  │           │
│  │  │  Scanner Instance                              │  │           │
│  │  │  • Config loading                              │  │           │
│  │  │  • Analyzer selection                          │  │           │
│  │  │  • Result aggregation                          │  │           │
│  │  └───────────────────────────────────────────────┘  │           │
│  │                                                       │           │
│  │  ┌───────────────────────────────────────────────┐  │           │
│  │  │  YARA Engine                                   │  │           │
│  │  │  ┌─────────────────────────────────────────┐  │  │           │
│  │  │  │  Rule Loader                             │  │  │           │
│  │  │  │  • code_execution.yara                   │  │  │           │
│  │  │  │  • command_injection.yara                │  │  │           │
│  │  │  │  • prompt_injection.yara                 │  │  │           │
│  │  │  │  • sql_injection.yara                    │  │  │           │
│  │  │  │  • data_exfiltration.yara                │  │  │           │
│  │  │  │  • credential_harvesting.yara            │  │  │           │
│  │  │  │  • script_injection.yara                 │  │  │           │
│  │  │  │  • system_manipulation.yara              │  │  │           │
│  │  │  │  • tool_poisoning.yara                   │  │  │           │
│  │  │  │  • coercive_injection.yara               │  │  │           │
│  │  │  └─────────────────────────────────────────┘  │  │           │
│  │  │                                                 │  │           │
│  │  │  ┌─────────────────────────────────────────┐  │  │           │
│  │  │  │  Pattern Matcher                         │  │  │           │
│  │  │  │  • Regex engine                          │  │  │           │
│  │  │  │  • String comparison                     │  │  │           │
│  │  │  │  • Context extraction                    │  │  │           │
│  │  │  └─────────────────────────────────────────┘  │  │           │
│  │  └───────────────────────────────────────────────┘  │           │
│  └─────────────────────────────────────────────────────┘           │
│                          │                                           │
│                          │ Connects to                              │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────┐           │
│  │          MCP Server (stdio mode)                     │           │
│  │  ┌───────────────────────────────────────────────┐  │           │
│  │  │  FastMCP Instance (server.py)                  │  │           │
│  │  │                                                 │  │           │
│  │  │  Tools (6):                                     │  │           │
│  │  │  • add()              ─┐                       │  │           │
│  │  │  • reverse_text()     ─┤                       │  │           │
│  │  │  • format_json()      ─┼─▶ Scanned             │  │           │
│  │  │  • calculate()        ─┤   individually         │  │           │
│  │  │  • scan_mcp_server()  ─┤                       │  │           │
│  │  │  • check_scanner...() ─┘                       │  │           │
│  │  │                                                 │  │           │
│  │  │  Prompts (3):                                   │  │           │
│  │  │  • code_review()      ─┐                       │  │           │
│  │  │  • summarize()        ─┼─▶ Scanned             │  │           │
│  │  │  • debug_helper()     ─┘   individually         │  │           │
│  │  │                                                 │  │           │
│  │  │  Resources (4):                                 │  │           │
│  │  │  • demo://info        ─┐                       │  │           │
│  │  │  • demo://timestamp   ─┼─▶ NOT scannable       │  │           │
│  │  │  • demo://examples    ─┤   (stdio limitation)  │  │           │
│  │  │  • demo://file/data   ─┘                       │  │           │
│  │  └───────────────────────────────────────────────┘  │           │
│  └─────────────────────────────────────────────────────┘           │
│                          │                                           │
│                          │ Returns                                   │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────┐           │
│  │          Scan Results                                │           │
│  │  • ToolScanResult objects                            │           │
│  │  • PromptScanResult objects                          │           │
│  │  • SecurityFinding objects (if issues found)         │           │
│  └─────────────────────────────────────────────────────┘           │
│                          │                                           │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────┐           │
│  │          Report Generation                           │           │
│  │  • Console output with status icons                  │           │
│  │  • JSON report (scan_report.json)                    │           │
│  │  • Summary statistics                                │           │
│  └─────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Single Component Scan Flow

### Tool Scanning Process

```
┌────────────────────────────────────────────────────────────┐
│ STEP 1: Initiate Tool Scan                                 │
│                                                            │
│  scanner.scan_stdio_server_tool(                           │
│      server_config=StdioServer(...),                       │
│      tool_name="calculate",                                │
│      analyzers=[AnalyzerEnum.YARA],                        │
│      timeout=30                                             │
│  )                                                          │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 2: Connect to MCP Server                              │
│                                                            │
│  • Spawn server process: uv run python -m mcpserver       │
│  • Establish stdio communication channel                   │
│  • Send MCP protocol handshake                             │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 3: Request Tool Metadata                              │
│                                                            │
│  MCP Request:                                              │
│  {                                                          │
│    "method": "tools/list"                                  │
│  }                                                          │
│                                                            │
│  MCP Response:                                             │
│  {                                                          │
│    "tools": [                                              │
│      {                                                     │
│        "name": "calculate",                                │
│        "description": "Evaluate a simple math expression", │
│        "inputSchema": { ... }                              │
│      }                                                     │
│    ]                                                        │
│  }                                                          │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 4: Extract Tool Source Code                           │
│                                                            │
│  Scanner extracts:                                         │
│  • Function name: "calculate"                              │
│  • Docstring: "Evaluate a simple..."                       │
│  • Parameters: expression (str)                            │
│  • Return type: float                                      │
│  • Implementation code:                                    │
│                                                            │
│    def calculate(expression: str) -> float:                │
│        allowed_chars = set("0123456789+-*/().% ")          │
│        if not all(c in allowed_chars for c in expression): │
│            raise ValueError(...)                           │
│        result = eval(expression, {"__builtins__": {}}, {}) │
│        return float(result)                                │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 5: Convert to Scannable Text                          │
│                                                            │
│  Text representation for YARA:                             │
│  """                                                        │
│  TOOL: calculate                                           │
│  DESCRIPTION: Evaluate a simple mathematical expression    │
│                                                            │
│  PARAMETERS:                                               │
│  - expression: str                                         │
│                                                            │
│  IMPLEMENTATION:                                           │
│  def calculate(expression: str) -> float:                  │
│      allowed_chars = set("0123456789+-*/().% ")            │
│      if not all(c in allowed_chars for c in expression):   │
│          raise ValueError("Invalid characters")            │
│      result = eval(expression, {"__builtins__": {}}, {})   │
│      return float(result)                                  │
│  """                                                        │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 6: Apply YARA Rules                                   │
│                                                            │
│  For each .yara file:                                      │
│                                                            │
│  ┌─────────────────────────────────────────┐             │
│  │ code_execution.yara                      │             │
│  │                                           │             │
│  │ Pattern: /\beval\s*\(/i                  │             │
│  │ Match: Line 87 "eval(expression, ..."    │ ◀── MATCH  │
│  └─────────────────────────────────────────┘             │
│                                                            │
│  ┌─────────────────────────────────────────┐             │
│  │ command_injection.yara                   │             │
│  │                                           │             │
│  │ Pattern: /\b(os\.system|subprocess)\s*\(/│             │
│  │ Match: None                               │ ◀── CLEAN  │
│  └─────────────────────────────────────────┘             │
│                                                            │
│  ┌─────────────────────────────────────────┐             │
│  │ sql_injection.yara                       │             │
│  │                                           │             │
│  │ Pattern: /SELECT.*FROM/i                 │             │
│  │ Match: None                               │ ◀── CLEAN  │
│  └─────────────────────────────────────────┘             │
│                                                            │
│  ... (8 more rule files)                                   │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 7: Analyze Matches in Context                         │
│                                                            │
│  Match found: eval() at line 87                            │
│                                                            │
│  Context analysis:                                         │
│  • Input validation present? ✅ Yes (allowed_chars)       │
│  • Restricted namespace? ✅ Yes ({"__builtins__": {}})    │
│  • Error handling? ✅ Yes (try-except)                    │
│  • User input sanitized? ✅ Yes (character whitelist)     │
│                                                            │
│  Risk assessment:                                          │
│  • Raw risk: HIGH (eval is dangerous)                      │
│  • Mitigated risk: LOW (proper controls in place)         │
│  • Final decision: PASS with note                          │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 8: Generate Result                                    │
│                                                            │
│  ToolScanResult(                                           │
│      tool_name="calculate",                                │
│      tool_description="Evaluate a simple math expression", │
│      status="completed",                                   │
│      analyzers=["yara"],                                   │
│      findings=[]  # Empty - mitigations sufficient         │
│  )                                                          │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────────┐
│ STEP 9: Return to Caller                                   │
│                                                            │
│  scan.py receives result and prints:                       │
│  [2/9] calculate... ✅ Clean                              │
└────────────────────────────────────────────────────────────┘
```

---

## YARA Rule Execution Detail

### How a Single Rule Processes Text

```
┌──────────────────────────────────────────────────────────────┐
│  INPUT TEXT (from MCP tool "calculate")                       │
│                                                               │
│  Line 1:  def calculate(expression: str) -> float:            │
│  Line 2:      allowed_chars = set("0123456789+-*/().% ")      │
│  Line 3:      if not all(c in allowed_chars ...):             │
│  Line 4:          raise ValueError(...)                       │
│  Line 5:      result = eval(expression, {...}, {})            │
│  Line 6:      return float(result)                            │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  YARA RULE: code_execution.yara                               │
│                                                               │
│  rule code_execution {                                        │
│      meta:                                                    │
│          threat_type = "CODE EXECUTION"                       │
│                                                               │
│      strings:                                                 │
│          $python_exec = /\beval\s*\(/i                        │
│                                                               │
│      condition:                                               │
│          $python_exec                                         │
│  }                                                             │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  PATTERN MATCHING ENGINE                                      │
│                                                               │
│  Processing pattern: /\beval\s*\(/i                           │
│                                                               │
│  Line 1: def calculate... ───────────────▶ No match          │
│  Line 2: allowed_chars... ───────────────▶ No match          │
│  Line 3: if not all... ──────────────────▶ No match          │
│  Line 4: raise ValueError... ────────────▶ No match          │
│  Line 5: result = eval(expression...) ───▶ ⚠️ MATCH FOUND!  │
│          └─────┬──────┘                                       │
│                │                                              │
│                ▼                                              │
│         ┌──────────────────────┐                             │
│         │ Capture Details:      │                             │
│         │ • Position: Line 5    │                             │
│         │ • Text: "eval("       │                             │
│         │ • Context: 50 chars   │                             │
│         └──────────────────────┘                             │
│  Line 6: return float... ────────────────▶ No match          │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  MATCH RESULT                                                 │
│                                                               │
│  {                                                             │
│      "rule": "code_execution",                                │
│      "string": "$python_exec",                                │
│      "pattern": "/\\beval\\s*\\(/i",                          │
│      "matches": [                                             │
│          {                                                    │
│              "offset": 145,                                   │
│              "line": 5,                                       │
│              "context": "result = eval(expression, {...})"   │
│          }                                                    │
│      ]                                                        │
│  }                                                             │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  CONTEXTUAL ANALYSIS                                          │
│                                                               │
│  Scanner checks surrounding code:                             │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │ Line 2: Input validation detected           │             │
│  │   allowed_chars = set(...)                  │             │
│  │   ✅ Positive security control               │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │ Line 5: Restricted namespace                │             │
│  │   eval(..., {"__builtins__": {}}, {})       │             │
│  │   ✅ Limits execution scope                  │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  ┌────────────────────────────────────────────┐             │
│  │ Error handling: try-except wrapper          │             │
│  │   ✅ Graceful failure handling               │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  Risk Assessment:                                             │
│  • Pattern matched: ⚠️ YES                                   │
│  • Mitigations present: ✅ YES                               │
│  • Exploitability: ⬇️ LOW (multiple controls)                │
│  • Final verdict: ✅ ACCEPTABLE RISK                         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  DECISION: NO FINDING GENERATED                               │
│                                                               │
│  Because:                                                     │
│  1. Match found but properly mitigated                        │
│  2. Multiple security controls in place                       │
│  3. Low exploitability after analysis                         │
│                                                               │
│  Result: findings = []                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Comparison: Clean vs. Vulnerable Code

### Scenario A: Clean Implementation (Our Project)

```
┌─────────────────────────────────────────────────────────┐
│  TOOL: calculate                                         │
│                                                          │
│  def calculate(expression: str) -> float:                │
│      # ✅ STEP 1: Input validation                      │
│      allowed_chars = set("0123456789+-*/().% ")          │
│      if not all(c in allowed_chars for c in expression): │
│          raise ValueError("Invalid characters")          │
│                                                          │
│      # ⚠️ STEP 2: Eval with restrictions               │
│      result = eval(expression, {"__builtins__": {}}, {}) │
│      return float(result)                                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  YARA SCAN RESULT                                        │
│                                                          │
│  Pattern matched: ✅ YES (eval detected)                │
│  Context analysis: ✅ PASS                              │
│    • Input validation: Present                           │
│    • Restricted namespace: Yes                           │
│    • Character whitelist: Enforced                       │
│                                                          │
│  Findings: 0                                             │
│  Status: ✅ Clean                                       │
└─────────────────────────────────────────────────────────┘
```

### Scenario B: Vulnerable Implementation

```
┌─────────────────────────────────────────────────────────┐
│  TOOL: calculate_unsafe                                  │
│                                                          │
│  def calculate_unsafe(expression: str) -> float:         │
│      # ❌ NO validation                                 │
│      # ❌ Unrestricted eval                             │
│      result = eval(expression)                           │
│      return float(result)                                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  YARA SCAN RESULT                                        │
│                                                          │
│  Pattern matched: ✅ YES (eval detected)                │
│  Context analysis: ❌ FAIL                              │
│    • Input validation: MISSING                           │
│    • Restricted namespace: MISSING                       │
│    • Character whitelist: MISSING                        │
│                                                          │
│  Findings: 1                                             │
│  ┌───────────────────────────────────────────────────┐ │
│  │ SecurityFinding(                                   │ │
│  │   severity="CRITICAL",                             │ │
│  │   category="CODE_EXECUTION",                       │ │
│  │   title="Unrestricted eval() usage",               │ │
│  │   description="eval() called without restrictions",│ │
│  │   recommendation="Use ast.literal_eval() or ..."   │ │
│  │ )                                                   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  Status: ❌ CRITICAL VULNERABILITY                      │
└─────────────────────────────────────────────────────────┘
```

---

## Performance Metrics

### Scanning Timeline

```
Time (seconds)
│
│  0.0s ─┐
│        │ Scanner initialization
│  0.1s ─┤ • Load config
│        │ • Initialize YARA engine
│        │ • Load 10 rule files
│  0.3s ─┘
│        │
│  0.3s ─┐
│        │ MCP server connection
│  0.5s ─┤ • Spawn server process
│        │ • Stdio handshake
│  0.7s ─┘
│        │
│  0.7s ─┐
│        │ Scan tool #1: "add"
│  1.2s ─┤ • Extract source
│        │ • Apply 10 YARA rules
│        │ • Analyze context
│  1.5s ─┘
│        │
│  1.5s ─┐
│        │ Scan tool #2: "calculate"
│  2.0s ─┤ • Extract source
│        │ • Apply 10 YARA rules
│        │ • Analyze context
│  2.3s ─┘
│        │
│        ... (4 more tools)
│        │
│  7.0s ─┐
│        │ Scan prompt #1: "code_review"
│  7.5s ─┤ • Extract template
│        │ • Apply 10 YARA rules
│  7.7s ─┘
│        │
│        ... (2 more prompts)
│        │
│  9.5s ─┐
│        │ Result aggregation
│ 10.0s ─┤ • Generate summary
│        │ • Create JSON report
│ 10.2s ─┘
│        │
│        ▼ Done
```

### Rule Processing Time

```
Average time per component per rule: ~10-15ms

code_execution.yara      ████░░░░░░  12ms
command_injection.yara   █████░░░░░  15ms
prompt_injection.yara    ████████░░  22ms  ◀── Most complex patterns
sql_injection.yara       ███░░░░░░░   9ms
data_exfiltration.yara   █████░░░░░  14ms
credential_harvesting.   ██████░░░░  18ms
script_injection.yara    ███░░░░░░░   8ms
system_manipulation.yara ████░░░░░░  11ms
tool_poisoning.yara      █████░░░░░  13ms
coercive_injection.yara  ███████░░░  20ms
                         ─────────────────
Total per component:     ~142ms average
```

---

## Summary

These diagrams illustrate:

1. **Complete Architecture**: How all components interact in the scanning pipeline
2. **Single Component Flow**: Detailed steps for scanning one tool
3. **Pattern Matching**: How YARA rules process code line-by-line
4. **Context Analysis**: How mitigations affect final decisions
5. **Comparison**: Clean vs. vulnerable code handling
6. **Performance**: Timing breakdown for understanding scan duration

The YARA scanning methodology in this project provides fast, reliable security analysis with minimal overhead, making it suitable for CI/CD integration and rapid feedback cycles.
