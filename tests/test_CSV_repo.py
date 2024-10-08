import unittest
import pytest
import os
import csv
from db.csv_repository import MyCSVRepository
from model.puzzle import *

"""Import a row from the csv with a specific date and use it as the puzzle data"""


def test_reader_positive():
    """make sure output is okay when puzzle is found"""

    test_date = "2000/01/01"
    test_lyric = "We've known each other for so long<br />You know the rules and so do I"
    test_genre = "Pop"
    test_year = 1987
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    test_puzzle = Puzzle(test_date, test_lyric, test_genre, test_year, test_title, test_title, test_artist, test_artist)
    test_repo = MyCSVRepository()

    check_puzzle = test_repo.get_puzzle_by_date(test_date)

    assert test_puzzle == check_puzzle


def test_reader_negative():
    """make sure output is okay when puzzle isn't found"""

    test_date = "1969/12/31"
    test_repo = MyCSVRepository()

    check_puzzle = test_repo.get_puzzle_by_date(test_date)
    assert check_puzzle is None


def test_submit():
    test_date = "2000/01/01"
    test_name = "Wilbur Wildcat"
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"
    test_repo = MyCSVRepository()

    with open(os.path.normpath(os.path.join(test_repo.ROOT, test_repo.SUBMISSIONS)), 'r') as sub:
        linecount_before = len(sub.readlines())

    # First test: full submission
    test1 = test_repo.record_submission(Submission(test_name,
                                                   test_date,
                                                   test_title,
                                                   test_artist))
    assert test1 is True

    # Second test: optional data omitted
    test2 = test_repo.record_submission(Submission(test_name,
                                                   test_date))
    assert test2 is True

    # Verify type checking
    with pytest.raises(TypeError):
        test3 = test_repo.record_submission((test_name, test_date))

    with open(os.path.normpath(os.path.join(test_repo.ROOT, test_repo.SUBMISSIONS)), 'r') as sub:
        linecount_after = len(sub.readlines())

    assert linecount_after == linecount_before + 2


def test_grades_in_data():
    test_repo = MyCSVRepository()
    with open(os.path.normpath(os.path.join(test_repo.ROOT, test_repo.PUZZLES)),
              'r', encoding='utf-8') as puzzles:
        csv_reader = csv.reader(puzzles, delimiter=test_repo.DELIMITER)
        next(csv_reader)
        matches = []
        for date, lyric, genre, year, title, titlematch, artist in csv_reader:
            datesartist = test_repo._get_artist(artist)
            datespuzzle = Puzzle(date, lyric, genre, int(year), title, titlematch,
                            datesartist.artist, datesartist.artistmatch)
            datesubmission = Submission('Wilbur', date, title, artist)
            thisgrade = (datespuzzle.answer.grade(datesubmission) == {'title': True, 'artist': True})
            matches.append(thisgrade)
            if not thisgrade:
                print(f'Date of puzzle with error: {date}\n')
        assert all(matches)


if __name__ == '__main__':
    unittest.main()
