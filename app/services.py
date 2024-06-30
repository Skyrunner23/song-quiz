from datetime import datetime, timedelta
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

    def __init__(self):
        self.repo = db.csv_repository.MyCSVRepository()

    def get_today(self, justclue=True) -> Union[Clue, Puzzle]:
        """return the clue for today's puzzle"""
        todaysdate = datetime.now().strftime(self.repo.DATEFORMAT)
        todayspuzzle = self.repo.get_puzzle_by_date(todaysdate)
        if todayspuzzle and justclue:
            return todayspuzzle.clue
        elif todayspuzzle:
            return todayspuzzle
        else:
            return None


    def get_yesterday(self) -> Puzzle:
        """return information for yesterday's puzzle"""
        yesterday = datetime.now() - timedelta(days=1)
        yesterdaysdate = yesterday.strftime(self.repo.DATEFORMAT)
        yesterdayspuzzle = self.repo.get_puzzle_by_date(yesterdaysdate)
        if yesterdayspuzzle:
            return yesterdayspuzzle
        else:
            return None


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