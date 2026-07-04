from mcp.server.fastmcp import FastMCP

from github_api import (
    list_repositories,
    create_repository,
    get_repository,
    list_issues,
    create_issue,
    list_prs,
    search_code
)

mcp = FastMCP("Github MCP")


@mcp.tool()
def list_repos():
    """List all GitHub repositories of the authenticated user."""
    return list_repositories()


@mcp.tool()
def create_repo(name: str, description: str = "", private: bool = False):
    """Create a new GitHub repository for the authenticated user."""
    return create_repository(name, description, private)


@mcp.tool()
def get_repo(owner: str, repo: str):
    """Get information and metadata about a specific GitHub repository."""
    return get_repository(owner, repo)


@mcp.tool()
def get_issues(owner: str, repo: str, state: str = "open"):
    """List issues in a repository (excluding pull requests). State can be 'open', 'closed', or 'all'."""
    return list_issues(owner, repo, state)


@mcp.tool()
def create_new_issue(owner: str, repo: str, title: str, body: str = ""):
    """Create a new issue in a specific GitHub repository."""
    return create_issue(owner, repo, title, body)


@mcp.tool()
def get_pull_requests(owner: str, repo: str, state: str = "open"):
    """List pull requests in a repository. State can be 'open', 'closed', or 'all'."""
    return list_prs(owner, repo, state)


@mcp.tool()
def search_github_code(query: str):
    """Search code across public and private GitHub repositories. Query format can contain qualifiers like 'repo:owner/repo'."""
    return search_code(query)


if __name__ == "__main__":
    mcp.run()