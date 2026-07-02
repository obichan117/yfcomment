"""Typer CLI. Entry point: ``yfc`` (see pyproject.toml).

    yfc 285A                 # latest 20 comments, compact table
    yfc 285A -n 50           # comment count
    yfc 285A --no-user       # hide usernames
    yfc 285A --no-votes      # hide はい/いいえ counts
    yfc 285A --full          # untruncated comment text
    yfc 285A --json          # JSON to stdout (pipe-friendly)
"""

import typer

app = typer.Typer(add_completion=False)


@app.command()
def main(
    code: str = typer.Argument(..., help='Stock code, e.g. "285A" or "7203" (".T" appended automatically)'),
    limit: int = typer.Option(20, "--limit", "-n", help="Number of comments to show"),
    no_user: bool = typer.Option(False, "--no-user", help="Hide usernames"),
    no_votes: bool = typer.Option(False, "--no-votes", help="Hide helpful-vote counts"),
    full: bool = typer.Option(False, "--full", help="Show full comment text without truncation"),
    as_json: bool = typer.Option(False, "--json", help="Output JSON instead of a table"),
) -> None:
    """Show the latest comments from the stock's Yahoo Finance Japan forum."""
    raise NotImplementedError("implemented in task: cli/render")


if __name__ == "__main__":
    app()
