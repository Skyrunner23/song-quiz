from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Union
from model.puzzle import *
import db.csv_repository

# Things we'll need:
# -- Get today's clue
#    == internal to function will need to look at date
#    == can cache Puzzle() in memory; if not in memory, then call DB reader
#    == what if Puzzle() isn't found?
# -- Get yesterday's answer


class Services:
    LOCALTZ = ZoneInfo("America/Phoenix")

    def __init__(self):
        self.repo = db.csv_repository.MyCSVRepository()

    def get_today(self, justclue=True) -> Union[Clue, Puzzle, None]:
        """return the clue for today's puzzle"""
        todaysdate = datetime.now(tz=self.LOCALTZ).strftime(self.repo.DATEFORMAT)
        todayspuzzle = self.repo.get_puzzle_by_date(todaysdate)
        if todayspuzzle and justclue:
            return todayspuzzle.clue
        elif todayspuzzle:
            return todayspuzzle
        else:
            return None

    def get_yesterday(self) -> Puzzle:
        """
        return information for yesterday's puzzle, or if there is no puzzle
          for yesterday, then return the most recent puzzle before today
        """
        range_to_consider = 15  # only check for the most recent 15 days
        for delta in range(0, range_to_consider):
            yesterday = datetime.now(tz=self.LOCALTZ) - timedelta(days=(1+delta))
            yesterdaysdate = yesterday.strftime(self.repo.DATEFORMAT)
            yesterdayspuzzle = self.repo.get_puzzle_by_date(yesterdaysdate)
            if yesterdayspuzzle:
                return yesterdayspuzzle
        return self.repo.DEFAULT

    def get_demo(self, justclue=True) -> Union[Clue, Puzzle, None]:
        """return the clue for a demo puzzle"""
        puzzledate = "2000/01/01"
        demopuzzle = self.repo.get_puzzle_by_date(puzzledate)
        if demopuzzle and justclue:
            return demopuzzle.clue
        elif demopuzzle:
            return demopuzzle
        else:
            return None

    def record_submission(self, user_sub: Submission) -> bool:
        """
        take in a user's submission for a puzzle and store it for grading

        :param user_sub: A Submission object with date, name, title, artist
        :return: True if successfully stored, else False
        """
        if not isinstance(user_sub, Submission):
            raise TypeError(f'[Services] record_submission received invalid type: '
                            f'{user_sub} should be Submission, is {type(user_sub)}')

        result = self.repo.record_submission(user_sub)
        return result


'''
From original code in Puzzle
  -- Move to HTML?

def get_answer(self, lyric_guess, artist_guess):
    """I'd like to move this code (eventually) to the business logic, not the class"""
    self.lyric_guess = lyric_guess
    self.artist_guess = artist_guess
    return (
        f"You guessed {lyric_guess} by {artist_guess}. The answer is {self.answer.title} by {self.answer.artist}.")
'''