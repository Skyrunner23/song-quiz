import csv
import os
from model.puzzle import *
from db.repository import PuzzleRepository
from functools import lru_cache


class MyCSVRepository(PuzzleRepository):
    FILEPATH = "../data/song_list.csv"
    DATEFORMAT = "%Y/%m/%d"
    DEFAULT = Puzzle("1970/01/01",
                  "We've known each other for so long",
                  "Rock",
                  1987,
                  "Never Gonna Give You Up",
                  "Rick Astley")

    def __init__(self):
        super().__init__()

    @lru_cache(maxsize=None)
    def get_puzzle_by_date(self, desired_date):
        """
        search the CSV file for a puzzle, based on the date

        If a matching date is found, return a Puzzle object containing that puzzle data
        If no matching puzzle is found, return None
        """
        puzzle = self.DEFAULT

        with open(os.path.join(os.path.dirname(__file__), self.FILEPATH), 'r') as puzzles:
            csv_reader = csv.reader(puzzles, delimiter="|")
            for date, lyric, genre, decade, title, artist in csv_reader:
                if date == desired_date:
                    # TODO: add check for valid date, genre, artist?
                    puzzle = Puzzle(date, lyric, genre, int(decade), title, artist)
                    break

        return puzzle
