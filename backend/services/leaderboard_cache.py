from typing import List

from backend.services.leaderboard_service import LeaderboardEntry


class LeaderboardReadDB:
    def __init__(self):
        self._cached: List[LeaderboardEntry] = []

    def set(self, entries: List[LeaderboardEntry]) -> None:
        self._cached = entries

    def get(self) -> List[LeaderboardEntry]:
        return self._cached

    def clear(self) -> None:
        self._cached = []
