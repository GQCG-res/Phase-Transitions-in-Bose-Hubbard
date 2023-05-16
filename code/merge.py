import pandas as pd
import glob
import os
import json

def fromList(col):
    return col[0]

def merge(name, directory):

    total_df = pd.DataFrame()
    path = './MPS_groundstate/data/' + directory

    json_pattern = os.path.join(path, '*.json')
    file_list = glob.glob(json_pattern)

    for file in file_list:
        with open(file) as json_file:
            data = json.load(json_file)
            data = {k:[v] for k,v in data.items()}  # WORKAROUND
            print(data)
        total_df = pd.concat([total_df, pd.DataFrame([data])], ignore_index=True)

    total_df = total_df.sort_values(['t_val'], ascending=[True])
    total_df = total_df.reset_index(drop=True)

    total_df["particles"] = total_df.apply(lambda row: fromList(row["particles"]), axis=1)
    total_df["energy"] = total_df.apply(lambda row: fromList(row["energy"]), axis=1)
    total_df["t_val"] = total_df.apply(lambda row: fromList(row["t_val"]), axis=1)
    
    total_df.to_json(name, orient="columns")


    print(total_df)

merge("./mott-lobe-3-E0.json", "Mott-Lobe-2-E0")
merge("./mott-lobe-3-Ep1.json", "Mott-Lobe-2-Ep1")
merge("./mott-lobe-3-Em1.json", "Mott-Lobe-2-Em1")
