# AI-Powered GitHub MCP Agent

This folder contains an agentic AI client and an MCP server that integrates with the GitHub REST API.

## File Structure

```
GithubMCP/
├── client.py          # AI agent client (OpenAI Reasoning + Tool calling)
├── server.py          # FastMCP server exposing GitHub tools
├── github_api.py      # GitHub REST API wrapper using httpx
├── config.py          # Dynamic environment configuration
├── .gitignore         # Excludes local environments & secrets (.env)
├── requirements.txt   # Package dependencies
└── README.md          # Documentation
```

## Prerequisites

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Agent

Start the interactive AI Agent by running:
   ```bash
   python client.py
   ```

The client will connect to `server.py` via standard stdio stream, discover all tools automatically, translate them to OpenAI schemas, and run a conversation loop.
