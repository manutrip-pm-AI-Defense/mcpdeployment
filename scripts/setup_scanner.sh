#!/bin/bash

# Setup script for Cisco AI MCP Scanner
# This script helps configure the environment variables for the scanner

echo "==================================="
echo "Cisco AI MCP Scanner Setup"
echo "==================================="
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Backing it up to .env.backup"
    cp .env .env.backup
fi

# Copy example file if .env doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
fi

echo ""
echo "📝 Please provide the following information:"
echo ""

# Prompt for API key
read -p "Enter your Cisco AI Defense API Key (or press Enter to skip): " api_key

if [ -z "$api_key" ]; then
    echo "⚠️  No API key provided. Deep scanning features will not be available."
    echo "   You can still use basic scanning without an API key."
else
    # Ask for endpoint region
    echo ""
    echo "Select your Cisco AI Defense endpoint region:"
    echo "1) US (default) - https://us.api.inspect.aidefense.security.cisco.com/api/v1"
    echo "2) EU - https://eu.api.inspect.aidefense.security.cisco.com/api/v1"
    echo "3) Custom endpoint"
    read -p "Enter choice (1-3) [1]: " endpoint_choice

    endpoint_choice=${endpoint_choice:-1}

    case $endpoint_choice in
        1)
            endpoint="https://us.api.inspect.aidefense.security.cisco.com/api/v1"
            ;;
        2)
            endpoint="https://eu.api.inspect.aidefense.security.cisco.com/api/v1"
            ;;
        3)
            read -p "Enter custom endpoint URL: " endpoint
            ;;
        *)
            echo "Invalid choice. Using US endpoint."
            endpoint="https://us.api.inspect.aidefense.security.cisco.com/api/v1"
            ;;
    esac

    # Update .env file
    if grep -q "MCP_SCANNER_API_KEY=" .env; then
        # Use | as delimiter since URL contains /
        sed -i.bak "s|MCP_SCANNER_API_KEY=.*|MCP_SCANNER_API_KEY=$api_key|" .env
        sed -i.bak "s|MCP_SCANNER_ENDPOINT=.*|MCP_SCANNER_ENDPOINT=$endpoint|" .env
        rm .env.bak
    else
        echo "MCP_SCANNER_API_KEY=$api_key" >> .env
        echo "MCP_SCANNER_ENDPOINT=$endpoint" >> .env
    fi

    echo ""
    echo "✅ Configuration saved to .env file"
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Load environment variables: source .env"
echo "2. Or export them manually:"
echo "   export MCP_SCANNER_API_KEY='your_api_key'"
echo "   export MCP_SCANNER_ENDPOINT='$endpoint'"
echo ""
echo "3. Test the scanner:"
echo "   python -c \"from mcp_scanner import MCPScanner; print('Scanner ready!')\""
echo ""
echo "4. Start your MCP server:"
echo "   uv run mcp-server"
echo ""

if [ -z "$api_key" ]; then
    echo "ℹ️  To get an API key for deep scanning:"
    echo "   1. Visit: https://aidefense.security.cisco.com/"
    echo "   2. Sign up or log in"
    echo "   3. Navigate to API Keys section"
    echo "   4. Generate a new API key"
    echo "   5. Run this script again with your key"
    echo ""
fi
