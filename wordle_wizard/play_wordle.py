"""
play_wordle.py

See repo README.md for details.

Functions:

    play_wordle()
        Opens a browser window with today's Wordle puzzle and automatically
        solves it.

Running play_wordle.py from the terminal calls play_wordle()
"""

from time import sleep

from wordle_controller import WordleController
from wordle_solver import WordleGame

# Number of seconds to wait before playing the game after loading the page
WAIT_BEFORE = 1
# Number of seconds to wait after completing the game before closing the
# browser window
WAIT_AFTER = 60


# ====================
def play_wordle():

    wordle_controller = WordleController()
    this_game = WordleGame()
    # Pause for a moment before beginning
    sleep(WAIT_BEFORE)

    while not wordle_controller.completed:
        suggestion = this_game.get_suggestion()
        result = wordle_controller.guess_word(suggestion)
        this_game.update(result)

    # Give the user some time to admire the result
    sleep(WAIT_AFTER)


# ====================
if __name__ == "__main__":

    play_wordle()
