# filters.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from calc import row_separate

SAMPLE_RATE = 6000


def lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


def highpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)


def apply_filter(data, filter_type, cutoff_low, cutoff_high, fs):
    if filter_type == 'LowPass':
        return lowpass_filter(data, cutoff_low, fs), 0
    elif filter_type == 'HighPass':
        return 0, highpass_filter(data, cutoff_high, fs)
    elif filter_type == 'BandPass':
        return lowpass_filter(data, cutoff_low, fs), highpass_filter(data, cutoff_high, fs)
    else:
        print("Wrong filter type inserted")
        return data


def row_separate(file_path):
 df = pd.read_csv(file_path, sep=',', header=0)
 return df


def means_medians_and_residuals(df, file):
    x_mean = np.mean(df['X (g)'])
    y_mean = np.mean(df['Y (g)'])
    z_mean = np.mean(df['Z (g)'])
    x_median = np.median(df['X (g)'])
    y_median = np.median(df['Y (g)'])
    z_median = np.median(df['Z (g)'])

    removed_bias_mean_x = df['X (g)'] - x_mean
    removed_bias_mean_y = df['Y (g)'] - y_mean
    removed_bias_mean_z = df['Z (g)'] - z_mean

    removed_bias_median_x = df['X (g)'] - x_median
    removed_bias_median_y = df['Y (g)'] - y_median
    removed_bias_median_z = df['Z (g)'] - z_median

    residuals_mean_x = sum(abs(removed_bias_mean_x - 0))
    residuals_mean_y = sum(abs(removed_bias_mean_y - 0))
    residuals_mean_z = sum(abs(removed_bias_mean_z - 0))

    residuals_median_x = sum(abs(removed_bias_median_x - 0))
    residuals_median_y = sum(abs(removed_bias_median_y - 0))
    residuals_median_z = sum(abs(removed_bias_median_z - 0))

    print(f"mean residuals from {file}, X:{residuals_mean_x}, Y:{residuals_mean_y}, Z:{residuals_mean_z}")
    print(f"median residuals from {file}, X:{residuals_median_x}, Y:{residuals_median_y}, Z:{residuals_median_z}")
    return  removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z,removed_bias_median_x, removed_bias_median_y, removed_bias_median_z


def data_reading(file_path, cutoff_low, cutoff_high, DesiredType, noise_path, fs=SAMPLE_RATE):
    for file in os.listdir(file_path):
        if file.endswith('.csv'):
            full_file_path = os.path.join(file_path, file)
            df = row_separate(full_file_path)
            print(df)
            mean_x, mean_y, mean_z, med_x, med_y, med_z = means_medians_and_residuals(df, file)

            mean_x -= mean_x.iloc[0]
            mean_y -= mean_y.iloc[0]
            mean_z -= mean_z.iloc[0]

            filtered_x_lp, filtered_x_hp = apply_filter(mean_x, DesiredType, cutoff_low, cutoff_high, fs)
            filtered_y_lp, filtered_y_hp = apply_filter(mean_y, DesiredType, cutoff_low, cutoff_high, fs)
            filtered_z_lp, filtered_z_hp = apply_filter(mean_z, DesiredType, cutoff_low, cutoff_high, fs)

            end_data_x = np.array(mean_x) - np.array(filtered_x_lp) - np.array(filtered_x_hp)
            end_data_y = np.array(mean_y) - np.array(filtered_y_lp) - np.array(filtered_y_hp)
            end_data_z = np.array(mean_z) - np.array(filtered_z_lp) - np.array(filtered_z_hp)

            signal_plot(df, file_path, file, end_data_x, end_data_y, end_data_z, mean_x, mean_y,
                        mean_z, med_x, med_y, med_z)


def signal_plot(df, main_folder, file_name, filtered_x, filtered_y, filtered_z, mean_x, mean_y, mean_z,
                med_x, med_y, med_z):
    plot_save_path = os.path.join(main_folder, f"{file_name.replace('.csv', '_filtered.jpg')}")

    plt.figure(figsize=(10, 10))
    plt.plot(df['Time (s)'], filtered_x, label='Filtered Accel X', color='black')
    plt.plot(df['Time (s)'], filtered_y, label='Filtered Accel Y', color='red')
    plt.plot(df['Time (s)'], filtered_z, label='Filtered Accel Z', color='blue')
    plt.title(f'Filtered data {file_name}')
    plt.xlabel('Time (с)')
    plt.ylabel('Acceleration (g)')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_save_path)
    plt.close()
