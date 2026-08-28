from pydantic import BaseModel


class ChordSegment(BaseModel):
    chord: str
    root: str
    type: str
    start: float
    end: float
    confidence: float