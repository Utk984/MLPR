import os

import librosa
import matplotlib.pyplot as plt
import numpy as np


# Function to extract pitch and tempo from an audio file
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mean_pitch = np.mean(pitches)
    mean_tempo = np.mean(tempo)
    return mean_pitch, mean_tempo


def plot(audio_dir):
    # Lists to store pitch and tempo values
    all_pitches = []
    all_tempos = []

    # Iterate through each audio file
    for filename in os.listdir(audio_dir):
        if filename.endswith(".wav"):
            audio_file = os.path.join(audio_dir, filename)
            mean_pitch, mean_tempo = extract_features(audio_file)
            all_pitches.append(mean_pitch)
            all_tempos.append(mean_tempo)

    # Scatter plot of mean pitch vs mean tempo for all audio files
    scatter(all_pitches, all_tempos, "Star Wars All Audio Files")


def scatter(list1, list2, title):
    plt.figure(figsize=(8, 6))
    plt.scatter(list1, list2, color="purple", alpha=0.75, label="Humming")
    plt.xlabel("Mean MFCC")
    plt.ylabel("Mean Tempo")
    plt.title(title)
    plt.scatter(list1[-2], list2[-2], color="red", alpha=0.75, label="Full")
    plt.scatter(list1[-1], list2[-1], color="blue", alpha=0.75, label="Sample")
    plt.legend(loc="upper right")
    plt.show()


# Directory containing the audio files
audio_dir = "../dataset1/MLEndHWD_StarWars_Audio_Files/"
plot(audio_dir)
