import os
import subprocess

import credentials, request_manager

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    # personal Github Account credentials
    git_username, git_access_token = credentials.load("tokens.txt")
    base_url = "https://api.github.com/repos/"

    switch_account = 0

    with open("data_result.csv", "r+") as data_result:

        try:
            index = int(data_result.readlines()[-1].split(',')[0])
        except:
            index = 0
        
        with open("data_source.csv") as data_source:

            for count, line in enumerate(data_source):
                if count != 0 and count == index+1:

                    line = line.split(",")
                    
                    tree_files_commit_url = "https://api.github.com/repos/{}/git/trees/{}?recursive=1".format(line[2], line[24])
                    tree_files_commit, switch_account = request_manager.request(tree_files_commit_url, git_username, git_access_token, switch_account)

                    has_pom = False
                    try:
                        for file in tree_files_commit["tree"]:
                            if file["type"] == "blob":
                                file_name = file["path"].split("/")[-1].lower()
                                if file_name == "pom.xml":
                                    has_pom = True
                        index += 1
                        data_result.write(str(index)+","+",".join(line)[:-1] +","+ str(has_pom)+"\n")
                        print("{}{}/{}".format(base_url, line[1], line[2]))
                    except:
                        index += 1
                    

                elif index == 0 and count == 0:
                        data_result.write("index,repo_id,app,full_name,description,owner_id,default_branch,language,"+
                                          "created_at,updated_at,pushed_at,size,stargazers,subscribers,is_fork,forks_count,"+
                                          "open_issues,watchers,has_downloads,has_issues,has_pages,has_wiki,has_projects,"+ 
                                          "git_url,clone_url,last_commit_sha,last_commit_date,last_commit_massage,last_commit_author,"+
                                          "tests_count,has_junit,is_maven"+ "\n")