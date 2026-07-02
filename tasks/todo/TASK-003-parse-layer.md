# TASK-003: Parse layer (`_internal/parse.py`)

**Status**: todo
**Priority**: high
**Delegation**: implementer

## Description
Implement `parse_comments(raw) -> list[Comment]` turning the dict from
`fetch_forum()` into `Comment` objects (see `models.py`). No network access.
Develop against `tests/fixtures/comment_api_response.json` (note: the fixture is a
single raw API response — its items live at `response.items`; `fetch_forum` hands
parse a merged `{"items": [...]}` dict).

Field mapping (details in `docs/research/yahoo-forum-api.md`):
- `part` → `number`; `dispname` → `username`; `good`/`bad` → `helpful_yes`/`helpful_no`
- `postDate` (`"2026/7/3 7:32"`) → `datetime` (JST naive is fine)
- `body` → `text`: strip HTML tags (`<span data-themeid>`, `<a>`) and unescape
  entities (`&hellip;` etc.). Use `html.unescape` + BeautifulSoup `.get_text()`.
- `sentiment` → `None` (not provided by this API)
- `url` → `None` for now (no per-comment permalink identified)

Sort output newest first by `number`.

## Acceptance Criteria
- [ ] Parsing the fixture yields 20 `Comment`s with correct number/username/votes
- [ ] `text` contains no `<`, `>`, or HTML entities for every fixture item
- [ ] `posted_at` is a real `datetime` matching the fixture's `postDate`
- [ ] No `httpx`/network imports in parse.py
- [ ] `uv run ruff check --select F401,F841` clean

## Notes
Runs fully offline — parallelizable with TASK-002.
