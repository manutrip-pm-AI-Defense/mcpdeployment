#!/usr/bin/env python3
"""
MCP Security Scanner with Cisco AI Defense API
Comprehensive cloud-based security analysis using Cisco's AI Defense platform

Usage:
    python scripts/scanners/cisco_api_scanner.py              # Full scan with Cisco API
    python scripts/scanners/cisco_api_scanner.py --quick      # Quick scan (sample components)

Note:
    - Requires MCP_SCANNER_API_KEY from https://aidefense.security.cisco.com/
    - For fast YARA-only scanning, use: python scripts/scanners/yara_scanner.py
    - For LLM analysis, use: python scripts/scanners/llm_api_scanner.py
"""

import asyncio
import json
import sys
import os
import argparse
import time
from datetime import datetime
from mcpscanner import Scanner, Config, AnalyzerEnum
from mcpscanner.core.mcp_models import StdioServer


async def scan(quick: bool = False):
    """Run comprehensive security scan with Cisco AI Defense API"""

    print("=" * 80)
    print("CISCO AI DEFENSE API - COMPREHENSIVE MCP SECURITY SCAN")
    print("=" * 80)
    print()

    # Load Cisco API credentials from environment
    api_key = os.getenv("MCP_SCANNER_API_KEY")
    api_endpoint = os.getenv("MCP_SCANNER_ENDPOINT",
                            "https://us.api.inspect.aidefense.security.cisco.com/api/v1")

    if not api_key:
        print("❌ Error: MCP_SCANNER_API_KEY not found in environment")
        print("   This scanner uses Cisco AI Defense API")
        print("   Please configure your API key in .env file")
        print("   Get your key from: https://aidefense.security.cisco.com/")
        print()
        print("   For YARA-only scanning, use: uv run python scripts/scanners/yara_scanner.py")
        print("   For LLM analysis, use: uv run python scripts/scanners/llm_api_scanner.py")
        return 1

    # Configure scanner with Cisco API credentials
    config = Config(
        api_key=api_key,
        endpoint_url=api_endpoint
    )
    scanner = Scanner(config=config)

    # Use only Cisco API analyzer
    analyzers_to_use = [
        AnalyzerEnum.API,  # Cisco AI Defense API analysis
    ]

    # Define MCP server
    server_config = StdioServer(
        command="uv",
        args=["run", "--", "python", "-m", "mcpserver"],
        env={"PYTHONPATH": "/Users/manutripathi/Documents/Projects/mcpdeployment/src"}
    )

    # Display configuration
    print("📋 Configuration:")
    print(f"   Server: {server_config.command} {' '.join(server_config.args)}")
    print(f"   Analyzer: Cisco AI Defense API")
    print(f"   API Endpoint: {api_endpoint}")
    print(f"   API Key: {api_key[:10]}...{api_key[-10:]}")
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
    print(f"🔧 Scanning {len(tools_to_scan)} Tools with Cisco AI Defense API...")
    print("-" * 80)

    for i, tool_name in enumerate(tools_to_scan, 1):
        print(f"[{i}/{total_components}] {tool_name}...", end=" ", flush=True)

        try:
            start_time = time.time()
            result = await scanner.scan_stdio_server_tool(
                server_config=server_config,
                tool_name=tool_name,
                analyzers=analyzers_to_use,
                timeout=60  # Longer timeout for API analysis
            )
            scan_duration = time.time() - start_time

            result.component_type = "tool"
            result.scan_duration = scan_duration
            all_results.append(result)

            if result.findings:
                print(f"⚠️  {len(result.findings)} finding(s) ({scan_duration:.1f}s)")
            else:
                print(f"✅ Clean ({scan_duration:.1f}s)")

        except Exception as e:
            print(f"❌ Error: {e}")

    print()

    # Scan Prompts
    print(f"💬 Scanning {len(prompts_to_scan)} Prompts with Cisco AI Defense API...")
    print("-" * 80)

    for i, prompt_name in enumerate(prompts_to_scan, len(tools_to_scan) + 1):
        print(f"[{i}/{total_components}] {prompt_name}...", end=" ", flush=True)

        try:
            start_time = time.time()
            result = await scanner.scan_stdio_server_prompt(
                server_config=server_config,
                prompt_name=prompt_name,
                analyzers=analyzers_to_use,
                timeout=60  # Longer timeout for API analysis
            )
            scan_duration = time.time() - start_time

            result.component_type = "prompt"
            result.scan_duration = scan_duration
            all_results.append(result)

            if result.findings:
                print(f"⚠️  {len(result.findings)} finding(s) ({scan_duration:.1f}s)")
            else:
                print(f"✅ Clean ({scan_duration:.1f}s)")

        except Exception as e:
            print(f"❌ Error: {e}")

    print()

    # Summary
    total_findings = sum(len(r.findings) for r in all_results)
    total_duration = sum(getattr(r, 'scan_duration', 0) for r in all_results)

    print("=" * 80)
    print("CISCO AI DEFENSE API SCAN RESULTS")
    print("=" * 80)
    print()
    print(f"✅ Components Scanned: {len(all_results)}")
    print(f"   • Tools: {len(tools_to_scan)}")
    print(f"   • Prompts: {len(prompts_to_scan)}")
    print(f"   • Analyzer: Cisco AI Defense API")
    print(f"   • Total Scan Duration: {total_duration:.1f} seconds")
    print(f"   • Security Findings: {total_findings}")
    print()

    if total_findings == 0:
        print("🎉 All components passed Cisco AI Defense security analysis!")
    else:
        print(f"⚠️  {total_findings} security issue(s) found.")
        print()

        # Display findings
        for result in all_results:
            if result.findings:
                name = getattr(result, 'tool_name', getattr(result, 'prompt_name', 'unknown'))
                print(f"📊 Issues in '{name}':")
                print("-" * 80)
                for finding in result.findings:
                    print(f"  • [{finding.severity}] {finding.title}")
                    print(f"    Category: {getattr(finding, 'category', 'N/A')}")
                    print(f"    {finding.description}")
                    if hasattr(finding, 'recommendation') and finding.recommendation:
                        print(f"    Recommendation: {finding.recommendation}")
                    print()

    # Resources note
    print()
    print("ℹ️  Note: Resources (4) cannot be scanned via stdio (package limitation)")
    print("   See docs/SCANNER_LIMITATIONS.md for details")
    print()

    # Save comprehensive report
    if not quick:
        report = {
            "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scan_type": "cisco_api",
            "api_endpoint": api_endpoint,
            "analyzers_used": [a.value for a in analyzers_to_use],
            "summary": {
                "tools_scanned": len(tools_to_scan),
                "prompts_scanned": len(prompts_to_scan),
                "total_findings": total_findings,
                "total_scan_duration_seconds": round(total_duration, 2),
                "avg_scan_duration_seconds": round(total_duration / len(all_results), 2) if all_results else 0
            },
            "results": []
        }

        for r in all_results:
            result_data = {
                "type": getattr(r, 'component_type', 'unknown'),
                "status": r.status,
                "findings_count": len(r.findings),
                "scan_duration_seconds": round(getattr(r, 'scan_duration', 0), 2),
                "analyzers_used": [a.value for a in analyzers_to_use]
            }

            if hasattr(r, 'tool_name'):
                result_data["name"] = r.tool_name
            elif hasattr(r, 'prompt_name'):
                result_data["name"] = r.prompt_name

            # Include detailed findings if present
            if r.findings:
                result_data["findings"] = [
                    {
                        "severity": f.severity,
                        "category": getattr(f, 'category', 'unknown'),
                        "title": f.title,
                        "description": f.description,
                        "analyzer": getattr(f, 'analyzer', 'unknown'),
                        "recommendation": getattr(f, 'recommendation', None),
                        "location": getattr(f, 'location', None)
                    }
                    for f in r.findings
                ]

            report["results"].append(result_data)

        with open("reports/scan_report_cisco.json", 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Cisco AI Defense scan report saved: reports/scan_report_cisco.json")
        print()

    return 0 if total_findings == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive MCP security scan with Cisco AI Defense API"
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick scan (sample components only)'
    )
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
