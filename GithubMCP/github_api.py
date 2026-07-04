import httpx

from config import BASE_URL, HEADERS


def list_repositories():
    """List repositories for the authenticated user."""
    url = f"{BASE_URL}/user/repos"
    response = httpx.get(url, headers=HEADERS)

    if response.status_code != 200:
        return response.json()

    repos = response.json()
    return [repo["name"] for repo in repos]


def create_repository(name: str, description: str = "", private: bool = False):
    """Create a new repository for the authenticated user."""
    url = f"{BASE_URL}/user/repos"
    data = {
        "name": name,
        "description": description,
        "private": private
    }
    response = httpx.post(url, headers=HEADERS, json=data)

    if response.status_code == 201:
        return "Repository created successfully."
    elif response.status_code == 422:
        return "Repository already exists."
    else:
        return response.json()


def get_repository(owner: str, repo: str):
    """Get details for a specific repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}"
    response = httpx.get(url, headers=HEADERS)

    if response.status_code == 200:
        repo_data = response.json()
        return {
            "name": repo_data.get("name"),
            "full_name": repo_data.get("full_name"),
            "description": repo_data.get("description"),
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "open_issues": repo_data.get("open_issues_count"),
            "url": repo_data.get("html_url")
        }
    else:
        return f"Error: {response.status_code} - {response.text}"


def list_issues(owner: str, repo: str, state: str = "open"):
    """List issues in a repository (excluding pull requests)."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    params = {"state": state, "per_page": 10}
    response = httpx.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        issues = response.json()
        items = []
        for issue in issues:
            # GitHub API returns pull requests in the issues endpoint; filter them out
            if "pull_request" not in issue:
                items.append({
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "user": issue.get("user", {}).get("login"),
                    "url": issue.get("html_url")
                })
        return items
    else:
        return f"Error: {response.status_code} - {response.text}"


def create_issue(owner: str, repo: str, title: str, body: str = ""):
    """Create a new issue in a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    data = {"title": title, "body": body}
    response = httpx.post(url, headers=HEADERS, json=data)

    if response.status_code == 201:
        issue_data = response.json()
        return f"Issue #{issue_data.get('number')} created successfully: {issue_data.get('html_url')}"
    else:
        return f"Error: {response.status_code} - {response.text}"


def list_prs(owner: str, repo: str, state: str = "open"):
    """List pull requests in a repository."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": state, "per_page": 10}
    response = httpx.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        prs = response.json()
        items = []
        for pr in prs:
            items.append({
                "number": pr.get("number"),
                "title": pr.get("title"),
                "state": pr.get("state"),
                "user": pr.get("user", {}).get("login"),
                "url": pr.get("html_url")
            })
        return items
    else:
        return f"Error: {response.status_code} - {response.text}"


def search_code(query: str):
    """Search code across GitHub repositories."""
    url = f"{BASE_URL}/search/code"
    params = {"q": query, "per_page": 5}
    response = httpx.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        results = response.json()
        items = []
        for item in results.get("items", []):
            items.append({
                "name": item.get("name"),
                "path": item.get("path"),
                "repository": item.get("repository", {}).get("full_name"),
                "url": item.get("html_url")
            })
        return items
    else:
        return f"Error: {response.status_code} - {response.text}"