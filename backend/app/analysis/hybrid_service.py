from app.ai.basic_pitch_service import (
    transcribe_audio,
)

from app.ai.ml_context import (
    build_ml_context,
)

from app.ai.ml_chord_adapter import (
    notes_to_chord_candidates,
)

from app.ai.ml_scale_adapter import (
    build_scale_context,
)

from app.ai.ml_interval_adapter import (
    build_intervals,
)

from app.ai.ml_arpeggio_adapter import (
    build_arpeggio_context,
)

from app.analysis.hybrid_schema import (
    HybridAnalysisResult,
)


def run_hybrid_analysis(
    audio_path: str,
    bpm: float | None = None,
    key: str | None = None,
    beats: list[float] | None = None,
):

    transcription = transcribe_audio(
        audio_path
    )

    notes = transcription.notes

    ml_context = build_ml_context(
        transcription
    )

    chord_candidates = (
        notes_to_chord_candidates(
            notes
        )
    )

    scale_context = (
        build_scale_context(
            notes
        )
    )

    intervals = build_intervals(
        notes
    )

    arpeggio_context = (
        build_arpeggio_context(
            notes
        )
    )

    return HybridAnalysisResult(

        bpm=bpm,

        key=key,

        beats=beats or [],

        ml_notes=notes,

        ml_chord_candidates=(
            chord_candidates
        ),

        ml_pitch_classes=(
            scale_context[
                "pitch_classes"
            ]
        ),

        ml_intervals=intervals,

        ml_arpeggio_context=(
            arpeggio_context
        ),

        ml_model=(
            transcription.model
        ),
    )