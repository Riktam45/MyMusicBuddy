from urllib.parse import urlparse


def detect_platform(url: str) -> str:
    """
    Detect the supported music platform from a URL.
    """

    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
    except Exception:
        return "unknown"

    if hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "www.music.youtube.com",
    }:
        if hostname in {
            "music.youtube.com",
            "www.music.youtube.com",
        }:
            return "youtube_music"

        return "youtube"

    if hostname in {
        "youtu.be",
        "www.youtu.be",
    }:
        return "youtube"

    return "unknown"