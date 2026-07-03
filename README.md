# yfcomment

[![PyPI version](https://img.shields.io/pypi/v/yfcomment.svg)](https://pypi.org/project/yfcomment/)
[![Python versions](https://img.shields.io/pypi/pyversions/yfcomment.svg)](https://pypi.org/project/yfcomment/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Yahoo Finance Japan stock forum comments (掲示板) and BBS rankings in your terminal —
no more scrolling a UI that shows 3 comments per screen.

```bash
yfc 285A                 # latest 20 comments, compact table
yfc 285A -n 50           # more comments
yfc 285A --no-user       # hide usernames
yfc 285A --no-votes      # hide はい/いいえ counts
yfc 285A --no-poll       # hide the thread sentiment poll header
yfc 285A --full          # untruncated comment text
yfc 285A --json          # JSON to stdout: {"code", "poll", "comments"}

yfc rank                 # 掲示板投稿数ランキング: top 20, daily
yfc rank -n 60 -w        # top 60 weekly (paginates automatically)
yfc rank -m --json       # monthly, JSON: {"term", "entries"}
```

## Install

```bash
uv tool install yfcomment   # or: pip install yfcomment
```

## Python API

```python
from yfcomment import get_forum, get_comments, get_ranking

forum = get_forum("285A", limit=20)
print(forum.poll)                # {"強く買いたい": 26.83, "買いたい": 2.44, ...} or None

for c in get_comments("285A", limit=20):
    print(c.posted_at, c.helpful_yes, c.helpful_no, c.text)

for e in get_ranking("weekly", limit=10):
    print(e.rank, e.code, e.name, e.price)
```
