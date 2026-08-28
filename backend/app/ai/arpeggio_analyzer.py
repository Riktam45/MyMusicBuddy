from app.ai.arpeggio_generator import (
    generate_arpeggio,
)
from app.ai.interval_analyzer import (
    identify_interval,
)


def analyze_arpeggio(
    root: str,
    arpeggio_type: str,
):
    """
    Generate an arpeggio and identify
    the intervals inside it.
    """

    notes = generate_arpeggio(
        root,
        arpeggio_type,
    )

    intervals = [
        identify_interval(
            root,
            note,
        )
        for note in notes
    ]

    return {
        "name": arpeggio_type,
        "root": root,
        "notes": notes,
        "intervals": intervals,
    }