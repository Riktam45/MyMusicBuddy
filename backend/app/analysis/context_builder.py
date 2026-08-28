import librosa

from app.analysis.context import AnalysisContext
from app.ai.feature_extractor import extract_features


def build_context(audio_path: str):
    """
    Build a reusable analysis context.
    """

    audio, sr = librosa.load(
        audio_path,
        sr=16000,
        mono=True,
    )

    features = extract_features(audio_path)

    return AnalysisContext(
        audio=audio,
        sample_rate=sr,
        features=features,
    )