from pydantic import BaseModel

from app.ai.chord_schema import ChordSegment
from app.ai.scale_schema import ScaleRecommendation
from app.ai.interval_schema import IntervalResult
from app.ai.arpeggio_schema import ArpeggioResult
from app.ai.ml_note_schema import MLNoteEvent


class AnalysisResult(BaseModel):

    bpm: float | None = None

    key: str | None = None

    beats: list[float] = []

    chord_segments: list[ChordSegment] = []

    chord_progression: list[str] = []

    scales: list[str] = []

    scale_recommendations: list[
        ScaleRecommendation
    ] = []

    intervals: list[IntervalResult] = []

    arpeggios: list[ArpeggioResult] = []

    confidence: dict[str, float] = {}

    ml_notes: list[MLNoteEvent] = []

    ml_model: str | None = None

    ml_chord_candidates: list[str] = []

    ml_pitch_classes: list[int] = []