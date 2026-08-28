from pydantic import BaseModel


class MLNoteEvent(BaseModel):
    note: str
    octave: int
    midi: int
    start: float
    end: float
    duration: float
    confidence: float