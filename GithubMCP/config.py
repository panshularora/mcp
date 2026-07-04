from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Github-MCP-Agent"
}

BASE_URL = "https://api.github.com"