import unittest
import pytest
from model.puzzle import *


def test_clue_obj():
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1987
    clue_out = "We've known each other for so long, Pop, 1987"
    test_clue = Clue(test_lyric, test_genre, test_year)

    assert clue_out == str(test_clue)


def test_clue_serialize():
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1987
    clue_out = "We've known each other for so long, Pop, 1980s"
    test_clue = Clue(test_lyric, test_genre, test_year)

    serialized = test_clue.serialize()
    assert isinstance(serialized, dict)
    assert serialized['lyric'] == test_lyric and serialized['genre'] == test_genre and serialized['year'] == test_year


def test_answer_onj():
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"
    answer_out = 'Never Gonna Give You Up, Rick Astley'

    test_answer = Answer(test_title, test_artist)
    assert answer_out == str(test_answer)


def test_puzzle_obj():
    test_date = "2024/01/01"
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1987
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    answer_out = 'Never Gonna Give You Up, Rick Astley'
    clue_out = "We've known each other for so long, Pop, 1987"
    date_out = "2024/01/01"

    test_puzzle = Puzzle(test_date, test_lyric, test_genre, test_year, test_title, test_artist)
    assert str(test_puzzle.clue) == clue_out
    assert str(test_puzzle.answer) == answer_out
    assert str(test_puzzle.date) == date_out

    """old version of the same code"""
    # assert test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You
    # Up " "by Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.") test_puzzle = Puzzle(
    # "1/1/2024", "We've known each other for so long", "Pop", 1980, "Rick Astley", "Never Gonna Give You Up") assert
    # test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You Up " "by
    # Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.")


def test_submission():
    test_name = "Wilbur Wildcat"
    test_date = "2024/01/01"
    test_baddate = "Sasquatch"
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"
    test_sub1 = Submission(test_name, test_date, test_title, test_artist)
    assert test_sub1.name == test_name
    assert test_sub1.date == test_date
    assert test_sub1.title == test_title
    assert test_sub1.artist == test_artist
    test_sub3 = Submission(test_name, test_date)
    assert test_sub3 is not None
    with pytest.raises(ValueError):
        test_sub2 = Submission(test_name, test_baddate)
    with pytest.raises(ValueError):
        test_sub2 = Submission("", test_date)
    with pytest.raises(TypeError):
        test_sub2 = Submission(1, test_date)
    with pytest.raises(TypeError):
        test_sub2 = Submission(test_name, 1987, test_title, test_artist)
    with pytest.raises(TypeError):
        test_sub2 = Submission(test_name, test_date, 1987, test_artist)
    with pytest.raises(TypeError):
        test_sub2 = Submission(test_name, test_date, test_title, 1987)


if __name__ == '__main__':
    unittest.main()
