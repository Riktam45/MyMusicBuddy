from app.ai.pitch_analyzer import (
    frequency_to_note,
)


def analyze_pitch(
    frequency: float,
):
    """
    Analyze a single detected frequency.
    """

    return frequency_to_note(
        frequency
    )