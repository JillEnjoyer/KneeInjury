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
    if filter_type == 'lowpass':
        return lowpass_filter(data, cutoff_low, fs)
    elif filter_type == 'highpass':
        return highpass_filter(data, cutoff_high, fs)
    elif filter_type == 'bandpass':
        return highpass_filter(lowpass_filter(data, cutoff_low, fs), cutoff_high, fs)
    else:
        print("Неправильный тип фильтра")
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


# Функция для чтения данных из файлов и их фильтрации
def data_reading(file_path, cutoff_low, cutoff_high, DesiredType, fs=SAMPLE_RATE):
    for file in os.listdir(file_path):
        if file.endswith('.csv'):
            full_file_path = os.path.join(file_path, file)
            df = row_separate(full_file_path)
            mean_x, mean_y, mean_z, med_x, med_y, med_z = means_medians_and_residuals(df, file)

            mean_x -= mean_x.iloc[0]
            mean_y -= mean_y.iloc[0]
            mean_z -= mean_z.iloc[0]

            filtered_x = apply_filter(mean_x, 'bandpass', cutoff_low, cutoff_high, fs)
            filtered_y = apply_filter(mean_y, 'bandpass', cutoff_low, cutoff_high, fs)
            filtered_z = apply_filter(mean_z, 'bandpass', cutoff_low, cutoff_high, fs)

            signal_plot(df, file_path, file, filtered_x, filtered_y, filtered_z, mean_x, mean_y,
                        mean_z, med_x, med_y, med_z)


# Функция для построения и сохранения графиков
def signal_plot(df, main_folder, file_name, filtered_x, filtered_y, filtered_z, mean_x, mean_y, mean_z,
                med_x, med_y, med_z):
    plot_save_path = os.path.join(main_folder, f"{file_name.replace('.csv', '_filtered.jpg')}")

    plt.figure(figsize=(10, 10))
    plt.plot(df['Time (s)'], filtered_x, label='Фильтрованный Accel X', color='black')
    plt.plot(df['Time (s)'], filtered_y, label='Фильтрованный Accel Y', color='red')
    plt.plot(df['Time (s)'], filtered_z, label='Фильтрованный Accel Z', color='blue')
    plt.title(f'Фильтрованные данные {file_name}')
    plt.xlabel('Время (с)')
    plt.ylabel('Ускорение (g)')
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_save_path)
    plt.close()


# Вспомогательные функции для RMS и SNR
def rms(data):
    return np.sqrt(np.mean(data ** 2))


def snr(signal, noise_rms):
    signal_rms = rms(signal)
    return 10 * np.log10((signal_rms ** 2) / (noise_rms ** 2)) if noise_rms != 0 else float('inf')
