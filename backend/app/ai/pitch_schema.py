from pydantic import BaseModel


class PitchResult(BaseModel):
    frequency: float
    midi: int
    note: str
    octave: int
    note_with_octave: str
    confidence: float