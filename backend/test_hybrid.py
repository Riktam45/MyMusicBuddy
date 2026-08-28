from app.analysis.context_builder import (
    build_context,
)

from app.ai.note_transcriber import (
    transcribe_notes,
)

from ml.basic_pitch.inference import (
    transcribe_with_basic_pitch,
)

from ml.hybrid.engine import (
    build_hybrid_notes,
)


AUDIO_FILE = (
    r"tone-test.mp3"
)


print("Loading audio...")

context = build_context(
    AUDIO_FILE
)


print("Running DSP...")

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


print("Building hybrid result...")

hybrid_notes = build_hybrid_notes(
    ml_notes,
    dsp_notes,
)


print()
print(
    "========== HYBRID ENGINE =========="
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
    "Hybrid notes:",
    len(hybrid_notes)
)

print()
print(
    "First 30 hybrid notes:"
)

for note in hybrid_notes[:30]:

    print(
        f"{note.note}{note.octave}"
        f" | {note.start}s"
        f" | confidence "
        f"{note.confidence}"
        f" | source={note.source}"
    )

print(
    "===================================="
)