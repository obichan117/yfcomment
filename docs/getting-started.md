# Getting Started

## Install

```bash
uv tool install yfcomment   # or: pip install yfcomment
```

Python 3.11+ required. This puts the `yfc` command on your PATH.

## Reading a stock's forum

Pass a stock code — the `.T` (Tokyo) market suffix is appended automatically:

```bash
yfc 285A          # Kioxia — latest 20 comments
yfc 7203          # Toyota
yfc 285A -n 100   # more comments (pagination is automatic)
```

The dim line above the table is the thread's sentiment poll (みんなの評価).

### Trimming the view

```bash
yfc 285A --no-user     # hide usernames
yfc 285A --no-votes    # hide 参考になりましたか はい/いいえ counts
yfc 285A --no-poll     # hide the sentiment poll header
yfc 285A --full        # full comment text, word-wrapped instead of truncated
```

## The comment ranking

Which stocks is everyone talking about?

```bash
yfc rank           # top 20, daily
yfc rank -w        # weekly
yfc rank -m        # monthly
yfc rank -n 60     # top 60 (fetches multiple pages)
```

!!! note
    The site exposes rank order, price, and last-post time — but not the
    actual post counts.

## JSON output

Every command takes `--json` for scripting:

```bash
yfc 285A --json -n 50 | jq '.comments[].text'
yfc rank -w --json | jq '.entries[] | {rank, code, name}'
```

Shapes: `{"code", "poll", "comments"}` for comments, `{"term", "entries"}` for
the ranking.

## Using it from Python

```python
from yfcomment import get_forum, get_ranking

forum = get_forum("285A", limit=50)
print(forum.poll)                      # {"強く買いたい": 26.83, ...} or None
for c in forum.comments:
    print(c.posted_at, c.helpful_yes, c.text)

for e in get_ranking("weekly", limit=10):
    print(e.rank, e.code, e.name)
```

See the [Python API reference](api.md) for all fields, or run the
[quickstart notebook on Colab](https://colab.research.google.com/github/obichan117/yfcomment/blob/main/examples/quickstart.ipynb).
