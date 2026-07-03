# yfcomment

Yahoo Finance Japan stock forum comments (掲示板) in your terminal — no more scrolling
a UI that shows 3 comments per screen.

```bash
yfc 285A                 # latest 20 comments, compact table
yfc 285A -n 50           # more comments
yfc 285A --no-user       # hide usernames
yfc 285A --no-votes      # hide はい/いいえ counts
yfc 285A --no-poll       # hide the thread sentiment poll header
yfc 285A --full          # untruncated comment text
yfc 285A --json          # JSON to stdout: {"code", "poll", "comments"}
```

## Install (local)

```bash
uv tool install .
```

## Python API

```python
from yfcomment import get_forum, get_comments

forum = get_forum("285A", limit=20)
print(forum.poll)                # {"強く買いたい": 26.83, "買いたい": 2.44, ...} or None

for c in get_comments("285A", limit=20):
    print(c.posted_at, c.helpful_yes, c.helpful_no, c.text)
```
