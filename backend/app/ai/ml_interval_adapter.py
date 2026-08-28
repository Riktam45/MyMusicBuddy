from app.ai.ml_note_schema import MLNoteEvent


def build_intervals(
    notes: list[MLNoteEvent],
) -> list[dict]:

    if len(notes) < 2:
        return []

    sorted_notes = sorted(
        notes,
        key=lambda note: (
            note.start,
            note.pitch,
        ),
    )

    intervals = []

    for previous, current in zip(
        sorted_notes,
        sorted_notes[1:],
    ):

        semitones = (
            current.pitch
            - previous.pitch
        )

        intervals.append(
            {
                "root_pitch": (
                    previous.pitch
                ),
                "note_pitch": (
                    current.pitch
                ),
                "semitones": semitones,
                "start": current.start,
            }
        )

    return intervals