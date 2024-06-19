import csv
import os
from model.puzzle import *

FILEPATH = "../data/song_list.csv"


def get_puzzle_by_date(desired_date):
    """
    search the CSV file for a puzzle, based on the date

    If a matching date is found, return a Puzzle object containing that puzzle data
    If no matching puzzle is found, return None
    """
    puzzle = None

    with open(os.path.join(os.path.dirname(__file__), FILEPATH), 'r') as puzzles:
        csv_reader = csv.reader(puzzles, delimiter="|")
        for date,lyric,genre,decade,title,artist in csv_reader:
            if date == desired_date:
                puzzle = Puzzle(date,lyric,genre,int(decade),title,artist)
                break

    return puzzle
