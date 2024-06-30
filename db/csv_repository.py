import csv
import os
import re
from model.puzzle import *
from db.repository import PuzzleRepository
from functools import lru_cache


class MyCSVRepository(PuzzleRepository):
    PUZZLES = "../data/song_list.csv"
    ARTISTS = "../data/artist_list.csv"
    DELIMITER = "%"
    DATEFORMAT = "%Y/%m/%d"
    DATEMATCH = r'\d{4}/\d{2}/\d{2}'
    DEFAULT = Puzzle("1970/01/01",
                  "We've known each other for so long",
                  "Rock",
                  1987,
                  "Never Gonna Give You Up",
                  "Rick Astley")
    DEFAULT = None

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

        with open(os.path.join(os.path.dirname(__file__), self.PUZZLES), 'r') as puzzles:
            csv_reader = csv.reader(puzzles, delimiter=self.DELIMITER)
            next(csv_reader)
            for date, lyric, genre, decade, title, artist in csv_reader:
                # Validation:
                #   artist: in self.get_artist() method, called below
                #   genre: in Genre() object
                #   date: lines below
                if not re.fullmatch(self.DATEMATCH, date):
                    raise ValueError(f'MyCSVRepository.get_puzzle_by_date(): malformed date in {self.PUZZLES}: {date}')
                if date == desired_date:
                    normalized = str(self.get_artist(artist))
                    if normalized is not None and artist != normalized:
                        artist = normalized
                    puzzle = Puzzle(date, lyric, genre, int(decade), title, artist)
                    break

        return puzzle

    def get_artist(self, desired_artist):
        """
        search the artist table in order to instantiate an Artist object

        :param desired_artist:str
        :return: Artist() object that matches this string, or None
        """
        #artist = self.DEFAULT.answer.artist
        artist = None

        with open(os.path.join(os.path.dirname(__file__), self.ARTISTS), 'r') as artists:
            csv_reader = csv.reader(artists, delimiter=self.DELIMITER)
            for id, artistname, pattern in csv_reader:
                if re.fullmatch(pattern, desired_artist.lower(), re.IGNORECASE):
                    artist = Artist(artistname)
                    break

        return artist
