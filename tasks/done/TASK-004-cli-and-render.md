# TASK-004: CLI + terminal rendering (`cli.py`, `_internal/render.py`)

**Status**: done
**Priority**: high
**Delegation**: implementer

## Description
Implement the Typer command body in `cli.py` (flags already declared) and
`build_table()` in `_internal/render.py`.

`render.build_table(comments, *, show_user, show_votes, full_text)` → Rich `Table`:
- Columns in order: time (`MM/dd HH:mm`), 👍/👎 votes (green/red, hidden by
  `--no-votes`), text, user (dim, hidden by `--no-user`). Omit the sentiment column
  for now — the API has no per-comment sentiment.
- Text column: `overflow="ellipsis"` truncation by default; `--full` switches to
  word-wrap (`overflow="fold"`, no truncation).
- Table title: `{CODE} — {n} comments`; use `box.SIMPLE` for a compact look.

`cli.main`:
- `--json`: print `json.dumps([c.to_dict() for c in comments], ensure_ascii=False)`
  to stdout, nothing else (pipe-friendly). Otherwise render the table via
  `rich.console.Console`.
- Errors (network failure, unknown code, no comments) → human message on stderr,
  exit code 1. No tracebacks for expected failures.

## Acceptance Criteria
- [x] `uv run yfc 285A` renders a table of 20 comments (live)
- [x] `-n 50`, `--no-user`, `--no-votes`, `--full` each visibly work (live)
- [x] `uv run yfc 285A --json | python3 -c "import json,sys; json.load(sys.stdin)"` passes
- [x] `uv run yfc NOSUCHCODE1234` exits 1 with a clean one-line error
- [x] `uv run ruff check --select F401,F841` clean

## Notes
Depends on TASK-002 + TASK-003 being merged (needs a working `get_comments`).
Japanese text: Rich handles CJK width — verify columns align with Japanese content.
