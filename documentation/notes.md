# Things to keep in mind

## Data model

The `Artist` class uses a controlled vocabulary for artist names. This needs to be managed and updated as needed.

The `Genre` class uses a controlled vocabulary for genres. Same consideration.

The `Puzzle.date` attribute is stored as a string, and the assumed format is yyyy/mm/dd to allow alphabetical sorting. Nothing enforces this format, however, and dates are compared as strings (not date objects), so string format must match in order to find a match.

DONE: implement a `__repr__` method for Puzzle objects?

Right now, the `MyCSVRepository()` class in reader.py does not validate the data, and doesn't do anything to check whether a `Puzzle()` was found for a given date. If no `Puzzle()` was found, it returns `None`.