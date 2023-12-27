import os
import pandas as pd
import json
from zipfile import ZipFile
import json
import csv

extracted_folder = './'

# List all JSON files in the extracted folder
json_files = [os.path.join(extracted_folder, file) for file in os.listdir(extracted_folder) if file.endswith('.json')]
print(json_files)

def iterate_json(obj_x, target = [], target_dict={}, result_dict={}, prefix=""):
    idx = 0
    name = ""
    status = ""
    if isinstance(obj_x, list):
        for i in range(len(obj_x)):
            # print('obj_x: is a ', type(obj_x), "iterate it again")
            idx = idx + 1
            iterate_json(obj_x[i], target, target_dict, result_dict, prefix + str(idx) + '.')

    if isinstance(obj_x, dict):
        for key, value in obj_x.items():
            new_prefix = prefix + key
            if isinstance(value, (dict, list)):
                # print('key: ',key, "is a ", type(value), "iterate it again")
                
                iterate_json(value, target, target_dict, result_dict, new_prefix)
            else:
                # print(new_prefix, value)
                if(key in target):
                    target_dict[new_prefix] = value
                if(key == "name"):
                    name = value
                if(key == "status"):
                    status = value
                if(len(name) and len(status)):
                    result_dict[name] = status
                    name = ""
                    status = ""
            


# Initialize an empty list to store JSON data
json_data = []

# Read JSON files and append data to the list
for json_file in json_files:
    with open(json_file) as f:  
        for row in f.readlines(): # 第二步：读取文件内容 
            if row.strip().startswith("//"):   # 第三步：对每一行进行过滤 
                continue
            json_data.append(row)                   # 第四步：将过滤后的行添加到列表中.
    
    json_str = json.loads("\n".join(json_data)) 
    print("json_str data type:%s, len=%d"% (type(json_str), len(json_data)))
    cvs_dict = {}
    simple_dict = {}
    iterate_json(json_str, ["name", "status", "path"], cvs_dict, simple_dict)
    cvs_list = [cvs_dict]
    simple_list = [simple_dict]
    detail_path = 'detail.csv' ## path/name of csv file to save to
    simple_path = 'simple.csv'
    df = pd.DataFrame(cvs_list)
    df = df.T
    df_simple = pd.DataFrame(simple_list).T
    print(df)
    print(df_simple)
    df.to_csv(detail_path, index=1)
    df_simple.to_csv(simple_path, index=1)
    