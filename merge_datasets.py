import pandas as pd
import json

with open('config.json') as json_config_file:
    config = json.load(json_config_file)

saga_df = pd.read_csv(config["saga"]["output"])
oddsat_df = pd.read_csv(config["oddsat"]["output"])

df_list = [saga_df,oddsat_df]

final_df = pd.concat(df_list, axis =0, ignore_index = True)

final_df.to_csv("yle_saga_oddsat_dataset.csv")

print("Done")
