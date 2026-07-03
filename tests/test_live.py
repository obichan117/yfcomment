"""Live network tests against finance.yahoo.co.jp — no mocking.

Marked slow; run with `uv run pytest -m slow`.
Expectations are dynamic (relative dates, uniqueness/ordering checks) rather
than hardcoded dates or comment numbers, since forum content changes daily.
"""

from datetime import datetime, timedelta

import pytest

from yfcomment import get_comments

pytestmark = pytest.mark.slow


def test_get_comments_default_limit():
    comments = get_comments("285A", limit=25)
    assert len(comments) == 25

    numbers = [c.number for c in comments]
    assert len(set(numbers)) == len(numbers)
    assert all(numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1))

    cutoff = datetime.now() - timedelta(days=90)
    for c in comments:
        assert c.posted_at >= cutoff


def test_get_comments_crosses_pagination_boundary():
    comments = get_comments("285A", limit=60)
    assert len(comments) == 60

    numbers = [c.number for c in comments]
    assert len(set(numbers)) == len(numbers)
    assert all(numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1))


def test_get_comments_different_code():
    comments = get_comments("7203", limit=5)
    assert len(comments) == 5
