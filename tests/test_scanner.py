#!/usr/bin/env python3
"""
Test script for Cisco AI MCP Scanner integration
Run this to verify your scanner setup is working correctly
"""

import os
import sys

def test_import():
    """Test if the scanner package is installed"""
    print("Testing scanner import...")
    try:
        import mcpscanner
        version = getattr(mcpscanner, '__version__', 'Unknown')
        print(f"✅ Scanner package imported successfully (version {version})")
        return True
    except ImportError as e:
        print(f"❌ Failed to import scanner: {e}")
        print("   Run: uv add cisco-ai-mcp-scanner")
        return False

def test_environment():
    """Test if environment variables are configured"""
    print("\nTesting environment variables...")

    api_key = os.getenv("MCP_SCANNER_API_KEY")
    endpoint = os.getenv("MCP_SCANNER_ENDPOINT")

    if api_key:
        print(f"✅ MCP_SCANNER_API_KEY is set (first 10 chars: {api_key[:10]}...)")
    else:
        print("⚠️  MCP_SCANNER_API_KEY is not set")
        print("   Basic scanning will work, but deep scanning requires an API key")
        print("   Get your key from: https://aidefense.security.cisco.com/")

    if endpoint:
        print(f"✅ MCP_SCANNER_ENDPOINT is set: {endpoint}")
    else:
        print("ℹ️  MCP_SCANNER_ENDPOINT not set (will use default)")

    return bool(api_key)

def test_scanner_init():
    """Test if scanner can be initialized"""
    print("\nTesting scanner initialization...")

    try:
        from mcpscanner import Scanner
        from mcpscanner.config import Config

        api_key = os.getenv("MCP_SCANNER_API_KEY")
        endpoint = os.getenv("MCP_SCANNER_ENDPOINT",
                           "https://us.api.inspect.aidefense.security.cisco.com/api/v1")

        config = Config()
        if api_key:
            config.api_key = api_key
            config.api_endpoint = endpoint
            print("✅ Scanner config initialized with API credentials")
        else:
            print("✅ Scanner config initialized (basic mode, no API key)")

        # Test creating a scanner instance
        scanner = Scanner(config=config)
        print("✅ Scanner instance created successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to initialize scanner: {e}")
        return False

def test_mcp_server():
    """Test if MCP server can import scanner tools"""
    print("\nTesting MCP server integration...")

    try:
        # Try importing the server module
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        from mcpserver import server

        # Check if scanner tools are available
        if hasattr(server, 'scan_mcp_server') and hasattr(server, 'check_scanner_status'):
            print("✅ Scanner tools are integrated in MCP server")
            print("   - scan_mcp_server")
            print("   - check_scanner_status")
            return True
        else:
            print("⚠️  Scanner tools not found in MCP server")
            return False

    except Exception as e:
        print(f"❌ Failed to test MCP server integration: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Cisco AI MCP Scanner - Setup Verification")
    print("=" * 60)
    print()

    results = []

    # Run tests
    results.append(("Package Import", test_import()))
    results.append(("Environment Config", test_environment()))
    results.append(("Scanner Init", test_scanner_init()))
    results.append(("MCP Server Integration", test_mcp_server()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")

    print()

    # Overall result
    all_passed = all(result[1] for result in results)

    if all_passed:
        print("🎉 All tests passed! Scanner is ready to use.")
        print()
        print("Next steps:")
        print("1. Start your MCP server: uv run mcp-server")
        print("2. Test scanning via your MCP client")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        print()
        print("Common fixes:")
        print("- Install scanner: uv add cisco-ai-mcp-scanner")
        print("- Set API key: export MCP_SCANNER_API_KEY='your_key'")
        print("- Run setup script: ./scripts/setup_scanner.sh")
        print()
        print("For detailed instructions, see: SCANNER_SETUP.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
