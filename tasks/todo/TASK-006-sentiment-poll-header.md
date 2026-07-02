# TASK-006: Thread sentiment poll header (optional)

**Status**: todo
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
- [ ] `yfc 285A` shows e.g. `強く買いたい 27% ・ 買いたい 2% ・ …` above the table (live)
- [ ] Poll parse failure or absence degrades to no header, exit 0
- [ ] `--no-poll` hides it; `--json` includes `poll` key
- [ ] Fast test with a saved HTML snippet fixture

## Notes
Do after TASK-004. Selector/percentages format documented in
`docs/research/yahoo-forum-api.md` (§ Notes for implementation).
