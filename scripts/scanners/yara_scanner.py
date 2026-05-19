#!/usr/bin/env python3
"""
MCP Security Scanner with YARA (Pattern-Based) Analysis
Fast pattern-based vulnerability detection

Usage:
    python scripts/scanners/yara_scanner.py              # Full detailed scan
    python scripts/scanners/yara_scanner.py --quick      # Quick scan (sample components)
"""

import asyncio
import json
import sys
import argparse
from mcpscanner import Scanner, Config, AnalyzerEnum
from mcpscanner.core.mcp_models import StdioServer


async def scan(quick: bool = False):
    """Run security scan on MCP server"""

    print("=" * 80)
    print("YARA PATTERN-BASED MCP SECURITY SCAN")
    print("=" * 80)
    print()

    # Configure scanner
    config = Config()
    scanner = Scanner(config=config)

    # Define MCP server
    server_config = StdioServer(
        command="uv",
        args=["run", "--", "python", "-m", "mcpserver"],
        env={"PYTHONPATH": "/Users/manutripathi/Documents/Projects/mcpdeployment/src"}
    )

    print("📋 Configuration:")
    print(f"   Server: {server_config.command} {' '.join(server_config.args)}")
    print(f"   Analyzer: YARA (Pattern-Based Security Analysis)")
    print(f"   Mode: {'Quick' if quick else 'Full'}")
    print()

    # Define components to scan
    if quick:
        tools_to_scan = ["add", "calculate"]
        prompts_to_scan = ["code_review"]
    else:
        tools_to_scan = [
            "add", "reverse_text", "format_json",
            "calculate", "scan_mcp_server", "check_scanner_status"
        ]
        prompts_to_scan = ["code_review", "summarize", "debug_helper"]

    all_results = []
    total_components = len(tools_to_scan) + len(prompts_to_scan)

    # Scan Tools
    print(f"🔧 Scanning {len(tools_to_scan)} Tools...")
    print("-" * 80)

    for i, tool_name in enumerate(tools_to_scan, 1):
        print(f"[{i}/{total_components}] {tool_name}...", end=" ")

        try:
            result = await scanner.scan_stdio_server_tool(
                server_config=server_config,
                tool_name=tool_name,
                analyzers=[AnalyzerEnum.YARA],
                timeout=30
            )
            result.component_type = "tool"
            all_results.append(result)

            if result.findings:
                print(f"⚠️  {len(result.findings)} finding(s)")
            else:
                print("✅ Clean")

        except Exception as e:
            print(f"❌ Error: {e}")

    print()

    # Scan Prompts
    print(f"💬 Scanning {len(prompts_to_scan)} Prompts...")
    print("-" * 80)

    for i, prompt_name in enumerate(prompts_to_scan, len(tools_to_scan) + 1):
        print(f"[{i}/{total_components}] {prompt_name}...", end=" ")

        try:
            result = await scanner.scan_stdio_server_prompt(
                server_config=server_config,
                prompt_name=prompt_name,
                analyzers=[AnalyzerEnum.YARA],
                timeout=30
            )
            result.component_type = "prompt"
            all_results.append(result)

            if result.findings:
                print(f"⚠️  {len(result.findings)} finding(s)")
            else:
                print("✅ Clean")

        except Exception as e:
            print(f"❌ Error: {e}")

    print()

    # Summary
    total_findings = sum(len(r.findings) for r in all_results)

    print("=" * 80)
    print("SCAN RESULTS")
    print("=" * 80)
    print()
    print(f"✅ Components Scanned: {len(all_results)}")
    print(f"   • Tools: {len(tools_to_scan)}")
    print(f"   • Prompts: {len(prompts_to_scan)}")
    print(f"   • Security Findings: {total_findings}")
    print()

    if total_findings == 0:
        print("🎉 All components passed security checks!")
    else:
        print(f"⚠️  {total_findings} security issue(s) found.")
        print()

        # Show findings
        for result in all_results:
            if result.findings:
                name = getattr(result, 'tool_name', getattr(result, 'prompt_name', 'unknown'))
                print(f"Issues in '{name}':")
                for finding in result.findings:
                    print(f"  • [{finding.severity}] {finding.title}")
                    print(f"    {finding.description}")
                print()

    # Resources note
    print()
    print("ℹ️  Note: Resources (4) cannot be scanned via stdio (package limitation)")
    print("   See docs/SCANNER_LIMITATIONS.md for details")
    print()

    # Save report
    if not quick:
        report = {
            "scan_date": "2026-05-10",
            "summary": {
                "tools_scanned": len(tools_to_scan),
                "prompts_scanned": len(prompts_to_scan),
                "total_findings": total_findings
            },
            "results": []
        }

        for r in all_results:
            result_data = {
                "type": getattr(r, 'component_type', 'unknown'),
                "status": r.status,
                "findings_count": len(r.findings)
            }

            if hasattr(r, 'tool_name'):
                result_data["name"] = r.tool_name
            elif hasattr(r, 'prompt_name'):
                result_data["name"] = r.prompt_name

            report["results"].append(result_data)

        with open("reports/scan_report_yara.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 YARA scan report saved: reports/scan_report_yara.json")
        print()

    return 0 if total_findings == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Scan MCP server for security vulnerabilities")
    parser.add_argument('--quick', action='store_true', help='Quick scan (sample components only)')
    args = parser.parse_args()

    try:
        exit_code = asyncio.run(scan(quick=args.quick))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nScan cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Scan failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
