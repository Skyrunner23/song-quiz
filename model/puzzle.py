from dataclasses import dataclass

@dataclass
class Clue:
    """A class representing a clue for a puzzle.

    Attributes:
        lyric (str): The lyric associated with the clue
        genre (Genre): The genre associated with the clue
        year (int): The year of the clue

    Raises:
        TypeError: If the types of `lyric` or `year` are not as expected.
    """

    def __init__(self, lyric, genre, year):
        if not isinstance(lyric, str):
            raise TypeError(f'[Clue] invalid lyric type: {lyric} should be string, is {type(lyric)}')
        if not isinstance(year, int):
            raise TypeError(f'[Clue] invalid year type: {year} should be int, is {type(year)}')
        self.lyric = lyric
        self.genre = Genre(genre)
        self.year = year


    def serialize(self):
        return {'lyric': self.lyric,
                'genre': self.genre.serialize(),
                'year': self.year}

    @staticmethod
    def _round_decade(year):
        """make sure the year ends with a zero"""
        return int(year / 10) * 10

    def __str__(self):
        return f"{self.lyric}, {self.genre}, {self.year}s"

    def __repr__(self):
        return f'Clue("{self.lyric}", "{self.genre}", "{self.year}")'

    def __eq__(self, other):
        if not isinstance(other, Clue):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.lyric == other.lyric and \
               self.genre == other.genre and \
               self.year == other.year


@dataclass
class Answer:
    """A class representing an answer for a puzzle.

    Attributes:
        title (str): The title of the song.
        artist (Artist): The artist of the song.

    Raises:
        TypeError: If the type of `title` is not as expected.
    """

    def __init__(self, title, artist):
        if not isinstance(title, str):
            raise TypeError(f'[Answer] invalid lyric type: {title} should be str, is {type(title)}')
        self.title = title
        self.artist = Artist(artist)

    def serialize(self):
        return {'title': self.title,
                'artist': self.artist.serialize()}

    def __str__(self):
        return f"{self.title}, {self.artist}"

    def __repr__(self):
        return f'Answer("{self.title}", "{self.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Answer):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.title == other.title and \
               self.artist == other.artist


@dataclass
class Puzzle:
    """A class representing a puzzle.

    Attributes:
        date (str): The date of the puzzle, format is yyyy/mm/dd
        clue (Clue): The clue associated with the puzzle.
        answer (Answer): The answer associated with the puzzle.
    """

    def __init__(self, date, lyric, genre, year, title, artist):
        self.date = date
        self.clue = Clue(lyric, genre, year)
        self.answer = Answer(title, artist)

    def serialize(self):
        return {'date': self.date,
                'clue': self.clue.serialize(),
                'answer': self.answer.serialize()}


    def __str__(self):
        return f'{self.clue}'

    def __repr__(self):
        return f'Puzzle("{self.date}", "{self.clue.lyric}", "{self.clue.genre}", "{self.clue.year}", "{self.answer.title}", "{self.answer.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Puzzle):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.date == other.date and \
               self.clue == other.clue and \
               self.answer == other.answer


@dataclass
class Genre:
    """A class representing a music genre.

    Attributes:
        genre (str): The genre name.

    Raises:
        TypeError: If the type of `genre` is not a string.
        ValueError: If the provided genre is not in the predefined genre set.
    """
    GENRE_SET = {"Rock", "Pop Rock", "Alt Rock", "Pop", "Metal",
                 "Dance"}

    def __init__(self, genre):
        if not isinstance(genre, str):
            raise TypeError(f'[Genre] invalid genre type: {genre} should be string, is {type(genre)}')
        if genre not in self.GENRE_SET:
            raise ValueError(f'[Genre] invalid genre: {genre} is not in GENRE_SET')
        self.genre = genre

    def serialize(self):
        return str(self)

    def __str__(self):
        return f'{self.genre}'

    def __repr__(self):
        return f'Genre("{self.genre}")'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.genre == other.genre


@dataclass
class Artist:
    """A class representing an artist. No validation is performed.

    Attributes:
        artist (str): The artist name.

    Raises:
        TypeError: If the type of `artist` is not a string.
    """


    def __init__(self, artist):
        if not isinstance(artist, str):
            raise TypeError(f'[Artist] invalid artist type: {artist} should be str, is {type(artist)}')
        self.artist = artist


    def serialize(self):
        return str(self)

    def __str__(self):
        return f'{self.artist}'

    def __repr__(self):
        return f'Artist("{self.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Artist):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.artist == other.artist
