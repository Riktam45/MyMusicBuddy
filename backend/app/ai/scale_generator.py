from app.music.notes import (
    note_to_pitch_class,
    pitch_class_to_note,
)
from app.music.scales import (
    SCALES,
    MODES,
)


def generate_scale(
    root: str,
    intervals: list[int],
) -> list[str]:
    """
    Generate note names for a scale.
    """

    root_pitch = note_to_pitch_class(root)

    return [
        pitch_class_to_note(
            root_pitch + interval
        )
        for interval in intervals
    ]


def generate_all_scales(root: str):
    """
    Generate all supported scales for a root.
    """

    results = {}

    for name, intervals in SCALES.items():

        results[name] = generate_scale(
            root,
            intervals,
        )

    for name, intervals in MODES.items():

        results[name] = generate_scale(
            root,
            intervals,
        )

    return results