"""Fast, offline tests for the parsing layer.

Uses a committed raw API response fixture — no network access here.
"""

import json
from datetime import datetime
from pathlib import Path

from yfcomment._internal.parse import parse_comments, parse_poll

_FIXTURE = Path(__file__).parent / "fixtures" / "comment_api_response.json"
_POLL_FIXTURE = Path(__file__).parent / "fixtures" / "evaluation_graph.html"


def _load_raw() -> dict:
    data = json.loads(_FIXTURE.read_text())
    return {"items": data["response"]["items"]}


def test_parse_returns_expected_count():
    comments = parse_comments(_load_raw())
    assert len(comments) == 20


def test_parse_field_types():
    comments = parse_comments(_load_raw())
    for c in comments:
        assert isinstance(c.number, int)
        assert isinstance(c.posted_at, datetime)
        assert isinstance(c.username, str) and c.username
        assert isinstance(c.helpful_yes, int)
        assert isinstance(c.helpful_no, int)


def test_parse_newest_first():
    comments = parse_comments(_load_raw())
    numbers = [c.number for c in comments]
    assert numbers == sorted(numbers, reverse=True)
    assert all(numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1))


def test_parse_text_is_html_free():
    comments = parse_comments(_load_raw())
    for c in comments:
        assert "<" not in c.text
        assert ">" not in c.text
        assert "&hellip;" not in c.text


def test_comment_to_dict_roundtrips_through_json():
    comments = parse_comments(_load_raw())
    for c in comments:
        d = c.to_dict()
        encoded = json.dumps(d)
        decoded = json.loads(encoded)
        assert decoded["posted_at"] == c.posted_at.isoformat()
        assert decoded["number"] == c.number
        assert decoded["username"] == c.username
        assert decoded["text"] == c.text


def test_parse_poll_from_fixture():
    poll = parse_poll(_POLL_FIXTURE.read_text())
    assert poll is not None
    assert list(poll.keys()) == ["強く買いたい", "買いたい", "様子見", "売りたい", "強く売りたい"]
    assert all(isinstance(v, float) for v in poll.values())
    assert poll["買いたい"] == 6.7


def test_parse_poll_absent_returns_none():
    assert parse_poll("<html><body>no poll here</body></html>") is None


def test_parse_poll_never_raises_on_garbage():
    assert parse_poll("") is None
    assert parse_poll("<<<not even html") is None
