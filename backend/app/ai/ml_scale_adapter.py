from app.ai.ml_note_schema import MLNoteEvent


def extract_pitch_classes(
    notes: list[MLNoteEvent],
) -> list[int]:

    return sorted(
        set(
            note.pitch % 12
            for note in notes
        )
    )


def build_scale_context(
    notes: list[MLNoteEvent],
) -> dict:

    pitch_classes = extract_pitch_classes(
        notes
    )

    return {
        "pitch_classes": pitch_classes,
        "note_count": len(notes),
    }