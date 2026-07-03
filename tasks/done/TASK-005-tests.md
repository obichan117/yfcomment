# TASK-005: Test suite

**Status**: done
**Priority**: medium
**Delegation**: implementer

## Description
Per project testing rules (`.claude/CLAUDE.md`): live tests for scraping (no mocks),
fast offline tests for parsing.

- `tests/test_parse.py` (fast): parse `tests/fixtures/comment_api_response.json`
  (items at `response.items` — wrap as `{"items": ...}` to match `parse_comments`
  input); assert count, field types, newest-first order, HTML-free text,
  `to_dict()` round-trips through `json.dumps`.
- `tests/test_live.py` (`@pytest.mark.slow`): `get_comments("285A", limit=25)`
  returns 25 with sane fields; `limit=60` crosses one pagination boundary and stays
  deduped/sorted; `get_comments("7203")` works. Use dynamic expectations
  (e.g. `posted_at` within the last 90 days), never hardcoded dates or comment numbers.
- CLI smoke (`@pytest.mark.slow`): run `yfc 285A --json -n 5` via `subprocess`,
  assert exit 0 and valid JSON of length 5.

## Acceptance Criteria
- [x] `uv run pytest --tb=short -m "not slow"` passes offline in <5s
- [x] `uv run pytest -m slow --tb=short` passes (live)
- [x] No mocking of HTTP anywhere
- [x] `uv run ruff check --select F401,F841` clean

## Notes
Depends on TASK-002/003/004.
