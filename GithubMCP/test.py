from github_api import list_repositories

repos = list_repositories()

print("Your repositories:\n")

for repo in repos:
    print("-", repo)



