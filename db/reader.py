import csv
from model.puzzle import Puzzle

FILEPATH = "db/song_list.csv"


def get_song_by_date(desired_date):
    puzzle = None

    with open(FILEPATH) as songs:
        csv_reader = csv.reader(songs, delimiter="|")
        for date,lyric,genre,decade,title,artist in csv_reader:
            if date == desired_date:
                puzzle = Puzzle(date,lyric,genre,int(decade),title,artist)
                #clue_out = "%s, %s, %ss" % (row[1], row[2], row[3])
                break

    return puzzle
