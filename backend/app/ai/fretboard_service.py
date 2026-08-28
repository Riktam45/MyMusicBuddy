from app.ai.fretboard_scale import (
    find_scale_positions,
)


def get_scale_fretboard(
    root: str,
    scale: str,
    notes: list[str],
):
    positions = find_scale_positions(
        notes
    )

    return {
        "root": root,
        "scale": scale,
        "positions": positions,
    }