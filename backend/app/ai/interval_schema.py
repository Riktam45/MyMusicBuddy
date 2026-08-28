from pydantic import BaseModel


class IntervalResult(BaseModel):
    root: str
    note: str
    semitones: int
    name: str