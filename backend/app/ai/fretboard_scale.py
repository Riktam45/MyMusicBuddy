from app.ai.fretboard_engine import generate_fretboard


def find_scale_positions(
    scale_notes: list[str],
):
    """
    Find every guitar position that belongs
    to the supplied scale.
    """

    fretboard = generate_fretboard()

    scale_notes = set(scale_notes)

    positions = []

    for position in fretboard:

        if position["note"] in scale_notes:
            positions.append(position)

    return positions