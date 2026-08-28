from pydantic import BaseModel


class SongCreate(BaseModel):
    url: str


class SongResponse(BaseModel):
    id: int
    source: str
    original_url: str
    title: str | None
    artist: str | None
    processed_audio: str | None
    
    class Config:
        from_attributes = True