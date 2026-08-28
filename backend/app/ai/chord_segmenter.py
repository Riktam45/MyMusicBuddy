from app.ai.chord_detector import detect_chord
from app.ai.chord_formatter import format_chord
from app.ai.chord_schema import ChordSegment
from app.ai.note_window import notes_in_window


def detect_segment_chords(
    note_events,
    segments,
):
    """
    Detect a chord for every time segment.
    """

    results = []

    for segment in segments:

        notes = notes_in_window(
            note_events,
            segment["start"],
            segment["end"],
        )

        chord = detect_chord(notes)

        if not chord:
            continue

        chord_name = format_chord(
            chord["root"],
            chord["type"],
        )

        results.append(
            ChordSegment(
                chord=chord_name,
                root=chord["root"],
                type=chord["type"],
                start=segment["start"],
                end=segment["end"],
                confidence=chord["score"],
            )
        )

    return results