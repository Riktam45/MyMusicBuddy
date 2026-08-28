def format_chord(root: str, chord_type: str) -> str:
    """
    Convert chord root + type into readable chord notation.
    """

    suffixes = {
        "major": "",
        "minor": "m",
        "diminished": "dim",
        "maj7": "maj7",
        "min7": "m7",
        "dom7": "7",
    }

    suffix = suffixes.get(
        chord_type,
        chord_type,
    )

    return f"{root}{suffix}"