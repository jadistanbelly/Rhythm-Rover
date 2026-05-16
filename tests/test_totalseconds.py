import pytest

from py_functions.totalseconds import totalseconds


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("7", 7),
        ("01:02", 62),
        ("1:02:03", 3723),
    ],
)
def test_totalseconds_parses_supported_formats(value, expected):
    assert totalseconds(value) == expected


@pytest.mark.parametrize("value", ["", "-1", "1:-2", "1:99", "1:2:3:4", "abc"])
def test_totalseconds_rejects_invalid_formats(value):
    with pytest.raises(ValueError):
        totalseconds(value)
