import pandas as pd


def apply_offsets(file_path, start_offset, end_offset):
    df = pd.read_csv(file_path)
    original_end_time = df['Time (s)'].max()

    df['Time (s)'] = df['Time (s)'] - start_offset
    df = df[df['Time (s)'] <= original_end_time - end_offset]

    new_file_name = file_path.replace('.csv', f'-offstart-{start_offset}-offend-{end_offset}.csv')
    df.to_csv(new_file_name, index=False)
    print(f"File saved as: {new_file_name}")