# yfcomment

CLI (`yfc`) + Python API that shows the latest comments from a Japanese stock's
Yahoo Finance Japan forum (e.g. https://finance.yahoo.co.jp/quote/285A.T/forum)
as a compact terminal table. Personal tool first; keep it publishable-clean but
no PyPI/MkDocs/CI yet.

## Quick start

```bash
uv sync
uv run yfc 285A                  # latest 20 comments
uv run pytest --tb=short         # fast tests
uv run pytest -m slow            # live network tests
uv run ruff check --select F401,F841
```

## Architecture

```
src/yfcomment/
├── __init__.py        # public API: get_comments(code, limit) -> list[Comment]
├── models.py          # Comment dataclass (public)
├── cli.py             # Typer app; console script `yfc`
└── _internal/
    ├── fetch.py       # I/O only — returns raw HTML/JSON, never parses
    ├── parse.py       # parsing only — raw -> list[Comment], never fetches
    ├── render.py      # list[Comment] -> Rich table
    └── config.yaml    # URLs, endpoint, selectors — site changes edit here, not Python
```

- Fetch/parse separation is a hard rule; config (URLs, selectors, UA, timeouts)
  lives in `_internal/config.yaml`, never as Python literals.
- Stateless by design: every run fetches the latest N. No local storage.
- v1 non-goals: posting/login, watchlists, unread tracking, sentiment analysis,
  archiving, price data.

## Key files

- `docs/research/yahoo-forum-api.md` — the comments JSON API, fully
  reverse-engineered and verified with a plain HTTP client (2026-07-03). Read this
  before touching fetch/parse. Flow: GET forum page once (cookies + embedded JWT)
  → GET `bff-quote-stocks/v1/ajax/bbs/comment` with `x-jwt-token` + `referer` + UA.
  Paginate with inclusive `mid` cursor, dedupe by `part`, max `size=50`.
- `_internal/config.yaml` — endpoint URLs, JWT extraction regexes, UA, timeouts.
- API quirks: `body` is HTML (strip tags, unescape entities); no per-comment
  sentiment (page shows a thread-level poll instead — optional header line);
  `good`/`bad` = はい/いいえ helpful votes.

## Testing

- Live scraping tests marked `@pytest.mark.slow` (no mocks for scrapers).
- Fast parse tests run against a committed HTML/JSON snapshot in `tests/fixtures/`.
- Use dynamic dates, never hardcoded ones.
