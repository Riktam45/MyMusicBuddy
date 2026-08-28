from app.ai.ml_note_schema import (
    MLNoteEvent,
    MLTranscriptionResult,
)


def build_ml_context(
    transcription: MLTranscriptionResult,
) -> dict:
    """
    Convert ML transcription into a simple
    music-analysis context.
    """

    notes = transcription.notes

    pitch_classes = [
        note.pitch % 12
        for note in notes
    ]

    unique_pitch_classes = sorted(
        set(pitch_classes)
    )

    return {
        "notes": notes,
        "pitch_classes": pitch_classes,
        "unique_pitch_classes": (
            unique_pitch_classes
        ),
        "note_count": len(notes),
        "model": transcription.model,
    }