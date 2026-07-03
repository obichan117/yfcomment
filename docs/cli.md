# CLI Reference

The `yfc` command has two subcommands. `comments` is the default: `yfc 285A`
is shorthand for `yfc comments 285A`.

## `yfc comments <code>` (default)

Show the latest comments from the stock's forum thread, newest first.

| Option | Default | Description |
|---|---|---|
| `CODE` (argument) | — | Stock code, e.g. `285A` or `7203`. `.T` appended automatically. |
| `-n`, `--limit` | `20` | Number of comments. Pagination is automatic. |
| `--no-user` | off | Hide usernames. |
| `--no-votes` | off | Hide 参考になりましたか はい/いいえ counts. |
| `--no-poll` | off | Hide the sentiment poll header line. |
| `--full` | off | Word-wrap full comment text instead of truncating to one line. |
| `--json` | off | Print `{"code", "poll", "comments"}` JSON instead of a table. |

Exit code `1` with a one-line message on stderr for network errors, unknown
codes, or empty threads.

### Comment JSON fields

`number` (site-wide comment No.), `posted_at` (ISO datetime), `username`,
`text`, `sentiment` (always `null` — not exposed by the comments API),
`helpful_yes`, `helpful_no`, `url` (always `null` — no per-comment permalink).

## `yfc rank`

Show the 掲示板投稿数ランキング — stocks ranked by forum activity.

| Option | Default | Description |
|---|---|---|
| `-n`, `--limit` | `20` | Number of entries (the site holds ~95; pages are fetched as needed). |
| `-w`, `--weekly` | off | Weekly ranking. |
| `-m`, `--monthly` | off | Monthly ranking. Mutually exclusive with `--weekly`. |
| `--json` | off | Print `{"term", "entries"}` JSON instead of a table. |

### Rank entry JSON fields

`rank`, `code`, `name`, `market` (e.g. `東証PRM`), `price` (display string,
e.g. `"83,300"`), `updated_at` (last forum activity), `forum_url`.
