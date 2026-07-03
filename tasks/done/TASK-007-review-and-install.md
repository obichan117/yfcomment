# TASK-007: Final review + local install

**Status**: done
**Priority**: medium
**Delegation**: main

## Description
Review all delegated diffs, run the Post-Implementation Checklist (tests, ruff,
exports in `__init__.py`, README/CLAUDE.md accuracy), verify the real CLI end-to-end
on 2–3 stocks, then install globally.

## Acceptance Criteria
- [x] `git diff` of every delegated task reviewed by main session
- [x] Full checklist green (pytest incl. `-m slow`, ruff, docs accurate)
- [x] `uv tool install .` → `yfc 285A` works from any directory
- [x] Commit suggested to user (no auto-commit)

## Notes
Decision: TASK-006 shipped in v0.1 (avoids a later breaking change to the --json shape).
