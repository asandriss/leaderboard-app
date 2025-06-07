import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Submission:
    """
    Represents a single submission by a user.

    Attributes:
        user (str): User name.
        score (int): Score for the submission.
        date (datetime): Date of submission.
        title (str): Optional submission title.
    """

    user: str
    score: int
    date: datetime
    title: str = field(default="")

    @staticmethod
    def from_dict(data: dict) -> "Submission":
        """
        Create a Submission instance from a dictionary.

        Args:
            data (dict): Dictionary with keys "user", "score", "date", and optionally "title".

        Returns:
            Submission: A validated Submission object.

        Raises:
            ValueError: If the input dictionary is missing required fields or contains invalid data.
        """
        logger.debug("Parsing submission from dict: %s", data)
        try:
            user = data["user"]
            score = int(data["score"])
            title = data.get("title", "")
            date = datetime.strptime(data["date"], "%d/%m/%Y")
        except (KeyError, ValueError, TypeError) as e:
            logger.warning("Failed to parse submission: %s", data, exc_info=True)
            raise ValueError(f"Invalid submission data: {data}") from e

        if not isinstance(user, str) or not user.strip():
            logger.warning("Invalid user field in submission: %s", data)
            raise ValueError("User must be a non-empty string")

        if not (0 <= score <= 1000):  # arbitrary score range check
            logger.warning("Score out of range in submission: %s", data)
            raise ValueError("Score must be between 0 and 1000")

        submission = Submission(
            user=user.strip(), score=score, title=title.strip(), date=date
        )
        logger.debug("Successfully created Submission: %s", submission)

        return submission
