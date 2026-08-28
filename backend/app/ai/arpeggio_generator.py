from app.music.arpeggios import ARPEGGIOS
from app.music.notes import (
    note_to_pitch_class,
    pitch_class_to_note,
)


def generate_arpeggio(
    root: str,
    arpeggio_type: str,
):
    """
    Generate the notes of an arpeggio.
    """

    if arpeggio_type not in ARPEGGIOS:
        raise ValueError(
            f"Unsupported arpeggio type: "
            f"{arpeggio_type}"
        )

    root_pitch = note_to_pitch_class(root)

    intervals = ARPEGGIOS[
        arpeggio_type
    ]

    return [
        pitch_class_to_note(
            root_pitch + interval
        )
        for interval in intervals
    ]