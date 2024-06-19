import unittest
from db.reader import *

"""Import a row from the csv with a specific date and use it as the puzzle data"""


def test_reader_positive():
    """make sure output is okay when puzzle is found"""

    test_date = "2024/01/01"
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1980
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    test_puzzle = Puzzle(test_date, test_lyric, test_genre, test_year, test_title, test_artist)
    test_repo = MyCSVRepository()

    check_puzzle = test_repo.get_puzzle_by_date(test_date)

    assert test_puzzle == check_puzzle


def test_reader_negative():
    """make sure output is okay when puzzle isn't found"""

    test_date = "1969/12/31"
    test_repo = MyCSVRepository()

    check_puzzle = test_repo.get_puzzle_by_date(test_date)
    assert check_puzzle is None


if __name__ == '__main__':
    unittest.main()
