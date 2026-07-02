"""Terminal rendering: list[Comment] -> Rich table. No fetching or parsing here."""

from rich.table import Table

from yfcomment.models import Comment


def build_table(
    comments: list[Comment],
    *,
    show_user: bool = True,
    show_votes: bool = True,
    full_text: bool = False,
) -> Table:
    """Build the comments table.

    Columns: time, sentiment, votes (optional), text, user (optional).
    Text is truncated to terminal width unless ``full_text``.
    """
    raise NotImplementedError("implemented in task: cli/render")
