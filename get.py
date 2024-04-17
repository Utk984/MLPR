import os
import time

import numpy as np
import parselmouth
from fastdtw import fastdtw


def load_pitch_values(file_path):
    return np.load(file_path)


def compute_sm_from_pitch_arrays(pitch_array1, pitch_array2):
    distance, _ = fastdtw(pitch_array1, pitch_array2)
    return distance


def compute_top_matches_for_wav(wav_file, npy_directory):
    # Compute pitch contour for the input WAV file
    pitch_values1 = plot_pitch_contour(wav_file)

    # Iterate over .npy files in the directory
    top_matches = []
    for npy_file in os.listdir(npy_directory):
        if npy_file.endswith(".npy"):
            npy_path = os.path.join(npy_directory, npy_file)
            pitch_values2 = load_pitch_values(npy_path)
            distance = compute_sm_from_pitch_arrays(pitch_values1, pitch_values2)
            top_matches.append([distance, npy_file])

    # Sort the matches based on distance
    top_matches.sort(key=lambda x: x[0])

    return top_matches[:5]


def plot_pitch_contour(file):
    sound = parselmouth.Sound(file)
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array["frequency"].reshape(-1, 1)
    return pitch_values


# Example usage
wav_file = "./data/dataset1_clean/MLEndHWD_StarWars_Audio_Files_clean/0851_clean.wav"
npy_directory = "./data/pitch_values/"
t1 = time.time()
top_matches = compute_top_matches_for_wav(wav_file, npy_directory)
print("Top 5 closest .npy files:")
for match in top_matches:
    print(f"File: {match[0]}, Distance: {match[1]}")
t2 = time.time()
print("Time taken:", t2 - t1)
