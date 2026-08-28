import librosa
import numpy as np

from app.analysis.context import AnalysisContext


def detect_bpm(
    context: AnalysisContext,
):
    """
    Detect BPM using librosa.
    """

    tempo, _ = librosa.beat.beat_track(
        y=context.audio,
        sr=context.sample_rate,
    )

    tempo_value = float(
        np.asarray(tempo).reshape(-1)[0]
    )

    return round(
        tempo_value,
        2,
    )