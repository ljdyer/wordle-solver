"""
play_wordle.py

See repo README.md for details.

Main function:

    play_wordle()
        Opens a browser window with today's Wordle puzzle and automatically
        solves it.

Running play_wordle.py from the terminal calls play_wordle()
"""

from time import sleep

from wordle_controller import WordleController
from wordle_solver import WordleSolver

# Number of seconds to wait before loading the page after opening comment
WAIT_BEFORE_BROWSER_OPEN = 1
# Number of seconds to wait before playing the game after loading the page
WAIT_BEFORE_GAME_PLAY = 1
# Number of seconds to wait after completing the game before closing the
# browser window
WAIT_AFTER_GAME_PLAY = 5


# ====================
def play_wordle():

    print()
    print('Ready? Time to watch a real Wordle master at work.')
    print()
    sleep(WAIT_BEFORE_BROWSER_OPEN)

    wordle_controller = WordleController()
    this_game = WordleSolver()
    # Pause for a moment before beginning
    sleep(WAIT_BEFORE_GAME_PLAY)

    while not wordle_controller.completed:
        suggestion = this_game.get_suggestion()
        result = wordle_controller.guess_word(suggestion)
        this_game.update(result)

    num_guesses = wordle_controller.last_played_row + 1
    display_closing_comment(num_guesses)
    print()
    # Give the user some time to admire the result
    sleep(WAIT_AFTER_GAME_PLAY)


# ====================
def display_closing_comment(num_guesses):

    if num_guesses == 1:
        print('Got it in 1! I guess today was my lucky day.')
    if num_guesses == 2:
        print('Got it in 2! Bow down to your AI master.')
    if num_guesses == 3:
        print('Got it in 3. Solid performance.')
    if num_guesses == 4:
        print("Got it in 4. Not bad, but I know I'll do better tomorrow.")
    if num_guesses >= 5:
        print(f"Hmm... it took me {num_guesses} attempts.",
              "Well, I was still quicker than you!")


# ====================
if __name__ == "__main__":

    play_wordle()
