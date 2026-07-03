"""yfcomment — Yahoo Finance Japan stock forum comments, as data or in your terminal.

Public API:

    from yfcomment import get_forum, get_comments, get_ranking, Forum, Comment, RankEntry

    forum = get_forum("285A", limit=20)
    comments = get_comments("285A", limit=20)
    ranking = get_ranking("daily", limit=20)
"""

from yfcomment.models import Comment, Forum, RankEntry
from yfcomment._internal.fetch import RANKING_TERMS, fetch_forum, fetch_ranking
from yfcomment._internal.parse import parse_comments, parse_poll, parse_ranking

__all__ = ["Comment", "Forum", "RankEntry", "get_comments", "get_forum", "get_ranking"]


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


def get_ranking(term: str = "daily", limit: int = 20) -> list[RankEntry]:
    """Fetch the BBS comment-count ranking (most-commented stocks).

    `term` is one of "daily", "weekly", "monthly" (daily by default).
    Returns the top `limit` entries. No post counts are exposed by the
    site — entries are ordered by rank, with price and last-forum-activity
    time only.
    """
    if term not in RANKING_TERMS:
        raise ValueError(f"unknown ranking term: {term!r} (expected one of {RANKING_TERMS})")
    raw = fetch_ranking(term, limit=limit)
    return parse_ranking(raw)[:limit]
