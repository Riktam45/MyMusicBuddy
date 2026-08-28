from sqlalchemy import Column, Float, ForeignKey, Integer

from app.core.database import Base


class Beat(Base):
    __tablename__ = "beats"

    id = Column(Integer, primary_key=True)

    song_id = Column(
        Integer,
        ForeignKey("songs.id"),
        nullable=False,
    )

    beat_time = Column(
        Float,
        nullable=False,
    )