import json
import logging
from typing import List

from backend.models.submission import Submission
from backend.services.submission_repository import SubmissionRepository

logger = logging.getLogger(__name__)


def process_uploaded_json(
    raw_data: str, repo: SubmissionRepository
) -> List[Submission]:
    try:
        users = json.loads(raw_data)
        assert isinstance(users, list)
    except (json.JSONDecodeError, AssertionError):
        raise ValueError("Invalid JSON format. Expected list of user objects.")

    print(f"[upload_service] Parsed {len(users)} users")
    added_submissions: List[Submission] = []

    for user_entry in users:
        user_name = user_entry.get("name")
        print(f"[upload_service] Processing user: {user_name}")
        if not isinstance(user_name, str):
            continue

        submissions = user_entry.get("submissions", [])
        if not isinstance(submissions, list):
            continue

        # falatten the list (combine and repeat user name with submission)
        for sub in submissions:
            print(f"[upload_service] Raw entry: {sub}")
            sub["user"] = user_name
            sub["title"] = sub.get("name", "")

            try:
                submission = Submission.from_dict(sub)
                if repo.add(submission):
                    added_submissions.append(submission)
            except ValueError:
                continue

    return added_submissions
