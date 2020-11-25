import os
import subprocess

import credentials, request_manager

if __name__ == "__main__":
    # personal Github Account credentials
    git_username, git_access_token = credentials.load("tokens.txt")
    switch_account = 0

    repo, switch_account = request_manager.request("https://api.github.com/repos/wala/WALA/commits?per_page=1", git_username, git_access_token, switch_account)
    repo_last_commit_message = repo[0]["commit"]["message"]
    if repo == "404: Not Found":
        print("repo vazio")

    print( )