# yfcomment

Yahoo Finance Japan stock forum comments (掲示板) and BBS rankings in your terminal —
no more scrolling a UI that shows 3 comments per screen.

```console
$ yfc 285A -n 3
強く買いたい 66% ・ 買いたい 6% ・ 様子見 11% ・ 売りたい 3% ・ 強く売りたい 14%
                               285A — 3 comments
  Time            Votes   Comment                                 User
 ──────────────────────────────────────────────────────────────────────
  07/03 18:39   👍0 👎0   何を恐れるの？                          69f*****
  07/03 18:38   👍2 👎1   長期ならもどるね                        58f*****
  07/03 18:38   👍4 👎1   痛くも痒くもない                        okn*****
```

## Install

```bash
uv tool install yfcomment   # or: pip install yfcomment
```

## Highlights

- **`yfc <code>`** — latest comments for any Japanese stock, with the thread's
  sentiment poll as a header line.
- **`yfc rank`** — the 掲示板投稿数ランキング (most-commented stocks), daily,
  weekly, or monthly.
- **JSON everywhere** — every command takes `--json` for pipe-friendly output.
- **A real API underneath** — comments come from Yahoo's JSON backend
  (reverse-engineered, no browser automation), so it's fast; see the
  [research notes](research/yahoo-forum-api.md).
- **Python API** — `get_forum()`, `get_comments()`, `get_ranking()` return
  typed dataclasses; see the [API reference](api.md).

Head to [Getting Started](getting-started.md) for a tour, or try the
[quickstart notebook on Colab](https://colab.research.google.com/github/obichan117/yfcomment/blob/main/examples/quickstart.ipynb).
