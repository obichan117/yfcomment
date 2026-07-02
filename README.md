# yfcomment

Yahoo Finance Japan stock forum comments (掲示板) in your terminal — no more scrolling
a UI that shows 3 comments per screen.

```bash
yfc 285A                 # latest 20 comments, compact table
yfc 285A -n 50           # more comments
yfc 285A --no-user       # hide usernames
yfc 285A --no-votes      # hide はい/いいえ counts
yfc 285A --full          # untruncated comment text
yfc 285A --json          # JSON to stdout
```

## Install (local)

```bash
uv tool install .
```

## Python API

```python
from yfcomment import get_comments

for c in get_comments("285A", limit=20):
    print(c.posted_at, c.sentiment, c.text)
```
