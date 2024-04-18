import unittest
from datetime import date
from app.puzzle import PuzzleInstance

today = date.today()


def test_hint():
    test_puzzle = PuzzleInstance(today, "We've known each other for so long", "Pop", 1980, "Rick Astley",
                                 "Never Gonna "
                                 "Give You Up")
    assert test_puzzle.get_hint() == "We've known each other for so long, Pop, 1980s"


def test_answer():
    test_puzzle = PuzzleInstance("1/1/2024", "We've known each other for so long", "Pop", 1980, "Rick Astley",
                                 "Never Gonna Give You Up")
    assert test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You Up "
                                                                                "by Rick Astley. The answer is Never "
                                                                                "Gonna Give You Up by Rick Astley.")


if __name__ == '__main__':
    unittest.main()
