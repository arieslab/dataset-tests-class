import os
import subprocess

import credentials, request_manager

if __name__ == "__main__":
    # personal Github Account credentials
    git_username, git_access_token = credentials.load("tokens.txt")
    switch_account = 0

    repo = request_manager.request("https://api.github.com/repos/apache/commons-io", git_username, git_access_token, switch_account)
    if repo == "404: Not Found":
        print("repo vazio")    
    print(repo)