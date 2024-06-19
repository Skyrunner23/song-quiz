
class Clue:
    """A class representing a clue for a puzzle.

    Attributes:
        lyric (str): The lyric associated with the clue.
        genre (Genre): The genre associated with the clue.
        decade (int): The decade of the clue's year.

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
        self.decade = self._round_decade(year)

    @staticmethod
    def _round_decade(year):
        """make sure the year ends with a zero"""
        return int(year / 10) * 10

    def __str__(self):
        return f"{self.lyric}, {self.genre}, {self.decade}s"

    def __repr__(self):
        return f'Clue("{self.lyric}", "{self.genre}", "{self.decade}")'

    def __eq__(self, other):
        if not isinstance(other, Clue):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.lyric == other.lyric and \
               self.genre == other.genre and \
               self.decade == other.decade


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


class Puzzle:
    """A class representing a puzzle.

    Attributes:
        date (str): The date of the puzzle, format is yyyy/mm/dd
        clue (Clue): The clue associated with the puzzle.
        answer (Answer): The answer associated with the puzzle.
        lyric_guess (str): A guess for the lyric of the song.
        artist_guess (str): A guess for the artist of the song.
    """

    def __init__(self, date, lyric, genre, year, title, artist):
        self.date = date
        self.clue = Clue(lyric, genre, year)
        self.answer = Answer(title, artist)

        self.lyric_guess = ""
        self.artist_guess = ""


    def __str__(self):
        return f'{self.clue}'

    def __repr__(self):
        return f'Puzzle("{self.date}", "{self.clue.lyric}", "{self.clue.genre}", "{self.clue.decade}", "{self.answer.title}", "{self.answer.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Puzzle):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.date == other.date and \
               self.clue == other.clue and \
               self.answer == other.answer


class Genre:
    """A class representing a music genre.

    Attributes:
        genre (str): The genre name.

    Raises:
        TypeError: If the type of `genre` is not a string.
        ValueError: If the provided genre is not in the predefined genre set.
    """
    GENRE_SET = {"Rock", "Pop", "Metal", "Dance"}

    def __init__(self, genre):
        if not isinstance(genre, str):
            raise TypeError(f'[Genre] invalid genre type: {genre} should be string, is {type(genre)}')
        if genre not in self.GENRE_SET:
            raise ValueError(f'[Genre] invalid genre: {genre} is not in GENRE_SET')
        self.genre = genre

    def __str__(self):
        return f'{self.genre}'

    def __repr__(self):
        return f'Genre("{self.genre}")'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.genre == other.genre


class Artist:
    """A class representing an artist.

    Attributes:
        artist (str): The artist name.

    Raises:
        TypeError: If the type of `artist` is not a string.
        ValueError: If the provided artist is not in the predefined artist set.
    """
    ARTIST_SET = {"Rick Astley", "Taylor Swift", "Weird Al", "Queen"}

    def __init__(self, artist):
        if not isinstance(artist, str):
            raise TypeError(f'[Artist] invalid artist type: {artist} should be str, is {type(artist)}')
        if artist not in self.ARTIST_SET:
            raise ValueError(f'[Artist] invalid artist: {artist} is not in ARTIST_SET')
        self.artist = artist

    def __str__(self):
        return f'{self.artist}'

    def __repr__(self):
        return f'Artist("{self.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Artist):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.artist == other.artist
