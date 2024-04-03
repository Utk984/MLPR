import csv
import sys

import librosa
import numpy as np


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
    name = file.split("/")[-1].replace("_clean", "")

    if scale_audio:
        x = x / np.max(np.abs(x))

    f0, voiced_flag = getPitch(x, fs, winLen=0.02)

    stft = np.abs(librosa.stft(audio_data))
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sample_rate)
    chroma = librosa.feature.chroma_stft(S=stft, sr=sample_rate)
    mel = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
    contrast = librosa.feature.spectral_contrast(S=stft, sr=sample_rate)
    spec_cent = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)
    spec_bw = librosa.feature.spectral_bandwidth(y=audio_data, sr=sample_rate)
    rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sample_rate)

    features = []
    header = ["filename", "pitch"]
    header.extend([f"mfcc_{i}" for i in range(mfcc.shape[0])])
    header.extend([f"chroma_{i}" for i in range(chroma.shape[0])])
    header.extend([f"mel_{i}" for i in range(mel.shape[0])])
    header.extend([f"contrast_{i}" for i in range(contrast.shape[0])])
    header.extend([f"spec_cent_{i}" for i in range(spec_cent.shape[0])])
    header.extend([f"spec_bw_{i}" for i in range(spec_bw.shape[0])])
    header.extend([f"rolloff_{i}" for i in range(rolloff.shape[0])])

    features.append(header)

    for i in range(len(f0)):
        frame_features = [
            name,
            f0[i],
            *mfcc[:, i],
            *chroma[:, i],
            *mel[:, i],
            *contrast[:, i],
            *spec_cent[:, i],
            *spec_bw[:, i],
            *rolloff[:, i],
        ]
        features.append(frame_features)

    return features


def extract(filename):
    if filename.endswith(".wav"):
        features = getfeatures(filename)
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(features)


file = sys.argv[1]
extract(file)
