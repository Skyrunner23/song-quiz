class Clue:
    def __init__(self, lyric, genre, year):
        if not isinstance(lyric, str):
            raise TypeError(f'[Clue] invalid lyric type: {lyric} is {type(lyric)}')
        if not isinstance(genre, str):
            raise TypeError(f'[Clue] invalid genre type: {genre} is {type(genre)}')
        if not isinstance(year, int):
            raise TypeError(f'[Clue] invalid year type: {year} is {type(year)}')
        self.lyric = lyric
        self.genre = Genre(genre)
        self.decade = self._round_decade(year)

    @staticmethod
    def _round_decade(year):
        """make sure the year ends with a zero"""
        return int(year / 10) * 10

    def __str__(self):
        return f"{self.lyric}, {self.genre}, {self.decade}s"


class Answer:
    def __init__(self, title, artist):
        if not isinstance(title, str):
            raise TypeError(f'[Answer] invalid lyric type: {title} is {type(title)}')
        if not isinstance(artist, str):
            raise TypeError(f'[Answer] invalid genre type: {artist} is {type(artist)}')
        self.title = title
        self.artist = Artist(artist)

    def __str__(self):
        return f"{self.title}, {self.artist}"


class Puzzle:
    def __init__(self, date, lyric, genre, year, artist, title):
        self.date = date
        self.clue = Clue(lyric, genre, year)
        self.answer = Answer(title, artist)

        self.lyric_guess = ""
        self.artist_guess = ""

    def get_answer(self, lyric_guess, artist_guess):
        """I'd like to move this code (eventually) to the business logic, not the class"""
        self.lyric_guess = lyric_guess
        self.artist_guess = artist_guess
        return (
            f"You guessed {lyric_guess} by {artist_guess}. The answer is {self.answer.title} by {self.answer.artist}.")

    def __str__(self):
        return f'{self.clue}'


class Genre:
    GENRE_SET = {"Rock", "Pop", "Metal", "Dance"}

    def __init__(self, genre):
        if genre not in self.GENRE_SET:
            raise ValueError(f'[Genre] invalid genre: {genre} is not in GENRE_SET')
        self.genre = genre

    def __str__(self):
        return f'{self.genre}'


class Artist:
    ARTIST_SET = {"Rick Astley", "Taylor Swift", "Weird Al"}

    def __init__(self, artist):
        if artist not in self.ARTIST_SET:
            raise ValueError(f'[Artist] invalid artist: {artist} is not in ARTIST_SET')
        self.artist = artist

    def __str__(self):
        return f'{self.artist}'
