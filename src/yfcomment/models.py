"""Public data model for forum comments."""

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class Comment:
    """One comment on a Yahoo Finance Japan stock forum thread."""

    number: int  # site-wide comment number ("No.1272773")
    posted_at: datetime
    username: str  # partially masked by the site (e.g. "abc***")
    text: str
    sentiment: str | None = None  # 買いたい / 強く買いたい / 売りたい / ...
    helpful_yes: int = 0  # 「参考になりましたか？」 はい
    helpful_no: int = 0  # 「参考になりましたか？」 いいえ
    url: str | None = None  # permalink to the comment, when available

    def to_dict(self) -> dict:
        d = asdict(self)
        d["posted_at"] = self.posted_at.isoformat()
        return d
