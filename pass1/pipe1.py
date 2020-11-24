data_source = open("data_source.csv")

data_result = open("data_result.csv", 'w')

data_result.write("repo_id,user,repo,commit,commit_date,#tests,size,LOC\n")
for line in data_source:
    line = line.split(",")
    if line[3] == "-":
        data_result.write(','.join(line[:3]) + ',' + ','.join(line[4:]))

data_source.close()
data_result.close()