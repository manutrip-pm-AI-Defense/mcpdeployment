# Documentation Index

Visual guide to navigate the YARA scanning methodology documentation.

```
scanning_methodology_doc/
│
├── 📖 README.md ⭐ START HERE
│   └── Overview of all documentation
│       Quick start guide
│       Reading guide for different roles
│       FAQ and support links
│
├── ⚡ QUICK_REFERENCE.md
│   └── One-page cheat sheet
│       Commands, rules, examples
│       Fast lookup reference
│
├── 📚 YARA_SCANNING_METHODOLOGY.md
│   └── Complete methodology guide
│       ├── What is YARA?
│       ├── How it works in MCP Scanner
│       ├── 10 YARA rule categories (detailed)
│       ├── Scanning process flow
│       ├── Examples from this project
│       ├── Pattern matching details
│       └── Best practices
│
├── 🎨 SCANNING_FLOW_DIAGRAM.md
│   └── Visual diagrams (ASCII art)
│       ├── Complete scanning architecture
│       ├── Single component scan flow
│       ├── YARA rule execution detail
│       ├── Clean vs vulnerable comparison
│       └── Performance metrics
│
├── 💻 PRACTICAL_EXAMPLES.md
│   └── Hands-on code examples
│       ├── Quick start examples
│       ├── Tool scanning (all 6 tools)
│       ├── Prompt scanning (all 3 prompts)
│       ├── Common patterns and fixes
│       └── Integration examples (CI/CD, hooks)
│
└── 📑 INDEX.md (this file)
    └── Navigation guide
```

---

## 🗺️ Navigation Map

### By Learning Style

**📖 Read Theory First:**
```
README.md → YARA_SCANNING_METHODOLOGY.md → SCANNING_FLOW_DIAGRAM.md → PRACTICAL_EXAMPLES.md
```

**💻 Learn By Doing:**
```
QUICK_REFERENCE.md → PRACTICAL_EXAMPLES.md → YARA_SCANNING_METHODOLOGY.md
```

**🎨 Visual Learner:**
```
SCANNING_FLOW_DIAGRAM.md → README.md → PRACTICAL_EXAMPLES.md
```

### By Role

**👨‍💻 Developer (Integrating Scanner):**
```
QUICK_REFERENCE.md
    ↓
PRACTICAL_EXAMPLES.md (Integration section)
    ↓
YARA_SCANNING_METHODOLOGY.md (Best Practices)
```

**🔒 Security Engineer:**
```
YARA_SCANNING_METHODOLOGY.md (Full read)
    ↓
PRACTICAL_EXAMPLES.md (Patterns and Fixes)
    ↓
QUICK_REFERENCE.md (Reference)
```

**📚 Beginner:**
```
README.md (Quick Start)
    ↓
PRACTICAL_EXAMPLES.md (Examples 1-3)
    ↓
SCANNING_FLOW_DIAGRAM.md (Architecture)
    ↓
YARA_SCANNING_METHODOLOGY.md (Deep dive)
```

### By Task

**🎯 "I want to run my first scan"**
```
README.md → Quick Start section
or
QUICK_REFERENCE.md → Commands section
```

**🎯 "I need to understand what YARA does"**
```
YARA_SCANNING_METHODOLOGY.md → "What is YARA?" section
or
SCANNING_FLOW_DIAGRAM.md → Complete Architecture
```

**🎯 "I found a security issue, how do I fix it?"**
```
PRACTICAL_EXAMPLES.md → Common Patterns and Fixes
or
QUICK_REFERENCE.md → Common Fixes section
```

**🎯 "I want to integrate this in CI/CD"**
```
PRACTICAL_EXAMPLES.md → Integration Examples
or
QUICK_REFERENCE.md → CI/CD Integration section
```

**🎯 "I want to understand the calculate tool"**
```
PRACTICAL_EXAMPLES.md → Example 4
or
YARA_SCANNING_METHODOLOGY.md → Example 1
```

**🎯 "Show me the scan flow visually"**
```
SCANNING_FLOW_DIAGRAM.md → Single Component Scan Flow
or
SCANNING_FLOW_DIAGRAM.md → YARA Rule Execution Detail
```

---

## 📊 Document Statistics

| Document | Pages | Reading Time | Difficulty |
|----------|-------|--------------|------------|
| README.md | ~12 | 15 min | ⭐ Easy |
| QUICK_REFERENCE.md | ~3 | 5 min | ⭐ Easy |
| YARA_SCANNING_METHODOLOGY.md | ~30 | 45 min | ⭐⭐ Medium |
| SCANNING_FLOW_DIAGRAM.md | ~20 | 25 min | ⭐⭐ Medium |
| PRACTICAL_EXAMPLES.md | ~25 | 40 min | ⭐⭐⭐ Advanced |

**Total:** ~90 pages, ~2 hours reading time

---

## 🎓 Suggested Learning Paths

### Path 1: Quick Start (30 minutes)
```
1. README.md → Quick Start (5 min)
2. QUICK_REFERENCE.md (5 min)
3. PRACTICAL_EXAMPLES.md → Examples 1-3 (20 min)
```
**Result:** Can run scans and understand basic results

---

### Path 2: Comprehensive Understanding (2 hours)
```
1. README.md (15 min)
2. YARA_SCANNING_METHODOLOGY.md (45 min)
3. SCANNING_FLOW_DIAGRAM.md (25 min)
4. PRACTICAL_EXAMPLES.md (30 min)
5. QUICK_REFERENCE.md (5 min)
```
**Result:** Deep understanding of YARA scanning

---

### Path 3: Practical Integration (1 hour)
```
1. QUICK_REFERENCE.md (5 min)
2. PRACTICAL_EXAMPLES.md → Integration (30 min)
3. YARA_SCANNING_METHODOLOGY.md → Best Practices (15 min)
4. README.md → FAQ (10 min)
```
**Result:** Ready to integrate in your workflow

---

### Path 4: Security Audit Focus (1.5 hours)
```
1. YARA_SCANNING_METHODOLOGY.md → Rule Categories (30 min)
2. PRACTICAL_EXAMPLES.md → Patterns and Fixes (30 min)
3. SCANNING_FLOW_DIAGRAM.md → Comparison (15 min)
4. QUICK_REFERENCE.md → Common Fixes (15 min)
```
**Result:** Can identify and fix vulnerabilities

---

## 🔍 Search Guide

### Finding Specific Information

**"How does eval() work in this project?"**
- PRACTICAL_EXAMPLES.md → Example 4
- YARA_SCANNING_METHODOLOGY.md → Example 1

**"What rules are applied?"**
- YARA_SCANNING_METHODOLOGY.md → YARA Rule Categories
- QUICK_REFERENCE.md → 10 YARA Rule Categories

**"How long does scanning take?"**
- SCANNING_FLOW_DIAGRAM.md → Performance Metrics
- QUICK_REFERENCE.md → Performance

**"CI/CD integration code?"**
- PRACTICAL_EXAMPLES.md → Example 10-12
- QUICK_REFERENCE.md → CI/CD Integration

**"What's the architecture?"**
- SCANNING_FLOW_DIAGRAM.md → Complete Architecture
- YARA_SCANNING_METHODOLOGY.md → Architecture

**"Common vulnerabilities and fixes?"**
- PRACTICAL_EXAMPLES.md → Common Patterns and Fixes
- QUICK_REFERENCE.md → Common Fixes

---

## 📚 Cross-References

### README.md Links To:
- All other documents (overview)
- Related project docs (SCANNER_SETUP.md, etc.)
- External resources

### YARA_SCANNING_METHODOLOGY.md Contains:
- Theory and concepts
- Detailed rule explanations
- Real project examples
- Best practices

### SCANNING_FLOW_DIAGRAM.md Shows:
- Visual process flows
- Architecture diagrams
- Performance charts
- Comparison diagrams

### PRACTICAL_EXAMPLES.md Provides:
- Executable code
- Real scan outputs
- Integration recipes
- Fix examples

### QUICK_REFERENCE.md Summarizes:
- Commands
- Rules table
- Common fixes
- Quick links

---

## 🎯 Key Sections Quick Access

### Commands
- QUICK_REFERENCE.md → Commands
- README.md → Quick Start

### Architecture
- SCANNING_FLOW_DIAGRAM.md → Complete Architecture
- YARA_SCANNING_METHODOLOGY.md → How YARA Works

### Rules
- YARA_SCANNING_METHODOLOGY.md → YARA Rule Categories
- QUICK_REFERENCE.md → 10 YARA Rule Categories

### Examples
- PRACTICAL_EXAMPLES.md → All examples
- YARA_SCANNING_METHODOLOGY.md → Examples section

### Integration
- PRACTICAL_EXAMPLES.md → Integration Examples
- QUICK_REFERENCE.md → CI/CD Integration

### Troubleshooting
- README.md → FAQ
- PRACTICAL_EXAMPLES.md → Common Patterns

---

## 📖 Recommended First Read

**👉 Start here: [README.md](./README.md)**

It provides:
- Overview of all documents
- Quick start guide
- Reading recommendations by role
- FAQ and support

**Then choose your path:**
- Quick learner? → QUICK_REFERENCE.md
- Hands-on? → PRACTICAL_EXAMPLES.md
- Theory-focused? → YARA_SCANNING_METHODOLOGY.md
- Visual? → SCANNING_FLOW_DIAGRAM.md

---

## 🔗 External Links Context

All documents link to:
- **Project docs:** SCANNER_SETUP.md, SCANNER_LIMITATIONS.md, CLAUDE.md
- **YARA official:** https://yara.readthedocs.io/
- **Cisco AI Scanner:** https://developer.cisco.com/docs/ai-defense/
- **MCP Protocol:** https://modelcontextprotocol.io/

---

## ✅ Document Checklist

Use this to track your reading progress:

- [ ] README.md - Overview and quick start
- [ ] QUICK_REFERENCE.md - Cheat sheet
- [ ] YARA_SCANNING_METHODOLOGY.md - Full methodology
- [ ] SCANNING_FLOW_DIAGRAM.md - Visual diagrams
- [ ] PRACTICAL_EXAMPLES.md - Hands-on examples
- [ ] Run first scan: `uv run python scripts/scan.py --quick`
- [ ] Understand project components (6 tools, 3 prompts)
- [ ] Review YARA rule categories (10 types)
- [ ] Try integration example (CI/CD or pre-commit)

---

**Happy learning! 🎓**

Start with [README.md](./README.md) and choose your path from there.
