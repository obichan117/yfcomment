"""I/O layer: talks to finance.yahoo.co.jp, returns raw content only.

Rules (see .claude/CLAUDE.md):
- Returns raw content (str HTML or dict JSON). No parsing into Comment here.
- URLs, headers, and timeouts come from config.yaml, not literals.
"""

import json
import re
from pathlib import Path

import httpx
import yaml

_CONFIG = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())

RANKING_TERMS: list[str] = _CONFIG["ranking"]["terms"]


def normalize_code(code: str) -> str:
    """"285A" -> "285A.T"; leaves an existing market suffix untouched."""
    if "." in code:
        return code
    return code + _CONFIG["forum"]["default_market_suffix"]


def _extract_jwt(page_html: str, page_url: str) -> str:
    """Pull the short-lived JWT out of the forum page HTML."""
    match = re.search(_CONFIG["forum"]["jwt_pattern"], page_html)
    if match:
        return match.group(1)
    match = re.search(_CONFIG["forum"]["jwt_fallback_pattern"], page_html)
    if match:
        return match.group(0)
    raise ValueError(f"could not extract JWT token from forum page: {page_url}")


def fetch_forum(code: str, limit: int = 20) -> dict:
    """Fetch raw forum content for a stock code.

    Flow: GET the server-rendered forum page once (sets cookies, embeds the
    JWT), then page through the comments JSON API with the inclusive `mid`
    cursor until `limit` unique items (by `part`) are collected.

    Returns the merged raw response plus the raw page HTML (needed for the
    optional sentiment-poll feature): {"items", "threadId", "totalSize",
    "page_html"}.
    """
    forum_cfg = _CONFIG["forum"]
    http_cfg = _CONFIG["http"]

    page_code = normalize_code(code)
    api_code = page_code.split(".")[0]

    page_url = forum_cfg["page_url"].format(code=page_code)
    user_agent = http_cfg["user_agent"]
    timeout = http_cfg["timeout_seconds"]
    max_page_size = forum_cfg["max_page_size"]

    with httpx.Client(
        headers={"user-agent": user_agent}, timeout=timeout, follow_redirects=True
    ) as client:
        page_resp = client.get(page_url)
        page_resp.raise_for_status()
        page_html = page_resp.text

        jwt_token = _extract_jwt(page_html, page_url)

        headers = {
            "x-jwt-token": jwt_token,
            "referer": page_url,
            "user-agent": user_agent,
        }

        items_by_part: dict[int, dict] = {}
        thread_id = None
        total_size = None
        mid = None

        while len(items_by_part) < limit:
            remaining = limit - len(items_by_part)
            # `mid` is an inclusive cursor: every page after the first re-returns
            # the item at `mid` (already collected), so ask for one extra to make
            # up for that guaranteed duplicate.
            size = min(remaining + 1 if mid is not None else remaining, max_page_size)
            url = forum_cfg["api_url"].format(code=api_code, size=size)
            if mid is not None:
                url += f"&mid={mid}"

            api_resp = client.get(url, headers=headers)
            api_resp.raise_for_status()
            payload = api_resp.json()["response"]

            thread_id = payload["threadId"]
            total_size = payload["totalSize"]
            page_items = payload["items"]

            if not page_items:
                break

            new_count = 0
            for item in page_items:
                if item["part"] not in items_by_part:
                    items_by_part[item["part"]] = item
                    new_count += 1

            next_mid = min(item["part"] for item in page_items)
            if next_mid == mid or new_count == 0:
                break
            mid = next_mid

    items = sorted(items_by_part.values(), key=lambda item: item["part"], reverse=True)

    return {
        "items": items,
        "threadId": thread_id,
        "totalSize": total_size,
        "page_html": page_html,
    }


def fetch_ranking(term: str, limit: int) -> dict:
    """Fetch raw BBS comment-ranking content for a term ("daily"/"weekly"/"monthly").

    Flow: GET the server-rendered ranking pages (no JWT/cookies needed),
    starting at page 1, extracting the embedded `window.__PRELOADED_STATE__`
    JSON from each page's HTML and pulling out `mainRankingList`. Stops once
    `limit` results have been collected or all pages have been fetched
    (never requests a page beyond `totalPage`).

    Returns the merged raw results plus size: {"results", "totalSize", "term"}.
    """
    ranking_cfg = _CONFIG["ranking"]
    http_cfg = _CONFIG["http"]

    market = ranking_cfg["default_market"]
    state_prefix = ranking_cfg["state_prefix"]
    user_agent = http_cfg["user_agent"]
    timeout = http_cfg["timeout_seconds"]

    collected: list[dict] = []
    total_size = None
    total_page = 1
    page = 1

    with httpx.Client(
        headers={"user-agent": user_agent}, timeout=timeout, follow_redirects=True
    ) as client:
        while len(collected) < limit and page <= total_page:
            url = ranking_cfg["page_url"].format(market=market, term=term, page=page)
            resp = client.get(url)
            resp.raise_for_status()
            html = resp.text

            idx = html.find(state_prefix)
            if idx == -1:
                raise ValueError(f"could not find embedded ranking state in page: {url}")

            state = json.JSONDecoder().raw_decode(html[idx + len(state_prefix) :])[0]
            ranking_list = state["mainRankingList"]
            paging = ranking_list["paging"]

            collected.extend(ranking_list["results"])
            total_size = paging["totalSize"]
            total_page = paging["totalPage"]
            page += 1

    return {
        "results": collected,
        "totalSize": total_size,
        "term": term,
    }
