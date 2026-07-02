"""Parsing layer: raw HTML/JSON -> list[Comment]. No network access here."""

from yfcomment.models import Comment


def parse_comments(raw: str | dict) -> list[Comment]:
    """Parse raw forum content (JSON dict or HTML str) into Comments, newest first."""
    raise NotImplementedError("implemented in task: fetch/parse")
