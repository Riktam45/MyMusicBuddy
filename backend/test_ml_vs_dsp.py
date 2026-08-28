from app.analysis.context_builder import (
    build_context,
)

from app.ai.note_transcriber import (
    transcribe_notes,
)

from ml.basic_pitch.inference import (
    transcribe_with_basic_pitch,
)

from ml.evaluation.note_comparison import (
    compare_notes,
    calculate_agreement,
)


AUDIO_FILE = (
    r"tone-test.mp3"
)


print("Loading audio...")

context = build_context(
    AUDIO_FILE
)


print("Running DSP transcription...")

dsp_notes = transcribe_notes(
    context
)


print(
    "DSP notes:",
    len(dsp_notes)
)


print("Running Basic Pitch...")

ml_notes = (
    transcribe_with_basic_pitch(
        AUDIO_FILE
    )
)


print(
    "ML notes:",
    len(ml_notes)
)


print()
print(
    "Comparing ML vs DSP..."
)


comparisons = compare_notes(
    ml_notes,
    dsp_notes,
)


agreement = calculate_agreement(
    comparisons
)


matched = sum(
    1
    for comparison
    in comparisons
    if comparison.matched
)


print()
print(
    "========== ML vs DSP =========="
)

print(
    "DSP notes:",
    len(dsp_notes)
)

print(
    "ML notes:",
    len(ml_notes)
)

print(
    "Matched notes:",
    matched
)

print(
    "ML/DSP agreement:",
    f"{agreement}%"
)

print(
    "==============================="
)


print()
print(
    "First 20 comparisons:"
)

for comparison in comparisons[:20]:

    if comparison.matched:

        print(
            f"✓ "
            f"{comparison.ml_note}"
            f"{comparison.ml_octave} "
            f"| time diff "
            f"{comparison.time_difference}s"
        )

    else:

        print(
            f"✗ "
            f"{comparison.ml_note}"
            f"{comparison.ml_octave} "
            f"| no DSP match"
        )