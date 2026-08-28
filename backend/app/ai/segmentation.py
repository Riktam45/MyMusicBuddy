def create_segments(
    beats: list[float],
    beats_per_segment: int = 4,
):
    """
    Group beats into musical segments.
    """

    if not beats:
        return []

    segments = []

    for index in range(
        0,
        len(beats) - 1,
        beats_per_segment,
    ):
        start = beats[index]

        end_index = min(
            index + beats_per_segment,
            len(beats) - 1,
        )

        end = beats[end_index]

        if end > start:
            segments.append(
                {
                    "start": start,
                    "end": end,
                }
            )

    return segments