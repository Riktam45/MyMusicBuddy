import librosa
import numpy as np


KEYS = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]


def detect_key(context):
    """
    Estimate the musical key using chroma features.
    """

    chroma = librosa.feature.chroma_stft(
        y=context.audio,
        sr=context.sample_rate,
    )

    chroma_mean = np.mean(chroma, axis=1)

    key_index = int(np.argmax(chroma_mean))

    return KEYS[key_index]