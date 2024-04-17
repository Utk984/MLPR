import os
import sys

import librosa
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


def getfeatures(file, scale_audio=False, onlySingleDigit=False):
    fs = None
    audio_data, sample_rate = librosa.load(file, sr=fs)
    x = audio_data
    fs = sample_rate
    features = []
    if scale_audio:
        x = x / np.max(np.abs(x))

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


def classify_song(train_data, train_labels, test_data, n_neighbors=5):
    scaler = StandardScaler()
    train_data_scaled = scaler.fit_transform(train_data)
    test_data_scaled = scaler.transform(test_data)

    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(train_data_scaled)

    _, indices = knn.kneighbors(test_data_scaled)

    test_labels = [
        max(set(train_labels[i]), key=train_labels[i].count) for i in indices[:, 0]
    ]

    return test_labels[0]


if __name__ == "__main__":
    feature_dataset_path = "./songs_all.csv"
    feature_df = pd.read_csv(feature_dataset_path)
    feature_df.drop(
        ["power", "pitch_mean", "pitch_std", "voiced_fr"], axis=1, inplace=True
    )

    label_dataset_path = "./utils/clustered_all.csv"
    label_df = pd.read_csv(label_dataset_path)

    X = feature_df.iloc[:, 1:].values
    y = label_df["Labels"].values

    new_audio_file = sys.argv[1]

    new_features = getfeatures(new_audio_file)

    new_label = classify_song(X, y, new_features, n_neighbors=5)

    print(f"The new audio file belongs to cluster: {new_label}")
