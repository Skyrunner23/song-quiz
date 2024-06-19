# Things we'll need:
# -- Get today's clue
#    == internal to function will need to look at date
#    == can cache Puzzle() in memory; if not in memory, then call DB reader
#    == what if Puzzle() isn't found?
# -- Get yesterday's answer

'''
From original code in Puzzle
  -- Move to HTML?

def get_answer(self, lyric_guess, artist_guess):
    """I'd like to move this code (eventually) to the business logic, not the class"""
    self.lyric_guess = lyric_guess
    self.artist_guess = artist_guess
    return (
        f"You guessed {lyric_guess} by {artist_guess}. The answer is {self.answer.title} by {self.answer.artist}.")
'''