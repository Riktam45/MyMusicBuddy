from app.music.chords import CHORDS


NOTE_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]


def generate_candidates(note_pitches):
    """
    Generate possible chords from detected notes.
    """

    if not note_pitches:
        return []

    detected = {
        pitch % 12
        for pitch in note_pitches
    }

    candidates = []

    for root in range(12):

        for chord_name, intervals in CHORDS.items():

            expected = {
                (root + interval) % 12
                for interval in intervals
            }

            intersection = detected & expected

            if not intersection:
                continue

            score = len(intersection) / len(expected)

            candidates.append(
                {
                    "root": NOTE_NAMES[root],
                    "type": chord_name,
                    "score": round(score, 3),
                }
            )

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return candidates