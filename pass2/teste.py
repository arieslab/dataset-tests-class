import os
import subprocess

import credentials, request_manager

if __name__ == "__main__":
    # personal Github Account credentials
    git_username, git_access_token = credentials.load("tokens.txt")
    switch_account = 0

    repo = request_manager.requestRaw("https://raw.githubusercontent.com/apach/commons-io/master/src/test/java/org/apache/commons/io/ThreadMonitorTestCase.java")
    if repo == "404: Not Found":
        print("repo vazio")    
    print(repo)