from dataclasses import dataclass


@dataclass
class NoteEvent:
    """
    Represents a detected musical note.
    """

    time: float
    frequency: float
    pitch: int
    note: str
    octave: int
    confidence: float