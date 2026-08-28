from dataclasses import dataclass


@dataclass
class NoteComparison:
    ml_note: str
    ml_octave: int
    dsp_note: str | None
    dsp_octave: int | None
    time_difference: float | None
    matched: bool


def compare_notes(
    ml_notes,
    dsp_notes,
    time_tolerance: float = 0.15,
):
    """
    Compare ML note events against DSP note events.

    A note is considered matched when:
    - note name is the same
    - octave is the same
    - timestamps are within the tolerance
    """

    comparisons = []

    used_dsp_indices = set()

    for ml_note in ml_notes:

        best_match = None
        best_index = None
        best_difference = None

        ml_time = ml_note.start

        for index, dsp_note in enumerate(
            dsp_notes
        ):

            if index in used_dsp_indices:
                continue

            dsp_time = dsp_note.time

            difference = abs(
                ml_time - dsp_time
            )

            if (
                difference
                <= time_tolerance
            ):

                same_note = (
                    ml_note.note
                    == dsp_note.note
                )

                same_octave = (
                    ml_note.octave
                    == dsp_note.octave
                )

                if (
                    same_note
                    and same_octave
                ):

                    if (
                        best_difference
                        is None
                        or difference
                        < best_difference
                    ):
                        best_match = dsp_note
                        best_index = index
                        best_difference = (
                            difference
                        )

        if best_match is not None:

            used_dsp_indices.add(
                best_index
            )

            comparisons.append(
                NoteComparison(
                    ml_note=ml_note.note,
                    ml_octave=ml_note.octave,
                    dsp_note=best_match.note,
                    dsp_octave=best_match.octave,
                    time_difference=round(
                        best_difference,
                        3,
                    ),
                    matched=True,
                )
            )

        else:

            comparisons.append(
                NoteComparison(
                    ml_note=ml_note.note,
                    ml_octave=ml_note.octave,
                    dsp_note=None,
                    dsp_octave=None,
                    time_difference=None,
                    matched=False,
                )
            )

    return comparisons


def calculate_agreement(
    comparisons,
) -> float:
    """
    Calculate the percentage of ML notes
    that were also detected by the DSP system.
    """

    if not comparisons:
        return 0.0

    matched = sum(
        1
        for comparison in comparisons
        if comparison.matched
    )

    return round(
        matched
        / len(comparisons)
        * 100,
        2,
    )