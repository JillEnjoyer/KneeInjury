import pandas as pd


def apply_offsets(file_path, start_offset, end_offset):
    df = pd.read_csv(file_path)

    df['Time (s)'] -= start_offset

    df = df[(df['Time (s)'] >= 0) & (df['Time (s)'] <= (end_offset - start_offset))]

    new_file_name = f"{file_path.replace('.csv', '')}-offstart-{start_offset}-offend-{end_offset}.csv"

    df.to_csv(new_file_name, index=False)
    print(f"File saved as: {new_file_name}")
