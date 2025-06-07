import logging
from dataclasses import dataclass
from typing import List

from backend.services.submission_repository import SubmissionRepository

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LeaderboardEntry:
    """
    Represents a leaderboard entry for a user.

    Attributes:
        user (str): The user's name.
        total_score (int): The sum of the user's top scores.
        top_scores (List[int]): The top N scores included in the total.
    """

    user: str
    total_score: int
    top_scores: List[int]


def compute_leaderboard(
    repo: SubmissionRepository, limit: int = 25
) -> List[LeaderboardEntry]:
    """
    Computes the leaderboard from stored submissions.

    Users must have at least 3 submissions to qualify. The leaderboard is computed
    using the sum of each users top 24 scores, and is sorted descending by total.

    Args:
        repo (SubmissionRepository): Repository containing all submissions.
        limit (int): Maximum number of users to include in the leaderboard.

    Returns:
        List[LeaderboardEntry]: Ranked leaderboard entries.
    """
    logger.info("Computing leaderboard (limit=%d)...", limit)

    entries: List[LeaderboardEntry] = []
    for user, submissions in repo._submissions_by_user.items():
        if len(submissions) < 3:
            logger.debug(
                "Skipping user '%s' (only %d submissions)", user, len(submissions)
            )
            continue

        top_scores = sorted((s.score for s in submissions), reverse=True)[:24]
        total = sum(top_scores)
        entry = LeaderboardEntry(user=user, total_score=total, top_scores=top_scores)
        entries.append(entry)
        logger.debug("User '%s': total=%d, top_scores=%s", user, total, top_scores)

    sorted_entries = sorted(entries, key=lambda e: e.total_score, reverse=True)[:limit]
    logger.info("Leaderboard computed: %d entries", len(sorted_entries))
    return sorted_entries
