"""Typer CLI. Entry point: ``yfc`` (see pyproject.toml).

    yfc 285A                 # latest 20 comments, compact table
    yfc 285A -n 50           # comment count
    yfc 285A --no-user       # hide usernames
    yfc 285A --no-votes      # hide はい/いいえ counts
    yfc 285A --full          # untruncated comment text
    yfc 285A --no-poll       # hide the sentiment poll header
    yfc 285A --json          # JSON to stdout (pipe-friendly)
"""

import json

import httpx
import typer
from rich.console import Console

from yfcomment import get_forum
from yfcomment._internal.render import build_table

app = typer.Typer(add_completion=False)


def _poll_line(poll: dict[str, float]) -> str:
    return " ・ ".join(f"{label} {round(percent)}%" for label, percent in poll.items())


@app.command()
def main(
    code: str = typer.Argument(..., help='Stock code, e.g. "285A" or "7203" (".T" appended automatically)'),
    limit: int = typer.Option(20, "--limit", "-n", help="Number of comments to show"),
    no_user: bool = typer.Option(False, "--no-user", help="Hide usernames"),
    no_votes: bool = typer.Option(False, "--no-votes", help="Hide helpful-vote counts"),
    full: bool = typer.Option(False, "--full", help="Show full comment text without truncation"),
    no_poll: bool = typer.Option(False, "--no-poll", help="Hide the sentiment poll header"),
    as_json: bool = typer.Option(False, "--json", help="Output JSON instead of a table"),
) -> None:
    """Show the latest comments from the stock's Yahoo Finance Japan forum."""
    normalized_code = code.upper()

    try:
        forum = get_forum(normalized_code, limit=limit)
    except (httpx.HTTPStatusError, httpx.HTTPError, ValueError) as exc:
        reason = str(exc).splitlines()[0]
        typer.echo(f"Error: could not fetch comments for {normalized_code}: {reason}", err=True)
        raise typer.Exit(1) from exc

    if not forum.comments:
        typer.echo(f"No comments found for {normalized_code}.", err=True)
        raise typer.Exit(1)

    if as_json:
        print(json.dumps(forum.to_dict(), ensure_ascii=False))
        return

    console = Console()
    if forum.poll and not no_poll:
        console.print(_poll_line(forum.poll), style="dim")

    table = build_table(forum.comments, show_user=not no_user, show_votes=not no_votes, full_text=full)
    table.title = f"{normalized_code} — {len(forum.comments)} comments"
    console.print(table)


if __name__ == "__main__":
    app()
