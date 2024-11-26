import os
import numpy as np
from scipy.io.wavfile import write
from calc import row_separate


def data_to_audio(file_path, sample_rate=44100):
    df = row_separate(file_path)
    time = df['Time (s)']
    axes = [df[axis] - np.mean(df[axis]) for axis in ['X (g)', 'Y (g)', 'Z (g)']]

    base_dir, base_name = os.path.split(file_path)
    base_name = os.path.splitext(base_name)[0]  # Removing CSV Extension

    for axis_data, axis_label in zip(axes, ['X', 'Y', 'Z']):
        max_time = time.iloc[-1]
        num_samples = int(max_time * sample_rate)
        new_time = np.linspace(0, max_time, num_samples)
        interpolated_signal = np.interp(new_time, time, axis_data)

        # Signal normalization
        interpolated_signal = interpolated_signal / np.max(np.abs(interpolated_signal))

        # Converting into int16
        audio_data = (interpolated_signal * 32767).astype(np.int16)

        output_file = os.path.join(base_dir, f"{base_name}_{axis_label}.wav")

        write(output_file, sample_rate, audio_data)
        print(f"Audio for {axis_label} axis saved to {output_file}")

# Пример использования
# data_to_audio('path_to_your_file.csv')