import unittest
import csv
from app.puzzle import Puzzle

"""Import a row from the csv with a specific date and use it as the puzzle data"""


def test_clue():
    test_puzzle = ""
    with open("../app/song_list.csv") as songs:
        csv_reader = csv.reader(songs, delimiter="|")
        for row in csv_reader:
            if row[0] == "1/1/2024":
                test_puzzle = Puzzle(row[0], row[1], row[2], int(row[3]), row[4], row[5])
                break

    clue_out = "We've known each other for so long, Pop, 1980s"

    assert str(test_puzzle) == clue_out
    assert str(test_puzzle.clue) == clue_out


def test_answer():
    test_date = "1/1/2024"
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1980
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    answer_out = 'Never Gonna Give You Up, Rick Astley'

    test_puzzle = Puzzle(test_date, test_lyric, test_genre, test_year, test_title, test_artist)
    assert str(test_puzzle.answer) == answer_out

    """\/ old version of the same code \/"""
    # assert test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You
    # Up " "by Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.") test_puzzle = Puzzle(
    # "1/1/2024", "We've known each other for so long", "Pop", 1980, "Rick Astley", "Never Gonna Give You Up") assert
    # test_puzzle.get_answer("Never Gonna Give You Up", "Rick Astley") == ("You guessed Never Gonna Give You Up " "by
    # Rick Astley. The answer is Never " "Gonna Give You Up by Rick Astley.")


if __name__ == '__main__':
    unittest.main()
