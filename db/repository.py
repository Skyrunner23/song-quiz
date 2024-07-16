import abc
from model.puzzle import *


class PuzzleRepository(metaclass=abc.ABCMeta):
    """Abstract repository: these are the methods we MUST implement"""

    @abc.abstractmethod
    def get_puzzle_by_date(self, desired_date: str) -> Puzzle:
        raise NotImplementedError

    @abc.abstractmethod
    def record_submission(self, user_sub: Submission) -> bool:
        raise NotImplementedError
