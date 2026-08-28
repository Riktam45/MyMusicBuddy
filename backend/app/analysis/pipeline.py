from app.analysis.context_builder import build_context
from app.analysis.schema import AnalysisResult
from app.ai.full_song_analyzer import FullSongAnalyzer
from app.ai.beat_tracker import detect_beats
from app.ai.scale_schema import ScaleRecommendation


def analyze_song(
    audio_path: str,
) -> AnalysisResult:
    """
    Run the complete MyMusic Buddy song analysis.
    """

    # Build shared audio context
    context = build_context(
        audio_path
    )

    # Run the complete Phase 6 analyzer
    analyzer = FullSongAnalyzer()

    full_result = analyzer.analyze(
        context
    )

    # Beat information is needed by the
    # existing AnalysisResult schema.
    beats = detect_beats(
        context
    )

    # Chord segments
    chord_segments = (
        full_result.chords or []
    )

    # Convert chord segments into a
    # simple chord progression.
    chord_progression = []

    for chord in chord_segments:
        if hasattr(chord, "chord"):
            chord_progression.append(
                chord.chord
            )

    # Convert scale dictionaries into
    # ScaleRecommendation objects.
    scale_recommendations = []

    for scale in (
        full_result.scales or []
    ):
        if isinstance(
            scale,
            ScaleRecommendation,
        ):
            scale_recommendations.append(
                scale
            )
            continue

        scale_recommendations.append(
            ScaleRecommendation(
                name=scale["name"],
                root=scale["root"],
                notes=scale["notes"],
                score=scale.get(
                    "score",
                    1.0,
                ),
                reason=scale.get(
                    "reason",
                    "Compatible with detected song key.",
                ),
            )
        )

    arpeggios = []
    
    for item in (
        full_result.arpeggios or []
    ):
        if isinstance(item, dict):
            arpeggio = item.get(
                "arpeggio"
            )
    
            if arpeggio:
                arpeggios.append(
                    arpeggio
                )
    
        else:
            arpeggios.append(item)    

    return AnalysisResult(
        bpm=full_result.bpm,
        key=full_result.key,
        beats=beats,
        chord_segments=chord_segments,
        chord_progression=chord_progression,
        scale_recommendations=(
            scale_recommendations
        ),
        intervals=(
            full_result.intervals or []
        ),
        arpeggios=arpeggios,
        confidence={},
    )