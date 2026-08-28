def smooth_chords(
    chord_segments,
):
    """
    Remove isolated chord predictions
    surrounded by another chord.
    """

    if len(chord_segments) < 3:
        return chord_segments

    result = chord_segments.copy()

    for i in range(1, len(result) - 1):

        previous_chord = result[i - 1].chord
        current_chord = result[i].chord
        next_chord = result[i + 1].chord

        if (
            previous_chord == next_chord
            and current_chord != previous_chord
        ):
            result[i] = result[i - 1].model_copy(
                update={
                    "start": result[i].start,
                    "end": result[i].end,
                }
            )

    return result