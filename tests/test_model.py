import unittest
import pytest
from model.puzzle import *

sample_date = "2024/01/01"
sample_lyric = "We've known each other for so long"
sample_genre = "Pop"
sample_year = 1987
sample_clue_pairs = [('lyric', sample_lyric), ('genre', sample_genre), ('year', sample_year)]
sample_clue_out = "We've known each other for so long, Pop, 1987"
sample_artist = "Rick Astley"
sample_artistmatch = r"ric?k astley"
sample_title = "Never Gonna Give You Up"
sample_titlematch = r"never (gonna|going to) give you up"
sample_answer_out = 'Never Gonna Give You Up, Rick Astley'
sample_name = "Wilbur Wildcat"
sample_baddate = "Sasquatch"
sample_submission_pairs = [('name', sample_name), ('date', sample_date),
                           ('title', sample_title), ('artist', sample_artist)]


def test_clue_obj():
    sample_clue = Clue(sample_lyric, sample_genre, sample_year)
    assert sample_clue_out == str(sample_clue)


def test_clue_serialize():
    sample_clue = Clue(sample_lyric, sample_genre, sample_year)
    serialized = sample_clue.serialize()
    assert isinstance(serialized, dict)
    for attribute_label, attribute_value in sample_clue_pairs:
        assert serialized[attribute_label] == attribute_value


def test_answer_obj():
    sample_answer = Answer(sample_title, sample_titlematch, sample_artist, sample_artistmatch)
    assert sample_answer_out == str(sample_answer)


def test_puzzle_obj():
    sample_puzzle = Puzzle(sample_date, sample_lyric, sample_genre,
                           sample_year, sample_title, sample_titlematch,
                           sample_artist, sample_artistmatch)
    assert str(sample_puzzle.clue) == sample_clue_out
    assert str(sample_puzzle.answer) == sample_answer_out
    assert str(sample_puzzle.date) == sample_date

    """old version of the same code"""
    # assert sample_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You
    # Up " "by Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.") sample_puzzle = Puzzle(
    # "1/1/2024", "We've known each other for so long", "Pop", 1980, "Rick Astley", "Never Gonna Give You Up") assert
    # sample_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You Up " "by
    # Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.")


def test_submission():
    sample_sub1 = Submission(sample_name, sample_date, sample_title, sample_artist)
    assert sample_sub1.name == sample_name
    assert sample_sub1.date == sample_date
    assert sample_sub1.title == sample_title
    assert sample_sub1.artist == sample_artist
    sample_sub3 = Submission(sample_name, sample_date)
    assert sample_sub3 is not None
    with pytest.raises(ValueError):
        sample_sub2 = Submission(sample_name, sample_baddate)
    with pytest.raises(ValueError):
        sample_sub2 = Submission("", sample_date)
    with pytest.raises(TypeError):
        sample_sub2 = Submission(1, sample_date)
    with pytest.raises(TypeError):
        sample_sub2 = Submission(sample_name, 1987, sample_title, sample_artist)
    with pytest.raises(TypeError):
        sample_sub2 = Submission(sample_name, sample_date, 1987, sample_artist)
    with pytest.raises(TypeError):
        sample_sub2 = Submission(sample_name, sample_date, sample_title, 1987)


def test_grade_submission():
    sample_sub1 = Submission(sample_name, sample_date, sample_title, sample_artist)
    sample_key1 = {'title': True, 'artist': True}
    sample_sub2 = Submission(sample_name, sample_date,
                             "Never gOiNg TO give you up", sample_artist)
    sample_sub3 = Submission(sample_name, sample_date,
                             sample_title, "rIk astley")
    sample_sub4 = Submission(sample_name, sample_date,
                             "Never", sample_artist)
    sample_key4 = {'title': False, 'artist': True}
    sample_sub5 = Submission(sample_name, sample_date,
                             sample_title, "astley")
    sample_key5 = {'title': True, 'artist': False}
    sample_puzzle = Puzzle(sample_date, sample_lyric, sample_genre,
                           sample_year, sample_title, sample_titlematch,
                           sample_artist, sample_artistmatch)
    assert sample_puzzle.answer.grade(sample_sub1) == sample_key1
    assert sample_puzzle.answer.grade(sample_sub2) == sample_key1
    assert sample_puzzle.answer.grade(sample_sub3) == sample_key1
    assert sample_puzzle.answer.grade(sample_sub4) == sample_key4
    assert sample_puzzle.answer.grade(sample_sub5) == sample_key5


if __name__ == '__main__':
    unittest.main()
