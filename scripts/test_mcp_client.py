#!/usr/bin/env python3
"""
Simple MCP client to test the HTTP server.

This script connects to the MCP HTTP server and lists available capabilities.
"""
import asyncio
import sys
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def test_mcp_server(host: str = "127.0.0.1", port: int = 8000):
    """Test MCP server by connecting and listing capabilities."""
    server_url = f"http://{host}:{port}"

    print(f"🔗 Connecting to MCP server at {server_url}")
    print("=" * 60)

    try:
        # Connect using streamable-http client
        async with streamable_http_client(server_url) as (read, write, _get_session_id):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                print("✅ Connected successfully!")
                print()

                # List available tools
                print("🛠️  Available Tools:")
                tools_result = await session.list_tools()
                for tool in tools_result.tools:
                    print(f"  • {tool.name}: {tool.description}")
                print(f"  Total: {len(tools_result.tools)} tools")
                print()

                # List available resources
                print("📚 Available Resources:")
                resources_result = await session.list_resources()
                for resource in resources_result.resources:
                    print(f"  • {resource.uri}: {resource.name}")
                print(f"  Total: {len(resources_result.resources)} resources")
                print()

                # List available prompts
                print("💬 Available Prompts:")
                prompts_result = await session.list_prompts()
                for prompt in prompts_result.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")
                print(f"  Total: {len(prompts_result.prompts)} prompts")
                print()

                print("=" * 60)
                print("✅ All tests passed! Server is working correctly.")

    except httpx.ConnectError:
        print(f"❌ Error: Could not connect to {server_url}")
        print()
        print("Make sure the server is running:")
        print(f"  MCP_REMOTE_HOST={host} MCP_REMOTE_PORT={port} uv run mcp-server-remote")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def test_tool_call(host: str = "127.0.0.1", port: int = 8000):
    """Test calling a tool on the MCP server."""
    server_url = f"http://{host}:{port}"

    print(f"\n🧪 Testing tool call...")
    print("=" * 60)

    try:
        async with streamable_http_client(server_url) as (read, write, _get_session_id):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Call the 'add' tool
                print("Calling tool: add(5, 3)")
                result = await session.call_tool("add", arguments={"a": 5, "b": 3})
                print(f"Result: {result.content}")
                print()

                # Call the 'reverse_text' tool
                print("Calling tool: reverse_text('Hello, MCP!')")
                result = await session.call_tool("reverse_text", arguments={"text": "Hello, MCP!"})
                print(f"Result: {result.content}")
                print()

                print("✅ Tool calls successful!")

    except Exception as e:
        print(f"❌ Tool call failed: {e}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Test MCP HTTP server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--test-tools", action="store_true", help="Test tool calls")

    args = parser.parse_args()

    # Run the test
    asyncio.run(test_mcp_server(args.host, args.port))

    if args.test_tools:
        asyncio.run(test_tool_call(args.host, args.port))


if __name__ == "__main__":
    main()
