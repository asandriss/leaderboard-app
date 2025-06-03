import pytest
from datetime import datetime
from backend.models.submission import Submission


def test_valid_submission_parsing_without_title():
    data = {"user": "alice", "score": 87, "date": "01/01/2024"}
    s = Submission.from_dict(data)
    assert s.user == "alice"
    assert s.score == 87
    assert s.title == ""
    assert s.date == datetime(2024, 1, 1)

def test_valid_submission_parsing_with_full_information():
    data = {"user": "alice", "score": 87, "title": "this is the submission title", "date": "01/01/2024"}
    s = Submission.from_dict(data)
    assert s.user == "alice"
    assert s.score == 87
    assert s.title == "this is the submission title"
    assert s.date == datetime(2024, 1, 1)

def test_invalid_missing_fields():
    with pytest.raises(ValueError):
        Submission.from_dict({"score": 100, "date": "01/01/2024"})


def test_invalid_score_range():
    with pytest.raises(ValueError):
        Submission.from_dict({"user": "bob", "score": 2000, "date": "01/01/2024"})


def test_invalid_date_format():
    with pytest.raises(ValueError):
        Submission.from_dict({"user": "bob", "score": 80, "date": "2024-01-01"})
