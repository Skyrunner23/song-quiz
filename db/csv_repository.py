import csv
import os
import logging
from model.puzzle import *
from db.repository import PuzzleRepository
from functools import lru_cache


class MyCSVRepository(PuzzleRepository):
    #ROOT = os.path.normpath("/opt/song-quiz/")
    ROOT = os.path.dirname(__file__)
    PUZZLES = "../data/song_list.csv"
    ARTISTS = "../data/artist_list.csv"
    SUBMISSIONS = "../data/submission_list.csv"
    DELIMITER = "%"
    DATEFORMAT = "%Y/%m/%d"
    DATEMATCH = r'\d{4}/\d{2}/\d{2}'
    DEFAULT = Puzzle("1970/01/01",
                     "We've known each other for so long",
                     "Rock",
                     1987,
                     "Never Gonna Give You Up",
                     "Never Gonna Give You Up",
                     "Rick Astley",
                     "Rick Astley")
    DEFAULT = None

    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()

    @lru_cache(maxsize=None)
    def get_puzzle_by_date(self, desired_date: str) -> Puzzle:
        """
        search the CSV file for a puzzle, based on the date

        If a matching date is found, return a Puzzle object containing that puzzle data
        If no matching puzzle is found, return None
        """
        puzzle = self.DEFAULT

        with open(os.path.normpath(os.path.join(self.ROOT, self.PUZZLES)),
                  'r', encoding='utf-8') as puzzles:
            csv_reader = csv.reader(puzzles, delimiter=self.DELIMITER)
            next(csv_reader)
            for date, lyric, genre, year, title, titlematch, artist in csv_reader:
                # Validation:
                #   artist: in self.get_artist() method, called below
                #   genre: in Genre() object
                #   date: lines below
                if not re.fullmatch(self.DATEMATCH, date):
                    raise ValueError(f'MyCSVRepository.get_puzzle_by_date(): malformed date in {self.PUZZLES}: {date}')
                if date == desired_date:
                    datesartist = self._get_artist(artist)
                    puzzle = Puzzle(date, lyric, genre, int(year), title, titlematch,
                                    datesartist.artist, datesartist.artistmatch)
                    break

        return puzzle

    def _get_artist(self, desired_artist: str) -> Artist:
        """
        search the artist table in order to instantiate an Artist object

        :param desired_artist:str
        :return: Artist() object that matches this string

        If a corresponding Artist() cannot be found, raise ValueError
        """
        # artist = self.DEFAULT.answer.artist
        artist = None

        with open(os.path.normpath(os.path.join(self.ROOT, self.ARTISTS)),
                  'r', encoding='utf-8') as artists:
            csv_reader = csv.reader(artists, delimiter=self.DELIMITER)
            for uid, artistname, pattern in csv_reader:
                if re.fullmatch(pattern, desired_artist, flags=re.IGNORECASE):
                    artist = Artist(artistname, pattern)
                    break

        if artist is None:
            raise ValueError(f'[MyCSVRepository._get_artist] : {artist} requested, not found')

        return artist

    def record_submission(self, user_sub: Submission) -> bool:
        """
        Store a puzzle submission from a user in the repository

        :param user_sub: A Submission object containing info for this user's submission
        :return: True if submission was correctly stored, else False
        """

        if not isinstance(user_sub, Submission):
            raise TypeError(f'[MyCSV_Repository] record_submission received invalid type: '
                            f'{user_sub} should be Submission, is {type(user_sub)}')

        with open(os.path.normpath(os.path.join(self.ROOT, self.SUBMISSIONS)),
                  'a', newline='', encoding='utf-8') as submissions:
            try:
                csv_writer = csv.writer(submissions, delimiter=self.DELIMITER)
                csv_writer.writerow([user_sub.name, user_sub.date, user_sub.title, user_sub.artist])
                return True
            except csv.Error as e:
                self.logger.error(f'[CSV_Repository] record submission failed: {e}')
                return False
