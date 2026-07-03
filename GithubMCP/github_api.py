import httpx

from config import BASE_URL, HEADERS


def list_repositories():
    url = f"{BASE_URL}/user/repos"

    response = httpx.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        return response.json()

    repos = response.json()

    return [repo["name"] for repo in repos]


def create_repository(name, description="", private=False):

    url = f"{BASE_URL}/user/repos"

    data = {
        "name": name,
        "description": description,
        "private": private
    }

    response = httpx.post(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code == 201:
        return "Repository created successfully."

    elif response.status_code == 422:
        return "Repository already exists."

    else:
        return response.json()