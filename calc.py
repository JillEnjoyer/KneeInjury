import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

from RMS import calculate_rms
from SNR import calculate_snr


def row_separate(file_path):
    return pd.read_csv(file_path, sep=',', header=0)


def calculate_residuals(signal):
    residuals = signal - np.mean(signal)
    return np.mean(residuals), np.median(residuals)


def save_plot(time, axes, file_path):
    colors = ['black', 'red', 'blue']
    labels = ['Accel X', 'Accel Y', 'Accel Z']

    plt.figure(figsize=(8, 8))
    for axis, color, label in zip(axes, colors, labels):
        plt.plot(time, axis, label=label, color=color)
    plt.title(f'Data from {os.path.basename(file_path)}')
    plt.xlabel('Time (s)')
    plt.ylabel('Accel Magnitude (g)')
    plt.legend()
    plt.grid(True)

    save_path = file_path.replace('.csv', '.jpg')
    plt.savefig(save_path)
    plt.close()
    print(f"Plot saved as {save_path}")


def save_results_to_txt(file_path, results):
    txt_file_path = file_path.replace('.csv', '.txt')
    with open(txt_file_path, 'w') as f:
        f.write(f'Results for {file_path}:\n')
        for key, value in results.items():
            f.write(f'{key}: {value}\n')
    print(f"Results saved in {txt_file_path}")


def process_file(file_path, noise_file_path, presaved_noise_flag, mode_flag):
    df = row_separate(file_path)
    time = df['Time (s)']
    axes = [df[axis] - np.mean(df[axis]) for axis in ['X (g)', 'Y (g)', 'Z (g)']]

    if mode_flag == "plot":
        save_plot(time, axes, file_path)
        return

    noise_axes = []
    if presaved_noise_flag:
        with open(noise_file_path, 'r') as file:
            reader = csv.reader(file)
            noise_axes = [float(row[0]) for row in list(reader)]
    else:
        noise_df = row_separate(noise_file_path)
        noise_axes = [calculate_rms(noise_df[axis] - np.mean(noise_df[axis])) for axis in ['X (g)', 'Y (g)', 'Z (g)']]

    results = {}
    for axis, noise, label in zip(axes, noise_axes, ['X', 'Y', 'Z']):
        rms = calculate_rms(axis)
        snr = calculate_snr(rms, noise)
        mean_res, median_res = calculate_residuals(axis)

        results.update({
            f'RMS for {label} axis': rms,
            f'SNR for {label} axis': snr,
            f'Mean Residuals for {label} axis': mean_res,
            f'Median Residuals for {label} axis': median_res,
        })

    save_plot(time, axes, file_path)
    save_results_to_txt(file_path, results)


def signal_plot(file_path, noise_file_path, presaved_noise_flag, mode_flag):
    files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.csv')] if os.path.isdir(file_path) else [file_path]

    for file in files:
        print(f"Processing file: {file}")
        process_file(file, noise_file_path, presaved_noise_flag, mode_flag)
