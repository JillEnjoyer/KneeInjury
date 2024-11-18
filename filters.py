import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from calc import row_separate

SAMPLE_RATE = 6000

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    return filtfilt(b, a, data)

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (0.5 * fs), btype='high')
    return filtfilt(b, a, data)

def apply_filter(data, filter_type, cutoff_low, cutoff_high, fs):
    filters = {
        'LowPass': (lowpass_filter(data, cutoff_low, fs), 0),
        'HighPass': (0, highpass_filter(data, cutoff_high, fs)),
        'BandPass': (lowpass_filter(data, cutoff_low, fs), highpass_filter(data, cutoff_high, fs))
    }
    return filters.get(filter_type, (data, data))

def means_medians_and_residuals(df, file):
    x_mean, y_mean, z_mean = df[['X (g)', 'Y (g)', 'Z (g)']].mean()
    x_median, y_median, z_median = df[['X (g)', 'Y (g)', 'Z (g)']].median()
    removed_bias_mean = df[['X (g)', 'Y (g)', 'Z (g)']] - [x_mean, y_mean, z_mean]
    removed_bias_median = df[['X (g)', 'Y (g)', 'Z (g)']] - [x_median, y_median, z_median]
    residuals_mean = removed_bias_mean.abs().sum().tolist()
    residuals_median = removed_bias_median.abs().sum().tolist()
    print(f"mean residuals from {file}, X:{residuals_mean[0]}, Y:{residuals_mean[1]}, Z:{residuals_mean[2]}")
    print(f"median residuals from {file}, X:{residuals_median[0]}, Y:{residuals_median[1]}, Z:{residuals_median[2]}")
    return removed_bias_mean.values.T.tolist() + removed_bias_median.values.T.tolist()


def data_reading(file_path, cutoff_low, cutoff_high, DesiredType, noise_path, fs=SAMPLE_RATE):
    files_to_process = [file_path] if os.path.isfile(file_path) else [
        os.path.join(file_path, file) for file in os.listdir(file_path) if file.endswith('.csv')
    ]
    for full_file_path in files_to_process:
        df = row_separate(full_file_path)
        mean_x, mean_y, mean_z, med_x, med_y, med_z = means_medians_and_residuals(df, full_file_path)

        mean_x, mean_y, mean_z = [np.array(x) - x[0] for x in [mean_x, mean_y, mean_z]]

        filtered_x_lp, filtered_x_hp = apply_filter(mean_x, DesiredType, cutoff_low, cutoff_high, fs)
        filtered_y_lp, filtered_y_hp = apply_filter(mean_y, DesiredType, cutoff_low, cutoff_high, fs)
        filtered_z_lp, filtered_z_hp = apply_filter(mean_z, DesiredType, cutoff_low, cutoff_high, fs)

        end_data_x = mean_x - filtered_x_lp - filtered_x_hp
        end_data_y = mean_y - filtered_y_lp - filtered_y_hp
        end_data_z = mean_z - filtered_z_lp - filtered_z_hp

        signal_plot(
            df, file_path, os.path.basename(full_file_path),
            end_data_x, end_data_y, end_data_z, mean_x, mean_y, mean_z,
            med_x, med_y, med_z
        )


def signal_plot(df, main_folder, file_name, filtered_x, filtered_y, filtered_z, mean_x, mean_y, mean_z, med_x, med_y,
                med_z):
    plot_save_path = os.path.join(main_folder, f"{file_name.replace('.csv', '_filtered.jpg')}")
    os.makedirs(main_folder, exist_ok=True)

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
    print(f"Plot saved: {plot_save_path}")
