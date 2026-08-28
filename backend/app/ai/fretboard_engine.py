from app.music.notes import (
    note_to_pitch_class,
    pitch_class_to_note,
)

from app.music.fretboard import (
    STANDARD_TUNING,
    NUMBER_OF_FRETS,
)


def generate_fretboard():
    """
    Generate all notes available on a standard
    tuned 6-string guitar.
    """

    fretboard = []

    for string_index, tuning_note in enumerate(
        STANDARD_TUNING
    ):
        open_pitch = note_to_pitch_class(
            tuning_note
        )

        string_number = 6 - string_index

        for fret in range(
            NUMBER_OF_FRETS + 1
        ):
            note = pitch_class_to_note(
                open_pitch + fret
            )

            fretboard.append(
                {
                    "string": string_number,
                    "fret": fret,
                    "note": note,
                }
            )

    return fretboard