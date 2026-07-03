from github_api import create_repository

response = create_repository(
    "test",
    "Repository created using MCP",
    False
)

# print(response.status_code)
# print(response.json())
print(response)