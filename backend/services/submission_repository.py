import logging
from typing import Dict, List, Set, Tuple

from backend.models.submission import Submission

logger = logging.getLogger(__name__)


class SubmissionRepository:
    """
    In-memory repository for storing and retrieving user submissions.

    Tracks submissions keyed by user name, and prevents duplicates based on (user, title, date).
    Intended as a temporary or test-time storage layer.
    """

    def __init__(self):
        """
        Initializes an empty repository.
        """
        self._submissions_by_user: Dict[str, List[Submission]] = {}
        self._seen: Set[Tuple[str, str, str]] = set()
        logger.info("Initialized SubmissionRepository.")

    def add(self, submission: Submission) -> bool:
        """
        Add a submission if it is not a duplicate.

        Args:
            submission (Submission): The submission to add.

        Returns:
            bool: True if added successfully, False if it was a duplicate.
        """
        key = (submission.user, submission.title, submission.date.isoformat())

        if key in self._seen:
            logger.debug(
                "Duplicate submission ignored for user='%s', title='%s', date=%s",
                submission.user,
                submission.title,
                submission.date.strftime("%Y-%m-%d"),
            )
            return False

        self._seen.add(key)
        self._submissions_by_user.setdefault(submission.user, []).append(submission)
        logger.info(
            "Stored submission: user='%s', score=%d, title='%s', date=%s",
            submission.user,
            submission.score,
            submission.title,
            submission.date.strftime("%Y-%m-%d"),
        )
        return True

    def get_user_submissions(self, user: str) -> List[Submission]:
        """
        Retrieve all submissions for a given user.

        Args:
            user (str): Username.

        Returns:
            List[Submission]: List of that user’s submissions.
        """
        return self._submissions_by_user.get(user, [])

    def get_all_submissions(self) -> List[Submission]:
        """
        Retrieve all submissions across all users.

        Returns:
            List[Submission]: All submissions in the repository.
        """
        all_subs = []
        for subs in self._submissions_by_user.values():
            all_subs.extend(subs)
        return all_subs

    def clear(self):
        """
        Clears all stored submissions and duplicate tracking.
        """
        self._submissions_by_user.clear()
        self._seen.clear()
        logger.warning("Submission repository cleared.")
