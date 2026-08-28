from sqlalchemy.orm import Session

from app.analysis.pipeline import analyze_song
from app.analysis.hybrid_service import run_hybrid_analysis
from app.music.model import Song


def analyze(
    db: Session,
    song: Song,
):
    # --------------------------------
    # 1. Existing DSP analysis
    # --------------------------------

    result = analyze_song(
        song.processed_audio
    )

    # --------------------------------
    # 2. Store core DSP results
    # --------------------------------

    if result.bpm is not None:
        song.bpm = int(
            result.bpm
        )

    song.key = result.key

    # --------------------------------
    # 3. ML + DSP hybrid analysis
    # --------------------------------

    hybrid = run_hybrid_analysis(
        audio_path=song.processed_audio,
        bpm=result.bpm,
        key=result.key,
        beats=result.beats,
    )

    # --------------------------------
    # 4. Add ML results to API result
    # --------------------------------

    result.ml_notes = (
        hybrid.ml_notes
    )

    result.ml_model = (
        hybrid.ml_model
    )

    result.ml_chord_candidates = (
        hybrid.ml_chord_candidates
    )

    result.ml_pitch_classes = (
        hybrid.ml_pitch_classes
    )

    # --------------------------------
    # 5. Mark analysis complete
    # --------------------------------

    song.analysis_status = (
        "completed"
    )

    db.commit()

    db.refresh(song)

    return result