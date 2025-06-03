import pytest
from backend.services.upload_service import process_uploaded_json
from backend.services.submission_repository import SubmissionRepository


def test_process_valid_json_input():
    repo = SubmissionRepository()
    json_data = '''
    [
        {
            "name": "Alice",
            "submissions": [
                { "score": 100, "title": "Maths", "date": "01/01/2024" },
                { "score": 90, "title": "Physics", "date": "02/01/2024" }
            ]
        }
    ]
    '''
    added = process_uploaded_json(json_data, repo)
    assert len(added) == 2
    assert repo.get_user_submissions("Alice") == added


def test_process_skips_invalid_submissions():
    repo = SubmissionRepository()
    json_data = '''
    [
        {
            "name": "Bob",
            "submissions": [
                { "score": "bad", "title": "Oops", "date": "16/07/2024" },
                { "score": 88, "title": "Good", "date": "16/07/2024" }
            ]
        }
    ]
    '''
    added = process_uploaded_json(json_data, repo)
    assert len(added) == 1
    assert added[0].score == 88


def test_invalid_json_raises_error():
    with pytest.raises(ValueError):
        process_uploaded_json("not a json", SubmissionRepository())
