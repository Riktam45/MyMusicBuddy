from pydantic import BaseModel

from app.ai.ml_note_schema import MLNoteEvent


class HybridAnalysisResult(BaseModel):

    bpm: float | None = None

    key: str | None = None

    beats: list[float] = []

    ml_notes: list[MLNoteEvent] = []

    ml_chord_candidates: list[str] = []

    ml_pitch_classes: list[int] = []

    ml_intervals: list[dict] = []

    ml_arpeggio_context: dict = {}

    ml_model: str | None = None