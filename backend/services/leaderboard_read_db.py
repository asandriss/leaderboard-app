import logging
from typing import List

from backend.services.leaderboard_service import LeaderboardEntry

logger = logging.getLogger(__name__)


class LeaderboardReadDB:
    """
    Temporary in-memory store for the current leaderboard.

    Acts as a read-model in a pseudo-CQRS setup. In production, this would be
    replaced with a durable cache or fast-access database (e.g. Redis, DynamoDB).
    """

    def __init__(self):
        self._cached: List[LeaderboardEntry] = []
        logger.info("LeaderboardReadDB initialized")

    def set(self, entries: List[LeaderboardEntry]) -> None:
        """
        Stores the latest leaderboard entries.

        Args:
            entries (List[LeaderboardEntry]): Computed leaderboard entries to cache.
        """
        self._cached = entries
        logger.info("Leaderboard updated with %d entries", len(entries))

    def get(self) -> List[LeaderboardEntry]:
        """
        Retrieves the current cached leaderboard.

        Returns:
            List[LeaderboardEntry]: Leaderboard entries.
        """
        logger.debug("Returning leaderboard with %d entries", len(self._cached))
        return self._cached

    def clear(self) -> None:
        """
        Clears the cached leaderboard entries.
        """
        logger.info("Clearing leaderboard cache")
        self._cached = []
