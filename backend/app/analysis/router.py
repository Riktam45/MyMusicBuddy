from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.analysis.service import analyze
from app.auth.dependencies import current_user
from app.core.database import get_db
from app.music.model import Song

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post("/{song_id}")
def analyze_music(
    song_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    song = (
        db.query(Song)
        .filter(
            Song.id == song_id,
            Song.user_id == user.id,
        )
        .first()
    )

    if not song:
        raise HTTPException(
            status_code=404,
            detail="Song not found",
        )

    return analyze(db, song)