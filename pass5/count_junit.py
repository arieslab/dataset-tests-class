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

                    tests_class_count_project = 0
                    tests_class_junit_3 = 0
                    tests_class_junit_4 = 0
                    tests_class_junit_5 = 0
                    print(tree_files_commit_url)
                    for file in tree_files_commit["tree"]:
                        if file["type"] == "blob":
                            file_name = file["path"].split("/")[-1].lower()
                            if file_name.endswith("test.java") or ( file_name.startswith("test") and file_name.endswith(".java") ):
                                tests_class_count_project += 1
                                
                                test_file_raw_url = "https://raw.githubusercontent.com/{}/{}/{}".format(line[2], line[24], file["path"])
                                test_file = request_manager.requestRaw(test_file_raw_url)
                                
                                #junit 3 comparator 
                                if test_file != 1:
                                    if "junit.framework" in test_file:
                                        tests_class_junit_3 +=1
                                    elif "org.junit.Assert" in test_file:
                                        tests_class_junit_4 +=1
                                    elif "org.junit.jupiter" in test_file:
                                        tests_class_junit_5 +=1
                    total = tests_class_junit_3+tests_class_junit_4+tests_class_junit_5
                    index += 1
                    data_result.write(str(index)+","+",".join(line)[:-2] +","+ str(tests_class_junit_3)+","+str(tests_class_junit_4)+","+str(tests_class_junit_5)+","+ str(total)+"\n")
                    
                    print("{}{}/{}".format(base_url, line[1], line[2]))

                elif index == 0 and count == 0:
                        data_result.write("index,repo_id,app,full_name,description,owner_id,default_branch,language,"+
                                          "created_at,updated_at,pushed_at,size,stargazers,subscribers,is_fork,forks_count,"+
                                          "open_issues,watchers,has_downloads,has_issues,has_pages,has_wiki,has_projects,"+ 
                                          "git_url,clone_url,last_commit_sha,last_commit_date,last_commit_massage,last_commit_author,"+
                                          "tests_count,has_junit,is_maven,classification,junit3_count,junit4_count,junit5_count,junit_count"+ "\n")