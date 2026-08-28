import math

from app.music.notes import (
    pitch_class_to_note,
)


A4_FREQUENCY = 440.0
A4_MIDI = 69


def frequency_to_midi(
    frequency: float,
) -> float:
    """
    Convert frequency in Hz to a MIDI note number.
    """

    if frequency <= 0:
        raise ValueError(
            "Frequency must be greater than 0."
        )

    return (
        69
        + 12 * math.log2(
            frequency / A4_FREQUENCY
        )
    )


def midi_to_note(
    midi_number: int,
) -> str:
    """
    Convert MIDI number to note name.
    """

    pitch_class = midi_number % 12

    octave = (
        midi_number // 12
    ) - 1

    note = pitch_class_to_note(
        pitch_class
    )

    return f"{note}{octave}"


def frequency_to_note(
    frequency: float,
) -> dict:
    """
    Convert a frequency into the nearest
    musical note and octave.
    """

    midi_float = frequency_to_midi(
        frequency
    )

    midi_number = round(
        midi_float
    )

    note_name = midi_to_note(
        midi_number
    )

    pitch_class = (
        midi_number % 12
    )

    octave = (
        midi_number // 12
    ) - 1

    return {
        "frequency": frequency,
        "midi": midi_number,
        "note": pitch_class_to_note(
            pitch_class
        ),
        "octave": octave,
        "note_with_octave":  midi_to_note(
            midi_number
        ),
        "confidence": calculate_pitch_confidence(
            frequency
        ),
    }

def calculate_pitch_confidence(
    frequency: float,
) -> float:
    """
    Estimate confidence based on how close
    the frequency is to the nearest
    equal-tempered note.
    """

    midi_float = frequency_to_midi(
        frequency
    )

    nearest_midi = round(
        midi_float
    )

    cents_difference = (
        midi_float - nearest_midi
    ) * 100

    cents_difference = abs(
        cents_difference
    )

    confidence = max(
        0.0,
        1.0
        - (
            cents_difference
            / 50.0
        ),
    )

    return round(
        confidence,
        3,
    )