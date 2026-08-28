from collections import Counter

from app.ai.ml_note_schema import MLNoteEvent


PITCH_CLASS_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]


def notes_to_chord_candidates(
    notes: list[MLNoteEvent],
) -> list[str]:

    if not notes:
        return []

    pitch_classes = [
        note.pitch % 12
        for note in notes
    ]

    counts = Counter(
        pitch_classes
    )

    most_common = counts.most_common(4)

    candidates = []

    for pitch_class, _ in most_common:

        pitch_class = pitch_class % 12

        root = PITCH_CLASS_NAMES[
            pitch_class
        ]

        candidates.append(root)

    return candidates