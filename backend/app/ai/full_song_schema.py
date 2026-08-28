from pydantic import BaseModel
from typing import Any
from pydantic import BaseModel, Field

class FullSongAnalysis(BaseModel):
    bpm: float | None = None
    key: str | None = None

    notes: list[Any] = Field(
        default_factory=list
    )

    chords: list[Any] = Field(
        default_factory=list
    )

    progression: list[Any] = Field(
        default_factory=list
    )

    scales: list[Any] = Field(
        default_factory=list
    )

    intervals: list[Any] = Field(
        default_factory=list
    )

    arpeggios: list[Any] = Field(
        default_factory=list
    )

    pitch: list[Any] = Field(
        default_factory=list
    )

