from pydantic import BaseModel


class ArpeggioResult(BaseModel):
    name: str
    root: str
    notes: list[str]
    intervals: list[str]