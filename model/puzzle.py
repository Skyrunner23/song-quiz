from dataclasses import dataclass
import re


@dataclass
class Submission:
    """A class representing a user's submitted answer for a puzzle.

    Attributes:
        name (str): The name of the submitter.
        date (str): The date whose puzzle this is a submission for, format is yyyy/mm/dd.
        title (str): The submitted song title.
        artist (str): The submitted artist.

    Only the name is required; the artist and song title can be blank.

    The artist and song cannot comprise an Answer object, since the artist and
    song title in an Answer will each be paired with a regular expression for grading.
    """

    def __init__(self, name, date, title="", artist=""):
        if not isinstance(name, str):
            raise TypeError(f'[Submission] invalid type: {name} should be str, is {type(name)}')
        if name == "":
            raise ValueError(f'[Submission] invalid value: {name} cannot be empty')
        if not isinstance(date, str):
            raise TypeError(f'[Submission] invalid type: {date} should be str, is {type(date)}')
        if not re.fullmatch(r"\d{4}/\d{2}/\d{2}", date):
            raise ValueError(f'[Submission] invalid value: {date} is not in yyyy/mm/dd format')
        if not isinstance(title, str):
            raise TypeError(f'[Submission] invalid type: {title} should be str, is {type(title)}')
        if not isinstance(artist, str):
            raise TypeError(f'[Submission] invalid type: {artist} should be str, is {type(artist)}')
        self.name = name
        self.date = date
        self.title = title
        self.artist = artist

    def serialize(self) -> dict:
        return {'name': self.name, 'date': self.date, 'title': self.title,
                'artist': self.artist}

    def __str__(self):
        return f"{self.name}, {self.date}, {self.title}, {self.artist}"

    def __repr__(self):
        return f'Submission("{self.name}", "{self.date}", "{self.title}", "{self.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Submission):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name and \
            self.date == other.date and \
            self.title == other.title and \
            self.artist == other.artist


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

    def serialize(self) -> dict:
        return {'lyric': self.lyric,
                'genre': self.genre.serialize(),
                'year': self.year}

    @staticmethod
    def _round_decade(year):
        """make sure the year ends with a zero"""
        return int(year / 10) * 10

    def __str__(self):
        return f"{self.lyric}, {self.genre}, {self.year}"

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

    Parameters:
        title (str): The title of the song.
        titlematch (str): A regex for matching the title
        artist (str): The artist of the song.
        artistmatch (str): A regex for matching the artist

    Methods:
        grade(Submission) -> bool: True if Submission matches title and artist

    Raises:
        TypeError: If the type of `title` is not as expected.
    """

    def __init__(self, title, titlematch, artist, artistmatch):
        for param in [title, titlematch, artist, artistmatch]:
            if not isinstance(param, str):
                raise TypeError(f'[Answer] invalid type: {param} should be str, is {type(param)}')
        self.title = title
        self._titlematch = titlematch
        self._artistobj = Artist(artist, artistmatch)
        self.artist = self._artistobj.artist
        # A bit of a fudge:
        self._artistmatch = self._artistobj.artistmatch

    def serialize(self) -> dict:
        return {'title': self.title,
                'artist': self.artist}

    def grade(self, submission: Submission) -> dict:
        """
        Grade a Submission against this Answer

        :param submission:
        :return: a dictionary with the following format:
        {'title': True/False, 'artist': True/False}
            each value is True if the submission matches, else False
        """
        components = ['title', 'artist']
        gradingkeys = ['_titlematch', '_artistmatch']
        grade = {component: False for component in components}
        for component, gradingkey in zip(components, gradingkeys):
            tograde = getattr(submission, component)
            gradeagainst = getattr(self, gradingkey)
            grade[component] = True if re.fullmatch(gradeagainst, tograde, flags=re.I) else False
        return grade

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

    def __init__(self, date, lyric, genre, year, title, titlematch, artist, artistmatch):
        self.date = date
        self.clue = Clue(lyric, genre, year)
        self.answer = Answer(title, titlematch, artist, artistmatch)

    def serialize(self) -> dict:
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
    """

    def __init__(self, genre):
        if not isinstance(genre, str):
            raise TypeError(f'[Genre] invalid genre type: {genre} should be string, is {type(genre)}')
        self.genre = genre

    def serialize(self) -> str:
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

    Parameters:
        artist (str): The artist name.
        artistmatch (str): A regex for matching the artist.

    Raises:
        TypeError: If the type of `artist` is not a string.
    """

    def __init__(self, artist, artistmatch):
        for param in [artist, artistmatch]:
            if not isinstance(param, str):
                raise TypeError(f'[Artist] invalid artist type: {param} should be str, is {type(param)}')
        self.artist = artist
        self.artistmatch = artistmatch

    def serialize(self) -> dict:
        return {'artist': self.artist, 'artistmatch': self.artistmatch}

    def __str__(self):
        return f'{self.artist}'

    def __repr__(self):
        return f'Artist("{self.artist}")'

    def __eq__(self, other):
        if not isinstance(other, Artist):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.artist == other.artist
