import csv
import os
import sys

import librosa
import numpy as np


def header(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        header = ["filename"]
        header.extend([f"mfcc_mean_{i}" for i in range(1, 21)])
        header.extend([f"mfcc_std_{i}" for i in range(1, 21)])
        header.extend([f"mfcc_var_{i}" for i in range(1, 21)])
        writer.writerow(header)


def getfeatures(file):
    fs = None
    audio_data, sample_rate = librosa.load(file, sr=fs)
    name = os.path.basename(file)
    features = [name]

    mfcc = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=20)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)
    mfcc_var = np.var(mfcc, axis=1)

    features.extend(mfcc_mean)
    features.extend(mfcc_std)
    features.extend(mfcc_var)

    return features


def extract_and_save_features(filename, output):
    if filename.endswith(".wav"):
        feature = getfeatures(filename)
        with open(output, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(feature)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.exists(output_file):
        header(output_file)
    extract_and_save_features(input_file, output_file)
