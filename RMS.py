import numpy as np


def calculate_rms(data):
    return np.sqrt(np.mean(np.square(data)))
