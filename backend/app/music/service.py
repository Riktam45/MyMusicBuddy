from sqlalchemy.orm import Session

from app.music.model import Song
from app.music.schema import SongCreate
from app.music.utils import detect_platform
from app.music.downloader import download_audio
from app.music.audio_processor import convert_to_wav


def create_song(
    db: Session,
    song: SongCreate,
    user_id: int,
):
    """
    Download a music URL, process the audio,
    and save the song information.
    """

    platform = detect_platform(song.url)

    if platform not in [
        "youtube",
        "youtube_music",
    ]:
        raise ValueError(
            "Currently only YouTube and YouTube Music URLs are supported."
        )

    audio_path, info = download_audio(
        song.url
    )

    processed_audio = convert_to_wav(
        audio_path
    )

    title = info.get("title")
    artist = info.get("uploader")
    duration = info.get("duration")

    db_song = Song(
        user_id=user_id,
        source=platform,
        original_url=song.url,
        title=title,
        artist=artist,
        duration=duration,
        audio_path=audio_path,
        processed_audio=processed_audio,
    )

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    return db_song