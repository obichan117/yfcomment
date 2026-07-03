# TASK-002: Fetch layer (`_internal/fetch.py`)

**Status**: done
**Priority**: high
**Delegation**: implementer

## Description
Implement `fetch.py` per the contract in `docs/research/yahoo-forum-api.md` (read it
first) and `_internal/config.yaml`. I/O only — no parsing into `Comment` here.

Required functions:
- `normalize_code(code) -> str` — already stubbed: append `.T` when no suffix.
- `fetch_forum(code, limit=20) -> dict` — full flow:
  1. `httpx.Client` with cookie persistence, UA and timeout from config.yaml.
  2. GET `page_url` (code WITH suffix) → extract JWT via `jwt_pattern`, fall back to
     `jwt_fallback_pattern`. Raise a clear error naming the URL if neither matches.
  3. GET `api_url` (code WITHOUT suffix) with headers `x-jwt-token`, `referer`
     (= page URL), UA. Page with inclusive `mid` cursor while collected < limit
     (`size` = min(limit remaining, `max_page_size`)); merge raw item dicts,
     dedupe by `part`.
  4. Return the merged raw response: `{"items": [...], "threadId": ..., "totalSize": ...}`.
- Also return/expose the raw page HTML for the optional sentiment-poll feature
  (TASK-006): include it as `{"page_html": ...}` in the returned dict.

## Acceptance Criteria
- [x] `fetch_forum("285A", limit=20)` returns ≥20 raw items (live)
- [x] `fetch_forum("285A", limit=120)` paginates: ≥120 unique `part` values (live)
- [x] Bare numeric codes work: `fetch_forum("7203", limit=5)` (live)
- [x] No parsing/Comment construction; no config literals in Python
- [x] `uv run ruff check --select F401,F841` clean

## Notes
API returns 400 when any of the three headers is missing — do not "simplify" them away.
