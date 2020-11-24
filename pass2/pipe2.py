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
                    repo, switch_account = request_manager.request("{}{}/{}".format(base_url, line[1], line[2]), git_username, git_access_token, switch_account)
                    
                    if repo != 0:

                        repo_id = int(repo["id"])
                        repo_full_name = repo["full_name"]
                        repo_user, repo_name = repo["full_name"].split("/")
                        repo_description = repo["description"]
                        repo_owner_id = repo["owner"]["id"]
                        repo_default_branch = repo["default_branch"]
                        repo_language = repo["language"]
                        repo_created_at = repo["created_at"]
                        repo_updated_at = repo["updated_at"]
                        repo_pushed_at = repo["pushed_at"]
                        repo_size = repo["size"]
                        repo_stargazers = repo["stargazers_count"]
                        repo_subscribers = repo["subscribers_count"]
                        repo_is_fork = repo["fork"]
                        repo_forks_count = repo["forks_count"]
                        repo_open_issues_count = repo["open_issues_count"]
                        repo_watchers_count = repo["watchers_count"]
                        repo_has_downloads = repo["has_downloads"]
                        repo_has_issues = repo["has_issues"]
                        repo_has_pages = repo["has_pages"]
                        repo_has_wiki = repo["has_wiki"]
                        repo_has_projects = repo["has_projects"]
                        repo_git_url = repo["git_url"]
                        repo_git_clone_url = repo["clone_url"]

                        last_commit_url = "https://api.github.com/repos/{}/{}/commits?per_page=1".format(repo_user, repo_name)
                        last_commit, switch_account = request_manager.request(last_commit_url, git_username, git_access_token, switch_account) 
                        
                        repo_last_commit_sha = last_commit[0]["sha"]
                        repo_last_commit_date = last_commit[0]["commit"]["committer"]["date"]
                        repo_last_commit_message = last_commit[0]["commit"]["message"]
                        repo_last_commit_author = last_commit[0]["commit"]["committer"]["name"]

                        tree_files_commit_url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive=1".format(repo_user, repo_name, repo_last_commit_sha)
                        tree_files_commit, switch_account = request_manager.request(tree_files_commit_url, git_username, git_access_token, switch_account)

                        tests_class_count_project = 0
                        tests_class_junit_3 = 0
                        tests_class_junit_4 = 0
                        tests_class_junit_5 = 0

                        for file in tree_files_commit["tree"]:
                            if file["type"] == "blob":
                                file_name = file["path"].split("/")[-1].lower()
                                if file_name.endswith("test.java") or ( file_name.startswith("test") and file_name.endswith(".java") ):
                                    tests_class_count_project += 1
                                    
                                    test_file_raw_url = "https://raw.githubusercontent.com/{}/{}/{}/{}".format(repo_user, repo_name, repo_last_commit_sha, file["path"])
                                    test_file = request_manager.requestRaw(test_file_raw_url)
                                    
                                    #junit 3 comparator 
                                    if test_file != 1:
                                        if "junit.framework" in test_file:
                                            tests_class_junit_3 +=1
                                        elif "org.junit.Assert" in test_file:
                                            tests_class_junit_4 +=1
                                        elif "org.junit.jupiter" in test_file:
                                            tests_class_junit_5 +=1

                        index += 1
                        data_result.write(str(index) +","+ str(repo_id) +","+ repo_name +","+ repo_full_name +","+" ".join((";".join(str(repo_description).strip().split(","))).split('\n'))+","+
                                        str(repo_owner_id) +","+ repo_default_branch +","+ str(repo_language) +","+ repo_created_at +","+ repo_updated_at+","+
                                        repo_pushed_at+","+str(repo_size)+","+str(repo_stargazers)+","+str(repo_subscribers)+","+str(repo_is_fork)+","+str(repo_forks_count)+","+
                                        str(repo_open_issues_count)+","+str(repo_watchers_count)+","+str(repo_has_downloads)+","+str(repo_has_issues)+","+str(repo_has_pages)+","+
                                        str(repo_has_wiki)+","+str(repo_has_projects)+","+repo_git_url+","+repo_git_clone_url+","+repo_last_commit_sha+","+
                                        repo_last_commit_date+","+" ".join((";".join(str(repo_last_commit_message).strip().split(","))).split('\n'))+","+repo_last_commit_author+","+
                                        str(tests_class_count_project) +","+ str(tests_class_junit_3) +","+ str(tests_class_junit_4) +","+ str(tests_class_junit_5) + '\n')
                        
                        print("{}{}/{}".format(base_url, line[1], line[2]))
             
                    else:
                        index += 1
                        data_result.write(str(index) +",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n")

                elif index == 0 and count == 0:
                        data_result.write("index,repo_id,app,full_name,description,owner_id,default_branch,language,"+
                                          "created_at,updated_at,pushed_at,size,stargazers,subscribers,is_fork,forks_count,"+
                                          "open_issues,watchers,has_downloads,has_issues,has_pages,has_wiki,has_projects,"+ 
                                          "git_url,clone_url,last_commit_sha,last_commit_date,last_commit_massage,last_commit_author,"+
                                          "tests_count,junit3_count,junit4_count,junit5_count"+ "\n")