from app.music.intervals import INTERVAL_NAMES
from app.music.notes import note_to_pitch_class


def calculate_interval(
    root: str,
    note: str,
) -> int:
    """
    Calculate the chromatic interval between
    a root note and another note.
    """

    root_pitch = note_to_pitch_class(root)
    note_pitch = note_to_pitch_class(note)

    return (note_pitch - root_pitch) % 12


def identify_interval(
    root: str,
    note: str,
) -> str:
    """
    Return the musical interval name.
    """

    interval = calculate_interval(
        root,
        note,
    )

    return INTERVAL_NAMES[interval]