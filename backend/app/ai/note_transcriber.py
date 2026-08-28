import librosa
import numpy as np

from app.ai.pitch_service import analyze_pitch
from app.ai.note_event import NoteEvent


def transcribe_notes(context):
    """
    Detect the main musical notes present in an audio signal.

    Returns a time-ordered sequence of detected notes.
    """

    f0, voiced_flag, voiced_prob = librosa.pyin(
        context.audio,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=context.sample_rate,
    )

    notes = []

    times = librosa.times_like(
        f0,
        sr=context.sample_rate,
    )

    for time, frequency, voiced, probability in zip(
        times,
        f0,
        voiced_flag,
        voiced_prob,
    ):
        if not voiced:
            continue

        if frequency is None:
            continue

        if np.isnan(frequency):
            continue

        pitch_result = analyze_pitch(
           float(frequency)
        )

        notes.append(
            NoteEvent(
                time=round(
                    float(time),
                    3,
                ),
                frequency=round(
                    float(frequency),
                    2,
                ),
                pitch=pitch_result["midi"],
                note=pitch_result["note"],
                octave=pitch_result["octave"],
                confidence=round(
                    float(probability),
                    3,
                ),
            )
        )

    return notes