from mcp.server.fastmcp import FastMCP

from github_api import list_repositories
from github_api import create_repository


mcp = FastMCP("Github MCP")

@mcp.tool()
def list_repos():
    """List all GitHub repositories."""
    return list_repositories()


@mcp.tool()
def create_repo(
    name: str,
    description: str = "",
    private: bool = False
):
    """Create a new GitHub repository."""
    return create_repository(
        name,
        description,
        private
    )


if __name__ == "__main__":
    mcp.run()