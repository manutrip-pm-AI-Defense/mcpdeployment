# server.py
import json
import os
import requests
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Load environment variables
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

# ============================================================================
# TOOLS - Functions that the AI can execute
# ============================================================================

@mcp.tool()
def format_json(json_string: str, indent: int = 2) -> str:
    """Pretty-print a JSON string

    Args:
        json_string: A JSON string to format
        indent: Number of spaces for indentation (default: 2)

    Returns:
        Formatted JSON string

    Raises:
        ValueError: If the input is not valid JSON
    """
    try:
        data = json.loads(json_string)
        return json.dumps(data, indent=indent, sort_keys=True)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")


@mcp.tool()
def get_news(country: str = "us", category: str = "", language: str = "en", max_results: int = 10) -> str:
    """Fetch latest news articles from NewsData.io API

    Args:
        country: Country code (e.g., "us", "gb", "in"). Default: "us"
        category: News category (e.g., "business", "technology", "sports", "health"). Default: all categories
        language: Language code (e.g., "en", "es", "fr"). Default: "en"
        max_results: Maximum number of articles to return (1-10). Default: 10

    Returns:
        JSON string containing news articles with title, description, link, and publish date

    Raises:
        ValueError: If API key is not configured or request fails

    Note:
        Requires NEWSDATA_API_KEY environment variable to be set.
        Get your free API key from: https://newsdata.io/
    """
    if not NEWSDATA_API_KEY:
        raise ValueError(
            "NewsData API key not configured. "
            "Set NEWSDATA_API_KEY environment variable. "
            "Get your free key from: https://newsdata.io/"
        )

    try:
        # Build API URL with parameters
        url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_API_KEY}&language={language}"

        if country:
            url += f"&country={country}"

        if category:
            url += f"&category={category}"

        # Make API request
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check for API errors
        if data.get("status") == "error":
            raise ValueError(f"API error: {data.get('results', {}).get('message', 'Unknown error')}")

        # Extract and format articles
        articles = data.get("results", [])[:max_results]

        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description"),
                "link": article.get("link", ""),
                "pubDate": article.get("pubDate", ""),
                "source": article.get("source_id", "Unknown"),
                "category": article.get("category", [])
            })

        result = {
            "status": "success",
            "totalResults": len(formatted_articles),
            "articles": formatted_articles
        }

        return json.dumps(result, indent=2)

    except requests.exceptions.Timeout:
        raise ValueError("Request timeout - NewsData API did not respond in time")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch news: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing news data: {str(e)}")


# ============================================================================
# RESOURCES - Read-only data that the AI can access
# ============================================================================

@mcp.resource("demo://info")
def get_server_info() -> str:
    """Get basic server information"""
    info = {
        "name": "Demo MCP Server",
        "version": "1.0.0",
        "description": "A demonstration MCP server with Tools, Resources, and Prompts",
        "capabilities": {
            "tools": ["format_json", "get_news"],
            "resources": ["demo://info", "demo://file/data"],
            "prompts": ["code_review", "summarize", "debug_helper"]
        },
        "integrations": {
            "newsdata_configured": bool(NEWSDATA_API_KEY)
        }
    }
    return json.dumps(info, indent=2)


@mcp.resource("demo://file/data")
def read_sample_data() -> str:
    """Read data from the sample data file

    Demonstrates how MCP resources can expose file system data to AI assistants.
    This allows the AI to access structured data without needing direct file system access.
    """
    import os

    # Get the project root directory (parent of src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_file = os.path.join(project_root, "data", "sample_data.json")

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)

        # Return the data as a formatted JSON string
        return json.dumps(data, indent=2)
    except FileNotFoundError:
        return json.dumps({
            "error": "Data file not found",
            "expected_path": data_file,
            "message": "Create data/sample_data.json in the project root"
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to read data file",
            "message": str(e)
        }, indent=2)


# ============================================================================
# PROMPTS - Reusable prompt templates
# ============================================================================

@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt

    Args:
        code: The code to review
        language: Programming language (default: python)

    Returns:
        A formatted prompt for code review
    """
    return f"""Please review the following {language} code for:
- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security concerns
- Readability and maintainability

Code to review:
```{language}
{code}
```

Please provide constructive feedback with specific suggestions for improvement."""


@mcp.prompt()
def summarize(text: str, max_words: int = 100) -> str:
    """Generate a text summarization prompt

    Args:
        text: The text to summarize
        max_words: Maximum words in summary (default: 100)

    Returns:
        A formatted prompt for summarization
    """
    return f"""Please summarize the following text in {max_words} words or less.
Focus on the key points and main ideas.

Text to summarize:
{text}

Summary:"""


@mcp.prompt()
def debug_helper(error_message: str, context: str = "") -> str:
    """Generate a debugging assistance prompt

    Args:
        error_message: The error message encountered
        context: Additional context about the error (optional)

    Returns:
        A formatted prompt for debugging help
    """
    prompt = f"""I encountered the following error and need help debugging it:

Error Message:
{error_message}
"""

    if context:
        prompt += f"""
Context:
{context}
"""

    prompt += """
Please help me:
1. Understand what caused this error
2. Identify potential solutions
3. Suggest best practices to avoid this in the future
"""

    return prompt