import os
from dotenv import load_dotenv
import requests

# Загрузка переменных окружения
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')


def create_repo():
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    data = {
        "name": REPO_NAME,
        "description": f"Test repo created by {REPO_NAME}",
        "public": True
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code == 201


def get_repos():
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    repos = response.json()

    return REPO_NAME in [repo['name'] for repo in repos]


def delete_repo():
    url = f"https://api.github.com/repos/{os.getenv('GITHUB_USERNAME')}/{REPO_NAME}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.delete(url, headers=headers)

    return response.status_code == 204


if __name__ == "__main__":
    print("Creating repository...")
    repo_created = create_repo()

    if repo_created:
        print(f"Repository '{REPO_NAME}' created successfully.")

        print("Checking if repository exists...")
        repo_exists = get_repos()
        if repo_exists:
            print(f"Repository '{REPO_NAME}' found in the list of repositories.")

            print("Deleting repository...")
            delete_repo()
            print(f"Repository '{REPO_NAME}' deleted successfully.")
        else:
            print(f"Error: Repository '{REPO_NAME}' not found.")
    else:
        print(f"Error: Failed to create repository '{REPO_NAME}'.")

