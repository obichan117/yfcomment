# TASK-006: Thread sentiment poll header (optional)

**Status**: done
**Priority**: low
**Delegation**: implementer

## Description
The forum page (already fetched for the JWT) embeds a thread-level sentiment poll
(強く買いたい 26.83%、買いたい 2.44%、様子見 …) in an `_EvaluationGraph` element.
Parse it in `parse.py` from the `page_html` that `fetch_forum` returns, and print it
as a single colored line above the table (skip silently when absent — graceful
degradation, this must never break the comment listing).

Add a `--no-poll` flag to hide it. In `--json` mode include it as
`{"poll": {...} | null, "comments": [...]}` — note this changes the current
top-level-array JSON shape; update TASK-005's CLI smoke test expectation accordingly.

## Acceptance Criteria
- [x] `yfc 285A` shows e.g. `強く買いたい 27% ・ 買いたい 2% ・ …` above the table (live)
- [x] Poll parse failure or absence degrades to no header, exit 0
- [x] `--no-poll` hides it; `--json` includes `poll` key
- [x] Fast test with a saved HTML snippet fixture

## Design (decided by main session — follow exactly)
Public API in `__init__.py`:
- New `get_forum(code, limit=20) -> Forum` — fetches once, returns poll + comments.
- `get_comments(code, limit=20)` stays, implemented as `get_forum(...).comments`.
- Export `Forum` alongside `Comment`.

`models.py`: add frozen dataclass `Forum` with fields `code: str`,
`poll: dict[str, float] | None` (label → percent, insertion order = site order,
e.g. `{"強く買いたい": 26.83, "買いたい": 2.44, ...}`), `comments: list[Comment]`.
Give it `to_dict()` → `{"code", "poll", "comments": [c.to_dict(), ...]}`.

`parse.py`: add `parse_poll(page_html) -> dict[str, float] | None` — extract from the
`_EvaluationGraph` element (labels + percentages appear as text like
`強く買いたい 26.83%、買いたい 2.44%、…`). Returns `None` on any parse failure
(graceful degradation — wrap in try/except, never raise).

`cli.py`: table mode prints the poll as one line above the table
(`強く買いたい 27% ・ 買いたい 2% ・ …`, percentages rounded to int) unless
`--no-poll` or poll is None. `--json` now prints `Forum.to_dict()`
(shape: `{"code", "poll", "comments"}`).

`tests/test_cli.py`: update the JSON smoke test for the new shape
(`d["comments"]` length 5, `"poll" in d`). Add a fast test for `parse_poll` using a
saved HTML snippet fixture `tests/fixtures/evaluation_graph.html` (cut the relevant
element out of a live page fetch).

## Notes
Do after TASK-004. Selector/percentages format documented in
`docs/research/yahoo-forum-api.md` (§ Notes for implementation).
