from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    source = Column(String(50), nullable=False)

    original_url = Column(String(1000), nullable=False)

    title = Column(String(255))

    artist = Column(String(255))

    duration = Column(Integer)

    processed_audio = Column(
        String(500),
    )
    audio_path = Column(String(500))

    features_path = Column(String(500))

    bpm = Column(Integer)

    key = Column(String(20))

    analysis_status = Column(
    String(30),
    default="pending",
    )

    analysis_completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )