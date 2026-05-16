from urllib.parse import urlparse

from py_functions.totalseconds import totalseconds

MAX_CLIP_SECONDS = 10


def normalize_clip_request(video_url: str, start: str, end: str) -> tuple[str, int, int]:
    """Validate user clip input and cap the requested clip length."""
    parsed = urlparse(video_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Audio URL must use http or https")

    start_seconds = totalseconds(start)
    end_seconds = totalseconds(end)
    if end_seconds <= start_seconds:
        raise ValueError("Clip end must be after start")

    if end_seconds - start_seconds > MAX_CLIP_SECONDS:
        end_seconds = start_seconds + MAX_CLIP_SECONDS

    return video_url.strip(), start_seconds, end_seconds
