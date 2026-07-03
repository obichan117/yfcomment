# TASK-008: `yfc rank` — BBS comment ranking command

**Status**: done
**Priority**: high
**Delegation**: implementer

## Description
Add `yfc rank`: shows the 掲示板投稿数ランキング (most-commented stocks) from
`https://finance.yahoo.co.jp/stocks/ranking/bbs`. Terms: daily (default), weekly,
monthly. Paginate properly (50/page, ~2 pages). Source is fully documented in
`docs/research/yahoo-forum-api.md` (§ BBS comment ranking) and `_internal/config.yaml`
(`ranking:` section) — read both before coding.

## Design (decided by main session — follow exactly)

**CLI dispatch** — `cli.py` gains a second Typer command, so the app becomes
multi-command. Keep `yfc 285A` working via argv preprocessing:
- Rename the existing command function registration to `@app.command("comments")`
  (function may stay `main` or be renamed `comments`).
- Add `@app.command("rank")`.
- Add a `run()` entry function:
  ```python
  def run() -> None:
      """Entry point: treat `yfc 285A` as `yfc comments 285A`."""
      args = sys.argv[1:]
      if args and args[0] not in {"comments", "rank"} and not args[0].startswith("-"):
          args = ["comments", *args]
      app(args)
  ```
- pyproject.toml: change the console script to `yfc = "yfcomment.cli:run"`.
- Verify all of: `yfc 285A`, `yfc comments 285A`, `yfc rank`, `yfc --help`
  (lists both commands), `yfc rank --help`.

**`rank` command options**:
- `-n/--limit` int, default 20 — number of entries (paginate as needed, cap at
  `paging.totalSize`; fetching more pages than `totalPage` is a bug).
- `-w/--weekly` and `-m/--monthly` flags; both set → error message + exit 2
  (typer.BadParameter). Neither → daily.
- `--json`: `json.dumps({"term": term, "entries": [e.to_dict() for e in entries]}, ensure_ascii=False)`.

**models.py** — frozen dataclass `RankEntry` with `to_dict()`:
`rank: int`, `code: str` (e.g. "285A"), `name: str`, `market: str`,
`price: str | None` (keep the site's display string, e.g. "83,300"),
`updated_at: str | None` (from `rankingResult.bbsContents.updateDateTime`),
`forum_url: str` (from `bbsUrl`).

**fetch.py** — `fetch_ranking(term: str, limit: int) -> dict`:
GET ranking pages (config `ranking.page_url`, market = `default_market`,
page = 1, 2, ... while collected < limit and page <= totalPage), UA/timeout from
config, extract embedded state per page: find `state_prefix`, then
`json.JSONDecoder().raw_decode(html[idx + len(prefix):])`, take `["mainRankingList"]`.
Raise ValueError naming the URL if the marker is missing. Return
`{"results": [merged raw result dicts...], "totalSize": N, "term": term}`.
(Peeking into the state for paging mirrors how comment pagination already reads
the JSON API; keep everything else raw.)

**parse.py** — `parse_ranking(raw: dict) -> list[RankEntry]`: map fields
(`rank` str→int, `stockCode`→code, `stockName`→name, `marketName`→market,
`savePrice`→price via `.get(...) or None`, `updateDateTime` via safe nested
`.get`s→updated_at, `bbsUrl`→forum_url), preserve order, truncate nothing.

**`__init__.py`** — public `get_ranking(term: str = "daily", limit: int = 20) -> list[RankEntry]`
(validate term against config `ranking.terms`, ValueError otherwise); export `RankEntry`.

**render.py** — `build_rank_table(entries) -> Table`: columns
`#` (right-justified), `Code`, `Name` (ratio=1, ellipsis), `Market` (dim),
`Price` (right-justified), `Last post` (dim). box.SIMPLE, expand=True like the
comments table. Title set by cli: `"BBS ranking — {term}"`.

**tests**:
- `tests/test_parse.py` (fast): parse `tests/fixtures/ranking_state.json`
  (a real `mainRankingList` dict; wrap as `{"results": fx["results"], "totalSize":
  fx["paging"]["totalSize"], "term": "daily"}`) → 50 entries, rank 1..50 ints in
  order, first entry has non-empty code/name/forum_url, to_dict round-trips json.
- `tests/test_live.py` (slow): `get_ranking(limit=60)` → exactly 60 entries,
  ranks strictly ascending 1..60 (crosses page boundary);
  `get_ranking("monthly", limit=5)` → 5; `get_ranking("bogus")` raises ValueError.
- `tests/test_cli.py` (slow): `yfc rank --json -n 5` → dict with term "daily" and
  5 entries; `yfc rank -w -m` → exit code 2; regression: `yfc 285A --json -n 5`
  still returns the comments shape (dispatch didn't break).

## Acceptance Criteria
- [x] `yfc rank` shows top-20 daily table (live)
- [x] `yfc rank -n 60 -w` paginates to 60 weekly entries (live)
- [x] `yfc rank -m --json` valid JSON (live)
- [x] `yfc 285A` (no subcommand) still works — dispatch regression-free
- [x] Full suite passes: fast + slow; ruff F401,F841 clean

## Notes
The ranking exposes NO post counts — rank order, price, and last-post time only.
Fixture already committed: `tests/fixtures/ranking_state.json`.
