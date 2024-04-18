GENRE_SET = {"Rock", "Pop", "Metal", "Dance"}
ARTIST_SET = {"Rick Astley", "Taylor Swift", "Weird Al"}


class ClueBundle:
    def __init__(self, lyric, genre, year):
        self.lyric = lyric
        self.genre = Genre(genre)
        assert isinstance(year, int)

        # make sure the year ends with a zero
        round_to_decade = year / 10
        round_to_decade = int(round_to_decade)
        round_to_decade *= 10

        year = round_to_decade
        self.decade = year


class AnswerBundle:
    def __init__(self, title, artist):
        self.title = title
        self.artist = Artist(artist)


class PuzzleInstance(ClueBundle, AnswerBundle):
    def __init__(self, date, lyric, genre, decade, artist, title):
        self.date = date
        ClueBundle.__init__(self, lyric, genre, decade)
        AnswerBundle.__init__(self, title, artist)

        self.lyric_guess = ""
        self.artist_guess = ""

    def get_hint(self):
        hint_genre = Genre.get_genre(self.genre)
        hint_string = f"{self.lyric}, {hint_genre}, {self.decade}s"
        return hint_string

    def get_answer(self, lyric_guess, artist_guess):
        self.lyric_guess = lyric_guess
        self.artist_guess = artist_guess
        return (f"You guessed {self.lyric_guess} by {self.artist_guess}. The answer is {self.title} "
                f"by {Artist.get_artist(self.artist)}.")


class Genre:
    def __init__(self, genre):
        self.genre = genre
        assert genre in GENRE_SET

    def get_genre(self):
        return self.genre


class Artist:
    def __init__(self, artist):
        self.artist = artist
        assert artist in ARTIST_SET

    def get_artist(self):
        return self.artist
