from github import Github, BadCredentialsException, UnknownObjectException
import os


def get_repo(access_token, repo_name):
    try:
        github = Github(access_token)
        user = github.get_user()
        repo = user.get_repo(repo_name)
        return repo
    except BadCredentialsException:
        print("Error: Invalid access token. Please check your access token and try again.")
    except UnknownObjectException:
        print(f"Error: Repository '{repo_name}' not found. Please check the repository name and try again.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
        raise