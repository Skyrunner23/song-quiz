import unittest
from db.reader import *

"""Import a row from the csv with a specific date and use it as the puzzle data"""
def test_reader():
    test_date = "1/1/2024"
    test_lyric = "We've known each other for so long"
    test_genre = "Pop"
    test_year = 1980
    test_artist = "Rick Astley"
    test_title = "Never Gonna Give You Up"

    answer_out = 'Never Gonna Give You Up, Rick Astley'

    test_puzzle = Puzzle(test_date, test_lyric, test_genre, test_year, test_title, test_artist)

    check_puzzle = reader(test_date)

    assert test_puzzle == check_puzzle

def test_clue():
    desired_date = "1/1/2024"
    filepath = "../db/song_list.csv"
    test_puzzle = None
    clue_out = None

    """this is the same code that the puzzle.py file uses to fetch a song, we're just fetching it ourselves here to 
    make sure the fetcher in the other file is working"""
    with open("../db/song_list.csv") as songs:
        csv_reader = csv.reader(songs, delimiter="|")
        for row in csv_reader:
            if row[0] == desired_date:
                test_puzzle = Puzzle(row[0], row[1], row[2], int(row[3]), row[4], row[5])
                clue_out = "%s, %s, %ss" % (row[1], row[2], row[3])
                break

    fetched_puzzle = get_song_from_file(desired_date, "../db/song_list.csv")
    fetched_clue = str(fetched_puzzle)

    assert fetched_clue == clue_out


"""This test is still using arbitrary values"""


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
