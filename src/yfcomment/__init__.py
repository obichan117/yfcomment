"""yfcomment — Yahoo Finance Japan stock forum comments, as data or in your terminal.

Public API:

    from yfcomment import get_comments, Comment

    comments = get_comments("285A", limit=20)
"""

from yfcomment.models import Comment
from yfcomment._internal.fetch import fetch_forum
from yfcomment._internal.parse import parse_comments

__all__ = ["Comment", "get_comments"]


def get_comments(code: str, limit: int = 20) -> list[Comment]:
    """Return the latest ``limit`` comments for a stock code (e.g. "285A", "7203").

    The ".T" market suffix is appended automatically when missing.
    Comments are ordered newest first.
    """
    raw = fetch_forum(code, limit=limit)
    return parse_comments(raw)[:limit]
