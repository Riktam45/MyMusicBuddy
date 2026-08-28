from pydantic import BaseModel


class FretPosition(BaseModel):
    string: int
    fret: int
    note: str


class FretboardRequest(BaseModel):
    root: str
    scale: str
    notes: list[str]


class FretboardResult(BaseModel):
    root: str
    scale: str
    positions: list[FretPosition]