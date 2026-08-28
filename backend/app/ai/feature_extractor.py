from pathlib import Path

import librosa
import numpy as np


FEATURE_DIR = Path("storage/features")
FEATURE_DIR.mkdir(parents=True, exist_ok=True)


def extract_features(audio_path: str):
    """
    Extract audio features for AI models.
    """

    y, sr = librosa.load(audio_path, sr=16000, mono=True)

    features = {
        "sample_rate": sr,
        "duration": librosa.get_duration(y=y, sr=sr),
        "tempo": float(librosa.feature.tempo(y=y, sr=sr)[0]),
        "mfcc": librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=13,
        ).tolist(),
        "chroma": librosa.feature.chroma_stft(
            y=y,
            sr=sr,
        ).tolist(),
        "spectral_centroid": librosa.feature.spectral_centroid(
            y=y,
            sr=sr,
        ).tolist(),
        "zero_crossing_rate": librosa.feature.zero_crossing_rate(
            y
        ).tolist(),
        "rms": librosa.feature.rms(
            y=y
        ).tolist(),
    }

    return features