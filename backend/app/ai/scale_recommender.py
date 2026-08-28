from app.ai.scale_generator import generate_scale
from app.music_theory.notes import note_to_pitch_class
from app.music_theory.scales import SCALES


def recommend_scales(
    chord_root: str,
    chord_type: str,
    key: str | None = None,
):
    """
    Recommend scales for a detected chord.
    """

    chord_intervals = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 3, 6],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
    }

    intervals = chord_intervals.get(
        chord_type,
        [0, 4, 7],
    )

    chord_root_pitch = note_to_pitch_class(
        chord_root
    )

    chord_notes = {
        (chord_root_pitch + interval) % 12
        for interval in intervals
    }

    recommendations = []

    for scale_name, scale_intervals in SCALES.items():

        scale_notes = {
            (
                chord_root_pitch + interval
            ) % 12
            for interval in scale_intervals
        }

        matches = chord_notes & scale_notes

        score = (
            len(matches)
            / len(chord_notes)
        )

        recommendations.append(
            {
                "name": scale_name,
                "root": chord_root,
                "notes": generate_scale(
                    chord_root,
                    scale_intervals,
                ),
                "score": round(score, 3),
                "reason": (
                    "Chord tones are contained "
                    "within the scale."
                ),
            }
        )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return recommendations