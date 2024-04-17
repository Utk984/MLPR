import os

import numpy as np
import parselmouth
from fastdtw import fastdtw
from tqdm import tqdm


def compute_sm_from_wav(x1, x2):
    X = plot_pitch_contour(x1)
    Y = plot_pitch_contour(x2)
    distance, _ = fastdtw(X, Y)
    return distance


def plot_pitch_contour(file):
    sound = parselmouth.Sound(file)
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array["frequency"].reshape(-1, 1)
    return pitch_values


def compute_dmax_for_file(file1, directory):
    values = []
    for file2 in os.listdir(directory):
        if file2.endswith(".wav"):
            dist = compute_sm_from_wav(
                file1,
                os.path.join(directory, file2),
            )
            values.append((file2, dist))
    values.sort(key=lambda x: x[1])
    return values[:5]


# Example usage
directory = "./data/hum_test/"

total = 0
correct1 = 0
for file in tqdm(os.listdir(directory)):
    total += 1
    if file.endswith(".wav"):
        values = compute_dmax_for_file(
            os.path.join(directory, file), "./data/song_test/"
        )
        if "Hakuna Matata_clean.wav" in [file for file, _ in values]:
            correct1 += 1

print(f"Accuracy of values: {correct1/total}")
