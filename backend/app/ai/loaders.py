import librosa

from app.analysis.context import AnalysisContext


def load_audio(
    audio_path: str,
) -> AnalysisContext:
    """
    Load an audio file and create an AnalysisContext.
    """

    audio, sample_rate = librosa.load(
        audio_path,
        sr=16000,
        mono=True,
    )

    return AnalysisContext(
        audio=audio,
        sample_rate=sample_rate,
        features={},
    )