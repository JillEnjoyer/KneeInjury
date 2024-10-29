import os

import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt, periodogram
import pandas as pd
import matplotlib.pyplot as plt
import math

main_folder = 'D:\\Data'  #советую потом поменять
# эта часть в случае если в файле все в одном толбце
FS = 6000  # sampling frequency in Hz
FLP = 10   # low pass filter passband frequency in Hz
FHP = 1000 # high pass filter passband frequency in Hz
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

    removed_bias_median_x=df['X (g)'] - x_median
    removed_bias_median_y=df['Y (g)'] - y_median
    removed_bias_median_z=df['Z (g)'] - z_median

    residuals_mean_x = sum(abs(removed_bias_mean_x - 0))
    residuals_mean_y = sum(abs(removed_bias_mean_y - 0))
    residuals_mean_z = sum(abs(removed_bias_mean_z - 0))

    residuals_median_x= sum(abs(removed_bias_median_x - 0))
    residuals_median_y= sum(abs(removed_bias_median_y - 0))
    residuals_median_z= sum(abs(removed_bias_median_z - 0))

    print(f"mean residuals from {file}, X:{residuals_mean_x}, Y:{residuals_mean_y}, Z:{residuals_mean_z}")
    print(f"median residuals from {file}, X:{residuals_median_x}, Y:{residuals_median_y}, Z:{residuals_median_z}")
    return  removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z,removed_bias_median_x, removed_bias_median_y, removed_bias_median_z

#Low-pass
def lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

#Hgh-pass
def highpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y


def datas_reading(main_folder, subfolder, cutoff = FLP, cutoff_high = FHP, sample_rate = FS):
    csv_folder_path = os.path.join(main_folder, subfolder, 'CSV')

    for file in os.listdir(csv_folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(csv_folder_path, file)
            df = row_separate(file_path)
            removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z,removed_bias_median_x, removed_bias_median_y, removed_bias_median_z = means_medians_and_residuals(df, file)
            print(removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z,removed_bias_median_x, removed_bias_median_y, removed_bias_median_z)
            removed_bias_mean_x = removed_bias_mean_x - removed_bias_mean_x.iloc[0]
            removed_bias_mean_y = removed_bias_mean_y - removed_bias_mean_y.iloc[0]
            removed_bias_mean_z = removed_bias_mean_z - removed_bias_mean_z.iloc[0]

            filtered_x = lowpass_filter(removed_bias_mean_x, cutoff, sample_rate)
            filtered_y = lowpass_filter(removed_bias_mean_y, cutoff, sample_rate)
            filtered_z = lowpass_filter(removed_bias_mean_z, cutoff, sample_rate)

            #filtered_x_high = highpass_filter(removed_bias_mean_x, cutoff_high, sample_rate)
            #filtered_y_high = highpass_filter(removed_bias_mean_y, cutoff_high, sample_rate)
            #filtered_z_high = highpass_filter(removed_bias_mean_z, cutoff_high, sample_rate)

            signal_plot(df, main_folder, subfolder, file, filtered_x, filtered_y, filtered_z, removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z, removed_bias_median_x, removed_bias_median_y, removed_bias_median_z)

def rms(data):
    length = len(data)
    rms_value = math.sqrt((sum(data**2))/length)
    return rms_value


def snr(signal, noise_rms):
    signal_rms = rms(signal)
    if noise_rms == 0:
        return float('inf')
    return 10 * np.log10((signal_rms ** 2) / (noise_rms ** 2))

def subA ():
    A = os.path.join(main_folder, 'A')
    datas_reading(A, 'Left')
    datas_reading(A, 'Right')

def subB ():
    B = os.path.join(main_folder, 'B')
    datas_reading(B, 'Left')
    datas_reading(B, 'Right')

def subC ():
    C = os.path.join(main_folder, 'C')
    datas_reading(C, 'Left')
    datas_reading(C, 'Right')

def signal_plot(df, main_folder, subfolder, file_name, filtered_x, filtered_y, filtered_z, removed_bias_mean_x, removed_bias_mean_y, removed_bias_mean_z, removed_bias_median_x, removed_bias_median_y, removed_bias_median_z):
#time(s), accelX (g), accelY (g), accelZ (g) where 1 g = 9.81 m/s^2
    data_path = os.path.join(main_folder, subfolder, 'CSV', file_name)
    df = pd.read_csv(data_path)
    if 'Left' in subfolder:
        knee = 'Left'
    else:
        knee = 'Right'

    x_rms = rms(removed_bias_mean_x)
    y_rms = rms(removed_bias_mean_y)
    z_rms = rms(removed_bias_mean_z)
    x_rms_median = rms(removed_bias_median_x)
    y_rms_median = rms(removed_bias_median_y)
    z_rms_median = rms(removed_bias_median_z)

    x_noise = df['X (g)'] - filtered_x
    y_noise = df['Y (g)'] - filtered_y
    z_noise = df['Z (g)'] - filtered_z

   # x_snr = snr(filtered_x, x_noise)
    #y_snr = snr(filtered_y, y_noise)
   # z_snr = snr(filtered_z, z_noise)
    x_snr = snr(filtered_x, rms(x_noise))
    y_snr = snr(filtered_y, rms(y_noise))
    z_snr = snr(filtered_z, rms(z_noise))
    print(f"datas from {file_name}")
    print(f"X SNR: {x_snr}")
    print(f"Y SNR: {y_snr}")
    print(f"Z SNR: {z_snr}")
    print(f"X RMS: {x_rms}")
    print(f"X RMS Median: {x_rms_median}")
    print(f"Y RMS: {y_rms}")
    print(f"Y RMS Median: {y_rms_median}")
    print(f"Z RMS: {z_rms_median}")
    print(f"Z RMS Median: {z_rms_median}")

    plt.figure(figsize=(10, 10))
    plt.plot(df['Time (s)'], df['X (g)'], label='Accel X', color='black')
    plt.plot(df['Time (s)'], df['Y (g)'], label='Accel Y', color='red')
    plt.plot(df['Time (s)'], df['Z (g)'], label='Accel Z', color='blue')
    plt.title(f'Subject {os.path.basename(main_folder)}, {knee} knee')
    plt.xlabel('Time(s)')
    plt.ylabel('Accel Mag(g)')
    plt.legend()
    plt.grid(True)

    save = os.path.join(main_folder, subfolder, 'CSV', f"{file_name.replace('.csv', '.jpg')}")
    plt.savefig(save)
    plt.close()


    plt.figure(figsize=(10, 10))
    plt.plot(df['Time (s)'], removed_bias_mean_x , label='Accel X', color='black')
    plt.plot(df['Time (s)'], removed_bias_mean_y , label='Accel Y', color='red')
    plt.plot(df['Time (s)'], removed_bias_mean_z , label='Accel Z', color='blue')
    plt.title(f'Subject {os.path.basename(main_folder)}, {knee} knee')
    plt.xlabel('Time(s)')
    plt.ylabel('Accel Mag(g)')
    plt.legend()
    plt.grid(True)

    save = os.path.join(main_folder, subfolder, 'CSV', f"{file_name.replace('.csv', '_removed bias.jpg')}")
    plt.savefig(save)
    plt.close()


    plt.figure(figsize=(10, 10))
    plt.plot(df['Time (s)'], filtered_x, label='Filtered Accel X', color='black')
    plt.plot(df['Time (s)'], filtered_y, label='Filtered Accel Y', color='red')
    plt.plot(df['Time (s)'], filtered_z, label='Filtered Accel Z', color='blue')
    plt.title(f'Subject {os.path.basename(main_folder)}, {knee} knee, filtered')
    plt.xlabel('Time(s)')
    plt.ylabel('Accel Mag(g)')
    plt.legend()
    plt.grid(True)

    save_filtered = os.path.join(main_folder, subfolder, 'CSV', f"{file_name.replace('.csv', '_filtered.jpg')}")
    plt.savefig(save_filtered)
    plt.close()

subA()
subB()
subC()