"""Terminal rendering: list[Comment] -> Rich table. No fetching or parsing here."""

from rich import box
from rich.table import Table
from rich.text import Text

from yfcomment.models import Comment, RankEntry


def _votes_cell(comment: Comment) -> Text:
    cell = Text()
    cell.append(f"\U0001f44d{comment.helpful_yes}", style="green")
    cell.append(" ")
    cell.append(f"\U0001f44e{comment.helpful_no}", style="red")
    return cell


def build_table(
    comments: list[Comment],
    *,
    show_user: bool = True,
    show_votes: bool = True,
    full_text: bool = False,
) -> Table:
    """Build the comments table.

    Columns: time, votes (optional), text, user (optional).
    Text is truncated to terminal width unless ``full_text``.
    """
    table = Table(box=box.SIMPLE, expand=True)

    table.add_column("Time", no_wrap=True)
    if show_votes:
        table.add_column("Votes", justify="right", no_wrap=True)
    table.add_column(
        "Comment",
        overflow="fold" if full_text else "ellipsis",
        no_wrap=not full_text,
        ratio=1,
    )
    if show_user:
        table.add_column("User", style="dim", no_wrap=True)

    for comment in comments:
        row = [comment.posted_at.strftime("%m/%d %H:%M")]
        if show_votes:
            row.append(_votes_cell(comment))
        row.append(comment.text)
        if show_user:
            row.append(comment.username)
        table.add_row(*row)

    return table


def build_rank_table(entries: list[RankEntry]) -> Table:
    """Build the BBS ranking table.

    Columns: rank, code, name (truncated to fit), market, price, last post time.
    """
    table = Table(box=box.SIMPLE, expand=True)

    table.add_column("#", justify="right", no_wrap=True)
    table.add_column("Code", no_wrap=True)
    table.add_column("Name", overflow="ellipsis", no_wrap=True, ratio=1)
    table.add_column("Market", style="dim", no_wrap=True)
    table.add_column("Price", justify="right", no_wrap=True)
    table.add_column("Last post", style="dim", no_wrap=True)

    for entry in entries:
        table.add_row(
            str(entry.rank),
            entry.code,
            entry.name,
            entry.market,
            entry.price or "",
            entry.updated_at or "",
        )

    return table
