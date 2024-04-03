import os

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


# Function to load audio file and extract features
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    mean_pitch = np.mean(pitches)
    mean_tempo = np.mean(tempo)

    return y, sr, spectrogram, mfccs, mean_pitch, mean_tempo


# Function to compare two audio files
def compare_audio(file1, file2):
    # Load and extract features for both audio files
    y1, sr1, spec1, mfccs1, mean_pitch1, mean_tempo1 = extract_features(file1)
    y2, sr2, spec2, mfccs2, mean_pitch2, mean_tempo2 = extract_features(file2)

    # Plot 1: Mel Spectrogram comparison
    plt.figure()
    plt.subplot(2, 1, 1)
    librosa.display.specshow(
        librosa.power_to_db(spec1, ref=np.max), sr=sr1, y_axis="mel", x_axis="time"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel Spectrogram - " + os.path.basename(file1))
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    plt.subplot(2, 1, 2)
    librosa.display.specshow(
        librosa.power_to_db(spec2, ref=np.max), sr=sr2, y_axis="mel", x_axis="time"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel Spectrogram - " + os.path.basename(file2))
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    plt.tight_layout()
    plt.show()

    # Plot 2: MFCC comparison
    plt.figure()
    plt.subplot(2, 1, 1)
    librosa.display.specshow(mfccs1, sr=sr1, x_axis="time")
    plt.colorbar()
    plt.title("MFCC - " + os.path.basename(file1))
    plt.xlabel("Time (s)")
    plt.ylabel("MFCC Coefficients")

    plt.subplot(2, 1, 2)
    librosa.display.specshow(mfccs2, sr=sr2, x_axis="time")
    plt.colorbar()
    plt.title("MFCC - " + os.path.basename(file2))
    plt.xlabel("Time (s)")
    plt.ylabel("MFCC Coefficients")

    plt.tight_layout()
    plt.show()

    # Plot 3: Waveform comparison
    plt.figure()
    plt.subplot(2, 1, 1)
    time = np.arange(len(y1)) / sr1
    plt.plot(time, y1)
    plt.title("Waveform - " + os.path.basename(file1))
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.subplot(2, 1, 2)
    time = np.arange(len(y2)) / sr2
    plt.plot(time, y2)
    plt.title("Waveform - " + os.path.basename(file2))
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()


# Example usage
audio_file1 = "./0842.wav"
audio_file2 = "./output.wav"
compare_audio(audio_file1, audio_file2)
