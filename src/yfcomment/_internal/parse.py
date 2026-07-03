"""Parsing layer: raw HTML/JSON -> list[Comment]. No network access here."""

import re
from datetime import datetime
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

from yfcomment.models import Comment

_CONFIG = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())

_POST_DATE_FORMAT = "%Y/%m/%d %H:%M"

# The forum page renders the thread-level sentiment poll ("みんなの評価") as an
# `_EvaluationGraph` component whose class-configured child holds a plain-text,
# screen-reader-only summary like "強く買いたい 26.83%、買いたい 2.44%、…" — easier
# and more stable to parse than the visual graph's split label/value spans.
_POLL_CLASS_PATTERN = re.compile("^" + re.escape(_CONFIG["selectors"]["poll_class_prefix"]))
_POLL_ITEM_PATTERN = re.compile(r"([^\s\d、]+)\s*([\d.]+)%")


def _clean_body(body: str) -> str:
    """Strip HTML tags and unescape entities from a raw comment body."""
    return BeautifulSoup(body, "lxml").get_text()


def parse_comments(raw: dict) -> list[Comment]:
    """Parse a merged forum JSON dict (as returned by `fetch_forum`) into
    Comments, newest first (by `number`).
    """
    comments = [
        Comment(
            number=item["part"],
            posted_at=datetime.strptime(item["postDate"], _POST_DATE_FORMAT),
            username=item["dispname"],
            text=_clean_body(item["body"]),
            sentiment=None,
            helpful_yes=item.get("good", 0),
            helpful_no=item.get("bad", 0),
            url=None,
        )
        for item in raw["items"]
    ]
    comments.sort(key=lambda c: c.number, reverse=True)
    return comments


def parse_poll(page_html: str) -> dict[str, float] | None:
    """Parse the thread-level sentiment poll ("みんなの評価") from a forum page's
    raw HTML, e.g. {"強く買いたい": 26.83, "買いたい": 2.44, ...}, in site order.

    Best-effort: returns None on any failure (missing element, unexpected
    markup, etc.) rather than raising — the poll is a nice-to-have that must
    never break the comment listing.
    """
    try:
        soup = BeautifulSoup(page_html, "lxml")
        summary = soup.find(class_=_POLL_CLASS_PATTERN)
        if summary is None:
            return None
        pairs = _POLL_ITEM_PATTERN.findall(summary.get_text())
        if not pairs:
            return None
        return {label: float(percent) for label, percent in pairs}
    except Exception:
        return None
