from app.ai.chord_candidates import generate_candidates


def detect_chord(note_events):
    """
    Detect the most likely chord from note events.
    """

    if not note_events:
        return None

    pitches = [
        note.pitch
        for note in note_events
    ]

    candidates = generate_candidates(pitches)

    if not candidates:
        return None

    return candidates[0]