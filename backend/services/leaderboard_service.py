from dataclasses import dataclass
from typing import List
from backend.models.submission import Submission
from backend.services.submission_repository import SubmissionRepository

@dataclass(frozen=True)
class LeaderboardEntry:
    user: str
    total_score: int
    top_scores: List[int]

def compute_leaderboard(repo: SubmissionRepository, limit: int = 25) -> List[LeaderboardEntry]:
    entries: List[LeaderboardEntry] = []

    for user, submissions in repo._submissions_by_user.items():
        if len(submissions) < 3:
            continue

        top_scores = sorted((s.score for s in submissions), reverse=True)[:24]
        total = sum(top_scores)
        entries.append(LeaderboardEntry(user=user, total_score=total, top_scores=top_scores))

    return sorted(entries, key=lambda e: e.total_score, reverse=True)[:limit]
