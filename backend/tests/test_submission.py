import pytest
from datetime import datetime
from backend.models.submission import Submission


def test_valid_submission_parsing():
    data = {"user": "alice", "score": 87, "date": "2024-01-01"}
    s = Submission.from_dict(data)
    assert s.user == "alice"
    assert s.score == 87
    assert s.date == datetime(2024, 1, 1)


def test_invalid_missing_fields():
    with pytest.raises(ValueError):
        Submission.from_dict({"score": 100, "date": "2024-01-01"})


def test_invalid_score_range():
    with pytest.raises(ValueError):
        Submission.from_dict({"user": "bob", "score": 2000, "date": "2024-01-01"})


def test_invalid_date_format():
    with pytest.raises(ValueError):
        Submission.from_dict({"user": "bob", "score": 80, "date": "01-01-2024"})
