import pandas as pd
import os


def initialize_config(config_file="configHandling.csv"):
    if not os.path.exists(config_file):
        data = {}

        df = pd.DataFrame(data)
        df.to_csv(config_file, index=False)
        print(f"Config file '{config_file}' created with default values.")


def read_config(config_file="configHandling.csv"):
    df = pd.read_csv(config_file)
    config = [df.iat[0, 1], df.iat[1, 1]]
    print(config)

    return config[0], config[1]


def write_config(noise_folder, last_used_folder, config_file="configHandling.csv"):
    print(f"{noise_folder}/{last_used_folder}")
    df = pd.read_csv(config_file)

    if noise_folder is not None:
        df.iat[0, 1] = noise_folder
        df.loc[df['parameter'] == 'noise_folder', 'value'] = str(noise_folder)
    if last_used_folder is not None:
        df.iat[1, 1] = last_used_folder
        df.loc[df['parameter'] == 'last_used_folder', 'value'] = str(last_used_folder)

    df.to_csv(config_file, index=False)
    print(f"Config updated: noise_folder={noise_folder}, last_used_folder={last_used_folder}")

