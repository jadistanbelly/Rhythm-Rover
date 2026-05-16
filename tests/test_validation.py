import pytest

from py_functions.validation import normalize_clip_request


def test_normalize_clip_request_caps_duration_to_ten_seconds():
    url, start, end = normalize_clip_request("https://youtu.be/example", "5", "99")

    assert url == "https://youtu.be/example"
    assert start == 5
    assert end == 15


@pytest.mark.parametrize("url", ["file:///tmp/audio.mp3", "ftp://example.com/file.mp3", "not-a-url"])
def test_normalize_clip_request_rejects_non_http_urls(url):
    with pytest.raises(ValueError, match="http or https"):
        normalize_clip_request(url, "1", "3")


@pytest.mark.parametrize(("start", "end"), [("5", "5"), ("6", "5")])
def test_normalize_clip_request_rejects_empty_or_reversed_ranges(start, end):
    with pytest.raises(ValueError, match="after start"):
        normalize_clip_request("https://example.com/audio", start, end)
