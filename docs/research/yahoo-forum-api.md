# Yahoo Finance Japan — forum comments API (reverse-engineered)

Status: **captured and verified with a plain HTTP client** (2026-07-03, via headless
Chromium network capture + urllib reproduction). No browser needed at runtime.

## Endpoint

```
GET https://finance.yahoo.co.jp/bff-quote-stocks/v1/ajax/bbs/comment?code={CODE}&size={N}[&mid={CURSOR}]
```

- `code` — **bare** stock code, no market suffix: `285A`, `7203` (the page URL uses
  `285A.T`, the API does not).
- `size` — comments per call. 20 is what the site uses; **50 verified working**.
- `mid` — pagination cursor, a comment number (`part`). Omit for the newest page.
  **Inclusive**: `mid=1273352` returns items starting at part `1273352` — dedupe by
  `part` when paging (comment numbers also have gaps from deletions).

### Required headers (all three, else HTTP 400)

| Header | Value |
|---|---|
| `x-jwt-token` | short-lived JWT extracted from the forum page HTML (see below) |
| `referer` | `https://finance.yahoo.co.jp/quote/{CODE}.T/forum` |
| `user-agent` | any realistic browser UA |

Cookies (`A`/`XA`/`B`/`XB`) are set by the page fetch; keep a cookie jar across the
two requests (verified working with them; not tested without).

### Token acquisition

The JWT sits in the forum page HTML inside escaped embedded JSON as
`jwtToken\":\"eyJ...\"`. Payload is only `{"exp": <unix>}` (~2h validity, HS256).
Flow: 1 GET of the page per CLI run → regex out the token → call the API.

Extraction regex (against raw HTML): `jwtToken\\":\\"([^"\\]+)`
Fallback: `eyJhbGciOiJIUzI1NiJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`

## Response shape

```json
{
  "isSuccess": true,
  "response": {
    "categoryId": "1835673",
    "threadId": "3cbb9fa0a454194f0d07b74acd145222",
    "totalSize": 1273235,          // ≈ newest comment number, not an exact count
    "isError": false,
    "items": [
      {
        "part": 1273154,           // comment number (No.xxxxxxx), descending
        "userId": "d5e3b9bd...",   // stable hash
        "userIcon": "https://s.yimg.jp/...png",
        "dispname": "しろうと",     // display name (not masked, unlike page render)
        "infoLink": "https://finance.yahoo.co.jp/cm/personal/history/comment?user=...",
        "title": "アップルが中国製メモリーの調達&hellip;",   // truncated, HTML entities
        "body": "<span data-themeid=\"1212\">アップル</span>が...", // HTML: strip tags, unescape entities
        "postDate": "2026/7/3 7:32",
        "good": 8,                 // 「参考になりましたか？」はい
        "bad": 4                   //                       いいえ
      }
    ]
  }
}
```

## Notes for implementation

- `body` is HTML — strip tags (`<span data-themeid>`, `<a>`) and unescape entities
  for terminal display.
- **No per-comment sentiment field.** The 買いたい tags seen on the page are a
  thread-level sentiment poll (e.g. 強く買いたい 26.83%、買いたい 2.44%) rendered in an
  `_EvaluationGraph` element in the page HTML. Optional nice-to-have: parse it from
  the page we already fetch for the JWT and print it as a header line.
  → `Comment.sentiment` will be `None` from this API.
- Comment permalink: `https://finance.yahoo.co.jp/quote/{CODE}.T/forum` has no
  per-comment anchor confirmed yet; `infoLink` links to the author's history instead.

## Capture method (for future re-verification)

Playwright headless Chromium, `page.on("response")` filtered to xhr/fetch, auto-scroll
to trigger infinite scroll. Script preserved conceptually in this doc's git history;
re-run if the endpoint starts returning 400 with valid tokens (signature/header change).

---

# BBS comment ranking (掲示板投稿数ランキング)

Status: **captured and verified with a plain HTTP client** (2026-07-03, headless
capture + urllib reproduction).

## Source

```
GET https://finance.yahoo.co.jp/stocks/ranking/bbs?market=all&term={daily|weekly|monthly}&page={1,2,...}
```

- **No XHR/JSON API exists** — the page fires only ad/tracking requests. The table is
  server-rendered with the data embedded in `window.__PRELOADED_STATE__` (a JS
  assignment inside a `<script>`; parse with `json.JSONDecoder().raw_decode` starting
  after `window.__PRELOADED_STATE__ = `).
- **No JWT, no cookies needed** — a plain GET with a browser User-Agent works
  (verified for monthly page 2).
- 50 rows per page; daily/weekly had `totalSize: 95`, monthly 93 (~2 pages).

## Embedded state shape

`state["mainRankingList"]`:

```json
{
  "results": [
    {
      "rank": "1",                       // string
      "stockCode": "285A",
      "marketName": "東証PRM",
      "stockName": "キオクシアホールディングス(株)",
      "detailLink": "https://finance.yahoo.co.jp/quote/285A.T",
      "bbsUrl": "https://finance.yahoo.co.jp/quote/285A.T/forum",
      "savePrice": "83,300",             // display string, comma separators
      "date": "15:30",                   // price timestamp
      "rankingResult": { "bbsContents": { "updateDateTime": "2026/07/03 19:03" }, ...all-null fields... }
    }
  ],
  "paging": { "hasNext": true, "totalPage": 2, "totalSize": 95, "page": 1, "size": 50,
              "startIndex": 1, "endIndex": 50, "displayedPageNumbers": [1, 2] }
}
```

Notes: the ranking does NOT expose post counts — order + `bbsContents.updateDateTime`
(last BBS activity) is all there is. `savePrice` and `rank` are strings.
Fixture: `tests/fixtures/ranking_state.json` (one real `mainRankingList`, 50 entries).
