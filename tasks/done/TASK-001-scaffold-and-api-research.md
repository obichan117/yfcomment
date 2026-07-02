# TASK-001: Scaffold package + reverse-engineer comments API

**Status**: done
**Priority**: high
**Delegation**: main

## Description
Set up the package skeleton (pyproject, src layout, stubs, config.yaml) and capture
the XHR endpoint behind the forum's infinite scroll.

## Acceptance Criteria
- [x] `uv sync` succeeds; `yfc --help` runs; ruff F401/F841 clean
- [x] Endpoint documented in `docs/research/yahoo-forum-api.md`
- [x] `_internal/config.yaml` has real `api_url` + JWT extraction regexes
- [x] Real API response committed as `tests/fixtures/comment_api_response.json`

## Notes
Done 2026-07-03. Captured via headless Playwright network recording, verified with
plain urllib (page fetch → JWT from embedded JSON → API call with x-jwt-token/referer/UA).
