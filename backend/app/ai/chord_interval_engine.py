from app.ai.interval_analyzer import (
    identify_interval,
)


CHORD_INTERVALS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "dom7": [0, 4, 7, 10],
}


def analyze_chord_intervals(
    root: str,
    chord_type: str,
):
    """
    Analyze the intervals contained
    within a chord.
    """

    intervals = CHORD_INTERVALS.get(
        chord_type
    )

    if intervals is None:
        return []

    results = []

    for semitones in intervals:

        # Import here to keep the dependency simple.
        from app.music.notes import (
            pitch_class_to_note,
            note_to_pitch_class,
        )

        root_pitch = note_to_pitch_class(
            root
        )

        note = pitch_class_to_note(
            root_pitch + semitones
        )

        results.append(
            {
                "root": root,
                "note": note,
                "semitones": semitones,
                "name": identify_interval(
                    root,
                    note,
                ),
            }
        )

    return results