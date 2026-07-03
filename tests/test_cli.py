"""CLI smoke tests via subprocess — exercises the real network path, no mocks.

Marked slow; run with `uv run pytest -m slow`.
"""

import json
import subprocess

import pytest

pytestmark = pytest.mark.slow


def test_cli_json_output():
    result = subprocess.run(
        ["uv", "run", "yfc", "285A", "--json", "-n", "5"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, dict)
    assert "poll" in data
    assert len(data["comments"]) == 5


def test_cli_bad_code_fails():
    result = subprocess.run(
        ["uv", "run", "yfc", "NOSUCHCODE1234", "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert result.stderr.strip() != ""
    assert result.stdout.strip() == ""


def test_cli_rank_json_output():
    result = subprocess.run(
        ["uv", "run", "yfc", "rank", "--json", "-n", "5"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["term"] == "daily"
    assert len(data["entries"]) == 5


def test_cli_rank_conflicting_terms_exits_2():
    result = subprocess.run(
        ["uv", "run", "yfc", "rank", "-w", "-m"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


def test_cli_comments_dispatch_still_works():
    result = subprocess.run(
        ["uv", "run", "yfc", "285A", "--json", "-n", "5"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "comments" in data
    assert len(data["comments"]) == 5
