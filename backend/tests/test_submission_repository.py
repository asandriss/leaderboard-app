import pytest
from datetime import datetime
from backend.models.submission import Submission
from backend.services.submission_repository import SubmissionRepository


def make_submission(user: str, title: str, date: str, score: int = 100) -> Submission:
    return Submission(user=user, title=title, score=score, date=datetime.strptime(date, "%Y-%m-%d"))


def test_add_and_retrieve_submission():
    repo = SubmissionRepository()
    s = make_submission("alice", "First try", "2024-01-01")
    assert repo.add(s) is True
    assert repo.get_user_submissions("alice") == [s]


def test_duplicate_submission_same_user_title_date():
    # Currently, we consider a post with same title and same date a duplicate. It will be ignored
    #  In a future implementation we may want to allow updates, in that case newer score will be used
    repo = SubmissionRepository()
    s1 = make_submission("alice", "Same title", "2024-01-01", 100)
    s2 = make_submission("alice", "Same title", "2024-01-01", 200)

    assert repo.add(s1) is True
    assert repo.add(s2) is False


def test_different_titles_on_same_day_are_allowed():
    repo = SubmissionRepository()
    s1 = make_submission("alice", "Morning run", "2024-01-01")
    s2 = make_submission("alice", "Evening session", "2024-01-01")

    assert repo.add(s1) is True
    assert repo.add(s2) is True

    results = repo.get_user_submissions("alice")
    assert len(results) == 2
    assert s1 in results and s2 in results


def test_different_users_same_title_and_date_are_allowed():
    repo = SubmissionRepository()
    s1 = make_submission("alice", "Daily challenge", "2024-01-01")
    s2 = make_submission("bob", "Daily challenge", "2024-01-01")

    assert repo.add(s1) is True
    assert repo.add(s2) is True

    assert repo.get_user_submissions("alice") == [s1]
    assert repo.get_user_submissions("bob") == [s2]


def test_get_all_submissions_aggregates_correctly():
    repo = SubmissionRepository()
    s1 = make_submission("alice", "A", "2024-01-01")
    s2 = make_submission("bob", "B", "2024-01-01")

    repo.add(s1)
    repo.add(s2)

    all_subs = repo.get_all_submissions()
    assert len(all_subs) == 2
    assert s1 in all_subs and s2 in all_subs


def test_clear_repository_empties_all_data():
    repo = SubmissionRepository()
    repo.add(make_submission("alice", "test", "2024-01-01"))
    repo.clear()

    assert repo.get_all_submissions() == []
    assert repo.get_user_submissions("alice") == []
