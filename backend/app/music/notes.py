NOTE_NAMES = [
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


def note_to_pitch_class(note: str) -> int:
    return NOTE_NAMES.index(note)


def pitch_class_to_note(pitch_class: int) -> str:
    return NOTE_NAMES[pitch_class % 12]