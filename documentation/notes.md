# Things to keep in mind

## Data model

The `Artist` class uses a controlled vocabulary for artist names. This needs to be managed and updated as needed.

The `Genre` class uses a controlled vocabulary for genres. Same consideration.

The `Puzzle.date` attribute is stored as a string, and the assumed format is yyyy/mm/dd to allow alphabetical sorting. Nothing enforces this format, however, and dates are compared as strings (not date objects), so string format must match in order to find a match.