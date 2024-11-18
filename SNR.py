import numpy as np


def calculate_snr(signal_rms, noise_rms):
    return 20 * np.log10(signal_rms / noise_rms) if noise_rms != 0 else np.inf
