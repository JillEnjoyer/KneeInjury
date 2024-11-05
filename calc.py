import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def row_separate(file_path):
    df = pd.read_csv(file_path, sep=',', header=0)
    return df

def calculate_rms(data):
    return np.sqrt(np.mean(np.square(data)))

def calculate_snr(signal, noise):
    signal_rms = calculate_rms(signal)
    noise_rms = calculate_rms(noise)
    return 20 * np.log10(signal_rms / noise_rms) if noise_rms != 0 else np.inf

def calculate_residuals(signal):
    mean_value = np.mean(signal)
    residuals = signal - mean_value
    mean_residual = np.mean(residuals)
    median_residual = np.median(residuals)
    return mean_residual, median_residual

def generate_noise(size):
    return np.random.normal(0, 0.001, size)

def save_plot(time, accel_x, accel_y, accel_z, file_path):
    plt.figure(figsize=(8, 8))
    plt.plot(time, accel_x, label='Accel X', color='black')
    plt.plot(time, accel_y, label='Accel Y', color='red')
    plt.plot(time, accel_z, label='Accel Z', color='blue')
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

def process_file(file_path):
    df = row_separate(file_path)

    time = df['Time (s)']
    accel_x = df['X (g)'] - np.mean(df['X (g)'])
    accel_y = df['Y (g)'] - np.mean(df['Y (g)'])
    accel_z = df['Z (g)'] - np.mean(df['Z (g)'])

    rms_x = calculate_rms(accel_x)
    rms_y = calculate_rms(accel_y)
    rms_z = calculate_rms(accel_z)

    noise_x = generate_noise(len(accel_x))
    noise_y = generate_noise(len(accel_y))
    noise_z = generate_noise(len(accel_z))

    snr_x = calculate_snr(accel_x, noise_x)
    snr_y = calculate_snr(accel_y, noise_y)
    snr_z = calculate_snr(accel_z, noise_z)

    mean_res_x, median_res_x = calculate_residuals(accel_x)
    mean_res_y, median_res_y = calculate_residuals(accel_y)
    mean_res_z, median_res_z = calculate_residuals(accel_z)

    results = {
        'RMS for X axis': rms_x,
        'RMS for Y axis': rms_y,
        'RMS for Z axis': rms_z,
        'SNR for X axis': snr_x,
        'SNR for Y axis': snr_y,
        'SNR for Z axis': snr_z,
        'Mean Residuals for X axis': mean_res_x,
        'Mean Residuals for Y axis': mean_res_y,
        'Mean Residuals for Z axis': mean_res_z,
        'Median Residuals for X axis': median_res_x,
        'Median Residuals for Y axis': median_res_y,
        'Median Residuals for Z axis': median_res_z
    }

    save_plot(time, accel_x, accel_y, accel_z, file_path)
    save_results_to_txt(file_path, results)

def signal_plot(file_path):
    if os.path.isdir(file_path):
        for item in os.listdir(file_path):
            if item.endswith('.csv'):
                full_item_path = os.path.join(file_path, item)
                print(f"Processing file: {full_item_path}")
                process_file(full_item_path)
    else:
        print(f"Processing single file: {file_path}")
        process_file(file_path)
