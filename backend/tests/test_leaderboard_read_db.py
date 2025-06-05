from backend.services.leaderboard_read_db import LeaderboardReadDB
from backend.services.leaderboard_service import LeaderboardEntry


def test_set_and_get_leaderboard_entries():
    db = LeaderboardReadDB()
    sample = [
        LeaderboardEntry(user="alice", total_score=123, top_scores=[60, 63]),
        LeaderboardEntry(user="bob", total_score=456, top_scores=[150, 150, 156]),
    ]
    db.set(sample)
    result = db.get()
    assert result == sample


def test_clear_leaderboard_entries():
    db = LeaderboardReadDB()
    db.set([LeaderboardEntry(user="alice", total_score=123, top_scores=[60, 63])])
    db.clear()
    assert db.get() == []


def test_get_returns_reference():
    db = LeaderboardReadDB()
    entry = LeaderboardEntry(user="alice", total_score=123, top_scores=[123])
    db.set([entry])
    result = db.get()
    result.append(LeaderboardEntry(user="evil", total_score=999, top_scores=[999]))
    assert len(db.get()) == 2  # Reminder: this will pass unless get() returns a copy
