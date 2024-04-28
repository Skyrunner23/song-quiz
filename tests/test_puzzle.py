import unittest
from datetime import date
from app.puzzle import Puzzle

today = date.today()


def test_clue():
    testdate = "1/1/2024"
    testlyric = "We've known each other for so long"
    testgenre = "Pop"
    testyear = 1980
    testartist = "Rick Astley"
    testtitle = "Never Gonna Give You Up"

    clueout = "We've known each other for so long, Pop, 1980s"

    test_puzzle = Puzzle(testdate, testlyric, testgenre, testyear, testartist,testtitle)
    assert str(test_puzzle) == clueout
    assert str(test_puzzle.clue) == clueout


def test_answer():
    testdate = "1/1/2024"
    testlyric = "We've known each other for so long"
    testgenre = "Pop"
    testyear = 1980
    testartist = "Rick Astley"
    testtitle = "Never Gonna Give You Up"

    answerout = 'Never Gonna Give You Up, Rick Astley'

    test_puzzle = Puzzle(testdate, testlyric, testgenre, testyear, testartist,testtitle)
    assert str(test_puzzle.answer) == answerout
#    assert test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You Up "
#                                                                                "by Rick Astley. The answer is Never "
#                                                                                "Gonna Give You Up by Rick Astley.")


if __name__ == '__main__':
    unittest.main()
