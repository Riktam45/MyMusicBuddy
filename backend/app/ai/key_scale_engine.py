from app.ai.scale_generator import generate_all_scales


def recommend_song_scales(
    key: str,
):
    """
    Generate scales based on the song's key.
    """

    scales = generate_all_scales(key)

    priority = [
        "major",
        "major_pentatonic",
        "blues",
    ]

    results = []

    for name in priority:

        if name not in scales:
            continue

        results.append(
            {
                "name": name,
                "root": key,
                "notes": scales[name],
            }
        )

    return results