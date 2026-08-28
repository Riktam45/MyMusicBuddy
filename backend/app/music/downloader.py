from pathlib import Path

import yt_dlp


AUDIO_DIR = Path("storage/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

MAX_DURATION_SECONDS = 15 * 60
MAX_FILE_SIZE = 150 * 1024 * 1024


def download_audio(url: str):
    """
    Download audio from a supported URL.

    Limits:
    - Maximum duration: 15 minutes
    - Maximum file size: 150 MB
    """

    output_template = str(
        AUDIO_DIR / "%(id)s.%(ext)s"
    )

    def duration_filter(info, *, incomplete):
        duration = info.get("duration")

        if duration is not None and duration > MAX_DURATION_SECONDS:
            return (
                "Audio is too long. "
                "Maximum allowed duration is 15 minutes."
            )

        return None

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": False,
        "noplaylist": True,

        # Reject files when yt-dlp knows their size
        # before downloading.
        "max_filesize": MAX_FILE_SIZE,

        # Reject long videos before downloading.
        "match_filter": duration_filter,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            url,
            download=True,
        )

        filename = ydl.prepare_filename(info)

    downloaded_file = Path(filename)

    if not downloaded_file.exists():
        raise ValueError(
            "The audio could not be downloaded."
        )

    if downloaded_file.stat().st_size > MAX_FILE_SIZE:
        downloaded_file.unlink(missing_ok=True)

        raise ValueError(
            "Downloaded audio is too large. "
            "Maximum allowed size is 150 MB."
        )

    duration = info.get("duration")

    if (
        duration is not None
        and duration > MAX_DURATION_SECONDS
    ):
        downloaded_file.unlink(missing_ok=True)

        raise ValueError(
            "Audio is too long. "
            "Maximum allowed duration is 15 minutes."
        )

    return str(downloaded_file), info