with open("data_result.csv", "r+") as data_result:

        try:
            index = int(data_result.readlines()[-1].split(',')[0])
        except:
            index = 0
        
        with open("data_source.csv") as data_source:

            for count, line in enumerate(data_source):
                    if(not line.endswith(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n")):
                        arr_line = line.split(",");
                        arr_line = ",".join(arr_line[1:]);
                        arr_line = arr_line.replace('"', " '")
                        data_result.write(arr_line)