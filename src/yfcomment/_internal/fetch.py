"""I/O layer: talks to finance.yahoo.co.jp, returns raw content only.

Rules (see .claude/CLAUDE.md):
- Returns raw content (str HTML or dict JSON). No parsing into Comment here.
- URLs, headers, and timeouts come from config.yaml, not literals.
"""

from pathlib import Path

import yaml

_CONFIG = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())


def normalize_code(code: str) -> str:
    """"285A" -> "285A.T"; leaves an existing market suffix untouched."""
    if "." in code:
        return code
    return code + _CONFIG["forum"]["default_market_suffix"]


def fetch_forum(code: str, limit: int = 20) -> str | dict:
    """Fetch raw forum content for a stock code.

    Uses the JSON API from config.yaml when known; otherwise fetches the
    server-rendered forum page HTML (~50 newest comments).
    """
    raise NotImplementedError("implemented in task: fetch/parse")
