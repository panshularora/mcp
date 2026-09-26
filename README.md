# mcp: Model Context Protocol experiments

A learning repo for the [Model Context Protocol](https://modelcontextprotocol.io). It holds three small, self-contained examples of MCP servers written with the Python SDK's `FastMCP`, plus clients that talk to them over stdio.

**Status:** learning project (7 commits, 30 Jun – 5 Jul 2026). Everything runs locally. The `test*.py` files are ad-hoc scripts, not a test suite.

| Folder | What it is |
|---|---|
| `mcpbasics/` | First server: arithmetic tools (`add`, `sub`, `mul`, `div`), `greet`, and basic file tools (`read_file`, `write_file`, `delete_file`). The client lists and calls them |
| `FileAssisstant/` | File-assistant server with sandboxed tools (`list_files`, `read_file`, `write_file`, `delete_file`, `create_dir`, `move_file`, `copy_file`, `file_info`). `get_safe_path` keeps every path inside `workspace/`. `client.py` is an interactive stdio client |
| `GithubMCP/` | GitHub server (`list_repos`, `create_repo`, `get_repo`, `get_issues`, `create_new_issue`, `get_pull_requests`, `search_github_code`) over the REST API with `httpx`. Its `client.py` discovers the server's tools, converts them to OpenAI function-calling schemas, and runs an agent loop with `gpt-4o-mini` |

## Run
```bash
# GitHub agent
cd GithubMCP
pip install -r requirements.txt
cp .env.example .env    # then fill in GITHUB_TOKEN and OPENAI_API_KEY
python client.py        # starts server.py over stdio and opens a chat loop

# File assistant
cd FileAssisstant && pip install mcp && python client.py
```
The GitHub tools can **create repositories and issues** with your token, so use a token scoped to a test account or repo.

## What I learned / next steps
- How MCP tool schemas map onto OpenAI function calling.
- Next: add pytest tests with a mocked GitHub API, a confirmation step before write actions, and rename `FileAssisstant` → `FileAssistant`.

## Stack
Python, `mcp` (FastMCP), httpx, OpenAI SDK, python-dotenv.
