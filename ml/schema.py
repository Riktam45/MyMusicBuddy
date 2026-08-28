from pydantic import BaseModel


class MLNoteEvent(BaseModel):
    pitch: int
    start: float
    end: float
    velocity: int | None = None


class MLTranscriptionResult(BaseModel):
    notes: list[MLNoteEvent]
    model: str
    confidence: float | None = None