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
