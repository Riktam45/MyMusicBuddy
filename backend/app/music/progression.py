def build_progression(chord_segments):
    """
    Build a chronological chord progression.
    """

    ordered = sorted(
        chord_segments,
        key=lambda x: x.start,
    )

    progression = []

    for segment in ordered:

        if not progression:
            progression.append(
                segment.chord
            )
            continue

        if progression[-1] != segment.chord:
            progression.append(
                segment.chord
            )

    return progression