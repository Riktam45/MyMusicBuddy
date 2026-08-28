from pydantic import BaseModel


class HybridNoteEvent(BaseModel):
    note: str
    octave: int
    midi: int

    start: float
    end: float
    duration: float

    confidence: float

    source: str