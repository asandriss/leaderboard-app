from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Submission:
    user: str
    score: int
    date: datetime
    title: str = field(default="")

    @staticmethod
    def from_dict(data: dict) -> "Submission":
        try:
            user = data["user"]
            score = int(data["score"])
            title = data.get("title", "")
            date = datetime.strptime(data["date"], "%d/%m/%Y")
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid submission data: {data}") from e

        if not isinstance(user, str) or not user.strip():
            raise ValueError("User must be a non-empty string")

        if not (0 <= score <= 1000):  # arbitrary score range check
            raise ValueError("Score must be between 0 and 1000")

        return Submission(user=user.strip(), score=score, title=title.strip(), date=date)
