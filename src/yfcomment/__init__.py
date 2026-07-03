"""yfcomment — Yahoo Finance Japan stock forum comments, as data or in your terminal.

Public API:

    from yfcomment import get_forum, get_comments, Forum, Comment

    forum = get_forum("285A", limit=20)
    comments = get_comments("285A", limit=20)
"""

from yfcomment.models import Comment, Forum
from yfcomment._internal.fetch import fetch_forum
from yfcomment._internal.parse import parse_comments, parse_poll

__all__ = ["Comment", "Forum", "get_comments", "get_forum"]


def get_forum(code: str, limit: int = 20) -> Forum:
    """Fetch a stock's forum thread: the sentiment poll header plus the
    latest ``limit`` comments (e.g. "285A", "7203").

    The ".T" market suffix is appended automatically when missing.
    Comments are ordered newest first. ``poll`` is None when the page has no
    poll or it could not be parsed (never raises for this reason).
    """
    raw = fetch_forum(code, limit=limit)
    return Forum(
        code=code,
        poll=parse_poll(raw["page_html"]),
        comments=parse_comments(raw)[:limit],
    )


def get_comments(code: str, limit: int = 20) -> list[Comment]:
    """Return the latest ``limit`` comments for a stock code (e.g. "285A", "7203").

    The ".T" market suffix is appended automatically when missing.
    Comments are ordered newest first.
    """
    return get_forum(code, limit=limit).comments
