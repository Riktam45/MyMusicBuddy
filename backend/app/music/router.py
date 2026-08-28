import wave

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import current_user
from app.core.database import get_db
from app.music.model import Song
from app.music.schema import SongCreate, SongResponse
from app.music.service import create_song
from app.music.audio_processor import convert_to_wav


router = APIRouter(
    prefix="/music",
    tags=["Music"],
)

MAX_UPLOAD_SIZE = 150 * 1024 * 1024
MAX_DURATION_SECONDS = 15 * 60


@router.post(
    "/upload",
    response_model=SongResponse,
)
async def upload_song(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    upload_dir = Path("storage/audio")
    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = Path(
        audio.filename or "uploaded_audio"
    ).name

    audio_path = upload_dir / filename

    total_size = 0

    with open(
        audio_path,
        "wb",
    ) as file:

        while True:
            chunk = await audio.read(1024 * 1024)

            if not chunk:
                break

            total_size += len(chunk)

            if total_size > MAX_UPLOAD_SIZE:
                file.close()

                audio_path.unlink(
                    missing_ok=True
                )

                raise HTTPException(
                    status_code=413,
                    detail=(
                        "File is too large. "
                        "Maximum allowed size is 150 MB."
                    ),
                )

            file.write(chunk)

    if total_size == 0:
        audio_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty.",
        )

    try:
        processed_audio = convert_to_wav(
            str(audio_path)
        )
    except Exception as exc:

        audio_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file is not a valid "
                "supported audio file."
            ),
        ) from exc

    try:
        with wave.open(
            processed_audio,
            "rb",
        ) as wav:

            frames = wav.getnframes()
            sample_rate = wav.getframerate()

            duration = frames / sample_rate

    except Exception as exc:

        audio_path.unlink(
            missing_ok=True
        )

        Path(processed_audio).unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to read the audio duration.",
        ) from exc

    if duration > MAX_DURATION_SECONDS:

        audio_path.unlink(
            missing_ok=True
        )

        Path(processed_audio).unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail=(
                "Audio is too long. "
                "Maximum allowed duration is 15 minutes."
            ),
        )

    db_song = Song(
        user_id=user.id,
        source="upload",
        original_url=filename,
        title=Path(filename).stem,
        artist=None,
        duration=duration,
        audio_path=str(audio_path),
        processed_audio=processed_audio,
    )

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    return db_song


@router.post(
    "/url",
    response_model=SongResponse,
)
def create_song_from_url(
    song: SongCreate,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    try:
        return create_song(
            db=db,
            song=song,
            user_id=user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc