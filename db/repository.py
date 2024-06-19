import abc
from model.puzzle import *

class PuzzleRepository(metaclass=abc.ABCMeta):
    """Abstract repository: these are the methods we MUST implement"""

    @abc.abstractmethod
    def get_puzzle_by_date(self, desired_date:str) -> Puzzle:
        raise NotImplementedError