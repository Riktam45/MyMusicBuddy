from .schema import HybridNoteEvent


def build_hybrid_notes(
    ml_notes,
    dsp_notes,
    time_tolerance: float = 0.15,
):
    """
    Combine ML and DSP note predictions.

    Matching notes become hybrid notes.
    Unmatched notes are preserved with
    their original source.
    """

    results = []

    used_dsp = set()

    for ml_note in ml_notes:

        best_dsp = None
        best_index = None
        best_difference = None

        for index, dsp_note in enumerate(
            dsp_notes
        ):

            if index in used_dsp:
                continue

            if (
                ml_note.note
                != dsp_note.note
            ):
                continue

            if (
                ml_note.octave
                != dsp_note.octave
            ):
                continue

            difference = abs(
                ml_note.start
                - dsp_note.time
            )

            if (
                difference
                <= time_tolerance
                and (
                    best_difference
                    is None
                    or difference
                    < best_difference
                )
            ):
                best_dsp = dsp_note
                best_index = index
                best_difference = difference

        if best_dsp is not None:

            used_dsp.add(
                best_index
            )

            confidence = (
                ml_note.confidence
                + best_dsp.confidence
            ) / 2

            results.append(
                HybridNoteEvent(
                    note=ml_note.note,
                    octave=ml_note.octave,
                    midi=ml_note.midi,
                    start=ml_note.start,
                    end=ml_note.end,
                    duration=ml_note.duration,
                    confidence=round(
                        confidence,
                        3,
                    ),
                    source="hybrid",
                )
            )

        else:

            results.append(
                HybridNoteEvent(
                    note=ml_note.note,
                    octave=ml_note.octave,
                    midi=ml_note.midi,
                    start=ml_note.start,
                    end=ml_note.end,
                    duration=ml_note.duration,
                    confidence=ml_note.confidence,
                    source="ml",
                )
            )

    # Add DSP notes that were not matched
    for index, dsp_note in enumerate(
        dsp_notes
    ):

        if index in used_dsp:
            continue

        results.append(
            HybridNoteEvent(
                note=dsp_note.note,
                octave=dsp_note.octave,
                midi=dsp_note.pitch,
                start=dsp_note.time,
                end=dsp_note.time,
                duration=0.0,
                confidence=dsp_note.confidence,
                source="dsp",
            )
        )

    results.sort(
        key=lambda note: note.start
    )

    return results