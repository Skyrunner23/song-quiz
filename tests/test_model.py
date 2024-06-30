import unittest
from model.puzzle import *


def test_clue():
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1987
    clue_out = "We've known each other for so long, Pop, 1980s"
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

def test_answer():
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"
    answer_out = 'Never Gonna Give You Up, Rick Astley'

    test_answer = Answer(test_title, test_artist)
    assert answer_out == str(test_answer)


def test_puzzle():
    test_date = "2024/01/01"
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1980
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    answer_out = 'Never Gonna Give You Up, Rick Astley'
    clue_out = "We've known each other for so long, Pop, 1980s"
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


if __name__ == '__main__':
    unittest.main()
