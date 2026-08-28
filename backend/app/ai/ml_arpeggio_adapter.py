from app.ai.ml_note_schema import MLNoteEvent


def build_arpeggio_context(
    notes: list[MLNoteEvent],
) -> dict:

    sorted_notes = sorted(
        notes,
        key=lambda note: (
            note.start,
            note.pitch,
        ),
    )

    pitch_sequence = [
        note.pitch
        for note in sorted_notes
    ]

    pitch_classes = [
        note.pitch % 12
        for note in sorted_notes
    ]

    return {
        "pitch_sequence": pitch_sequence,
        "pitch_classes": pitch_classes,
        "note_count": len(notes),
    }