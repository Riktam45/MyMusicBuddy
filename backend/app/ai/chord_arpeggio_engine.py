from app.ai.arpeggio_analyzer import (
    analyze_arpeggio,
)


SUPPORTED_ARPEGGIOS = {
    "major": "major",
    "minor": "minor",
    "diminished": "diminished",
    "maj7": "maj7",
    "min7": "min7",
    "dom7": "dom7",
}


def analyze_chord_arpeggio(
    root: str,
    chord_type: str,
):
    """
    Generate an arpeggio matching
    the detected chord.
    """

    arpeggio_type = SUPPORTED_ARPEGGIOS.get(
        chord_type
    )

    if not arpeggio_type:
        return None

    return analyze_arpeggio(
        root,
        arpeggio_type,
    )