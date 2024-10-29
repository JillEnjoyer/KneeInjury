import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#from filters import lowpass_filter

def row_separate(file_path):
    df = pd.read_csv(file_path, sep=',', header=0)
    return df


def calculate_rms(signal):
    return np.sqrt(np.mean(np.square(signal)))


# Функция для расчета SNR (Signal-to-Noise Ratio)
def calculate_snr(signal, noise):
    signal_rms = calculate_rms(signal)
    noise_rms = calculate_rms(noise)
    return 20 * np.log10(signal_rms / noise_rms) if noise_rms != 0 else np.inf


# Функция для расчета резидуалов и их среднего и медианы
def calculate_residuals(signal):
    mean_value = np.mean(signal)
    residuals = signal - mean_value
    mean_residual = np.mean(residuals)
    median_residual = np.median(residuals)
    return mean_residual, median_residual


# Генерация шума для примера
def generate_noise(size):
    return np.random.normal(0, 0.001, size)


def signal_plot(file_path):
    # Проверяем, является ли путь папкой
    if os.path.isdir(file_path):
        for item in os.listdir(file_path):
            if item.endswith('.csv'):
                full_item_path = os.path.join(file_path, item)
                print(f"Processing file: {full_item_path}")
                process_file(full_item_path)
    else:
        print(f"Processing single file: {file_path}")
        process_file(file_path)


def process_file(file_path):
    df = row_separate(file_path)

    time = df['Time (s)']
    accel_x = df['X (g)']
    accel_y = df['Y (g)']
    accel_z = df['Z (g)']

    # Убираем смещения
    accel_x -= np.mean(accel_x)
    accel_y -= np.mean(accel_y)
    accel_z -= np.mean(accel_z)

    # Расчет RMS
    rms_x = calculate_rms(accel_x)
    rms_y = calculate_rms(accel_y)
    rms_z = calculate_rms(accel_z)

    # Генерация шума
    noise_x = generate_noise(len(accel_x))
    noise_y = generate_noise(len(accel_y))
    noise_z = generate_noise(len(accel_z))

    # Расчет SNR
    snr_x = calculate_snr(accel_x, noise_x)
    snr_y = calculate_snr(accel_y, noise_y)
    snr_z = calculate_snr(accel_z, noise_z)

    # Расчет резидуалов
    mean_res_x, median_res_x = calculate_residuals(accel_x)
    mean_res_y, median_res_y = calculate_residuals(accel_y)
    mean_res_z, median_res_z = calculate_residuals(accel_z)

    # Построение графика
    plt.figure(figsize=(8, 8))
    plt.plot(time, accel_x, label='Accel X', color='black')
    plt.plot(time, accel_y, label='Accel Y', color='red')
    plt.plot(time, accel_z, label='Accel Z', color='blue')

    plt.title(f'Data from {os.path.basename(file_path)}')
    plt.xlabel('Time (s)')
    plt.ylabel('Accel Magnitude (g)')
    plt.legend()
    plt.grid(True)

    # Сохранение графика
    save_path = file_path.replace('.csv', '.jpg')
    plt.savefig(save_path)
    plt.close()

    # Запись данных в txt файл
    txt_file_path = file_path.replace('.csv', '.txt')
    with open(txt_file_path, 'w') as f:
        f.write(f'Results for {file_path}:\n')
        f.write(f'RMS for X axis: {rms_x}\n')
        f.write(f'RMS for Y axis: {rms_y}\n')
        f.write(f'RMS for Z axis: {rms_z}\n')
        f.write(f'SNR for X axis: {snr_x} dB\n')
        f.write(f'SNR for Y axis: {snr_y} dB\n')
        f.write(f'SNR for Z axis: {snr_z} dB\n')
        f.write(f'Mean Residuals for X axis: {mean_res_x}\n')
        f.write(f'Mean Residuals for Y axis: {mean_res_y}\n')
        f.write(f'Mean Residuals for Z axis: {mean_res_z}\n')
        f.write(f'Median Residuals for X axis: {median_res_x}\n')
        f.write(f'Median Residuals for Y axis: {median_res_y}\n')
        f.write(f'Median Residuals for Z axis: {median_res_z}\n')

    print(f"Results saved in {txt_file_path}")
