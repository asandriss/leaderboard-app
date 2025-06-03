from typing import List, Dict, Set, Tuple
from backend.models.submission import Submission

class SubmissionRepository:
    def __init__(self):
        self._submissions_by_user: Dict[str, List[Submission]] = {}
        self._seen: Set[Tuple[str, int, str]] = set()
    
    def add(self, submission: Submission) -> bool:
        # use user, submission title and date as a unique identifier of a score
        key = (submission.user, submission.title, submission.date.isoformat())

        if key in self._seen:
            return False # duplicate submission
        
        self._seen.add(key)
        self._submissions_by_user.setdefault(submission.user, []).append(submission)
        return True
    
    def get_user_submissions(self, user:str) -> List[Submission]:
        return self._submissions_by_user.get(user, [])
    
    def get_all_submissions(self) -> List[Submission]:
        all_subs = []

        for subs in self._submissions_by_user.values():
            all_subs.extend(subs)
        return all_subs
    
    def clear(self):
        self._submissions_by_user.clear()
        self._seen.clear()