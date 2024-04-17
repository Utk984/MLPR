import csv
import os
import sys

import librosa
import numpy as np


def header(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        header = ["filename"]
        header.extend([f"mfcc_{i}" for i in range(1, 21)])
        header.extend([f"chroma_{i}" for i in range(1, 13)])
        header.extend([f"mel_{i}" for i in range(1, 129)])
        header.extend([f"contrast_{i}" for i in range(1, 8)])
        header.extend(
            [
                "power",
                "pitch_mean",
                "pitch_std",
                "voiced_fr",
                "rms",
                "spec_cent",
                "spec_bw",
                "rolloff",
                "zcr",
                "spectral_flatness",
            ]
        )
        header.extend([f"spectral_flux_{i}" for i in range(1, 21)])
        writer.writerow(header)


def getPitch(x, fs, winLen=0.02):
    p = winLen * fs
    frame_length = int(2 ** int(p - 1).bit_length())
    hop_length = frame_length // 2
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y=x, fmin=80, fmax=450, sr=fs, frame_length=frame_length, hop_length=hop_length
    )
    return f0, voiced_flag


def getfeatures(file, scale_audio=False, onlySingleDigit=False):
    fs = None
    audio_data, sample_rate = librosa.load(file, sr=fs)
    x = audio_data
    fs = sample_rate
    name = os.path.basename(file)
    features = [name]
    if scale_audio:
        x = x / np.max(np.abs(x))
    f0, voiced_flag = getPitch(x, fs, winLen=0.02)

    power = np.sum(x**2) / len(x)
    pitch_mean = np.nanmean(f0) if np.mean(np.isnan(f0)) < 1 else 0
    pitch_std = np.nanstd(f0) if np.mean(np.isnan(f0)) < 1 else 0
    voiced_fr = np.mean(voiced_flag)

    stft = np.abs(librosa.stft(audio_data))

    mfcc = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate).T, axis=0)
    features.extend(mfcc)

    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    features.extend(chroma)

    mel = np.mean(
        librosa.feature.melspectrogram(y=audio_data, sr=sample_rate).T,
        axis=0,
    )
    features.extend(mel)

    contrast = np.mean(
        librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0
    )
    features.extend(contrast)

    xi = [power, pitch_mean, pitch_std, voiced_fr]
    features.extend(xi)

    rms = np.mean(librosa.feature.rms(y=audio_data))
    features.extend([rms])

    spec_cent = np.mean(
        librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate).T, axis=0
    )
    features.extend(spec_cent)

    spec_bw = np.mean(
        librosa.feature.spectral_bandwidth(y=audio_data, sr=sample_rate).T, axis=0
    )
    features.extend(spec_bw)

    rolloff = np.mean(
        librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate).T, axis=0
    )
    features.extend(rolloff)

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=audio_data))
    features.extend([zcr])

    spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=audio_data))
    features.extend([spectral_flatness])

    mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    delta_mfccs = np.diff(mfccs.T, axis=0)
    spectral_flux = np.mean(delta_mfccs, axis=0)
    features.extend(spectral_flux)

    return features


def extract_and_save_features(filename, output):
    if filename.endswith(".wav"):
        feature = getfeatures(filename)
        with open(output, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(feature)


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    if not os.path.exists(output):
        header(output)
    extract_and_save_features(input, output)
