from datetime import datetime

from backend.models.submission import Submission
from backend.services.leaderboard_service import (LeaderboardEntry,
                                                  compute_leaderboard)
from backend.services.submission_repository import SubmissionRepository


def make_submission(user: str, score: int, date="2024-01-01") -> Submission:
    return Submission(
        user=user,
        score=score,
        title=f"Title {score}",
        date=datetime.strptime(date, "%Y-%m-%d"),
    )


def test_leaderboard_filters_users_with_less_than_3_submissions():
    repo = SubmissionRepository()
    repo.add(make_submission("alice", 100))
    repo.add(make_submission("alice", 95))

    leaderboard = compute_leaderboard(repo)
    assert leaderboard == []


def test_leaderboard_sums_top_24_scores_only():
    repo = SubmissionRepository()

    # Add 30 submissions: 0-29
    for i in range(30):
        repo.add(make_submission("bob", i))

    leaderboard = compute_leaderboard(repo)
    assert len(leaderboard) == 1

    entry = leaderboard[0]
    assert entry.user == "bob"
    assert len(entry.top_scores) == 24
    assert entry.total_score == sum(range(6, 30))  # top 24 scores (ignore frist 6)


def test_leaderboard_ranking_is_correct():
    repo = SubmissionRepository()

    for score in [90, 80, 70]:
        repo.add(make_submission("alice", score))
    for score in [60, 50, 40]:
        repo.add(make_submission("bob", score))
    for score in [99, 98, 97]:
        repo.add(make_submission("carol", score))

    leaderboard = compute_leaderboard(repo)

    assert [e.user for e in leaderboard] == ["carol", "alice", "bob"]


def test_leaderboard_limit_parameter():
    repo = SubmissionRepository()

    for i in range(5):
        for score in [100, 99, 98]:
            repo.add(make_submission(f"user{i}", score))

    leaderboard = compute_leaderboard(repo, limit=3)
    assert len(leaderboard) == 3
