import pandas as pd
import os


def initialize_config(config_file="configHandling.csv"):
    if not os.path.exists(config_file):
        # Создаем начальный CSV файл с параметрами
        data = {
        }

        df = pd.DataFrame(data)
        df.to_csv(config_file, index=False)
        print(f"Config file '{config_file}' created with default values.")


def read_config(config_file="configHandling.csv"):
    df = pd.read_csv(config_file)
    config = [df.iat[0, 0], df.iat[1, 0]]
    print(config)

    return config[0], config[1]


def write_config(noise_folder, last_used_folder, config_file="configHandling.csv"):
    # Читаем существующие параметры
    df = pd.read_csv(config_file)

    # Обновляем значения только если переданы новые данные
    if noise_folder is not None:
        df.iat[0, 0] = noise_folder
    if last_used_folder is not None:
        df.iat[1, 0] = last_used_folder

    # Обновляем значения
    df.loc[df['parameter'] == 'noise_folder', 'value'] = str(noise_folder)
    df.loc[df['parameter'] == 'last_used_folder', 'value'] = str(last_used_folder)

    # Сохраняем обратно в CSV файл
    df.to_csv(config_file, index=False)
    print(f"Config updated: noise_folder={noise_folder}, last_used_folder={last_used_folder}")

