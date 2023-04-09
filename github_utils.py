from github import Github
import os


def get_repo(access_token, repo_name):
    github = Github(access_token)
    user = github.get_user()
    repo = user.get_repo(repo_name)
    return repo