from pydantic import BaseModel


class ScaleRecommendation(BaseModel):
    name: str
    root: str
    notes: list[str]
    score: float
    reason: str