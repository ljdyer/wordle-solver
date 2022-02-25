"""
wordle_simulator.py

Simulate a Wordle game in order to test Wordle-solving algorithms.
"""

from wordle_solver import WordleSolver

class WordleSimulator:

    # ====================
    def __init__(self, solution: str):

        self.solution = solution
        self.guesses_so_far = 0
        self.solved = False

    # ====================
    def guess_word(self, word: str) -> list:

        if not len(word) == 5:
            raise ValueError('Words must be five letters long.')
        result = []
        for position, letter in enumerate(word):
            if self.solution[position] == letter:
                result.append('correct')
            elif letter in self.solution:
                result.append('present')
            else:
                result.append('absent')
        self.guesses_so_far += 1

        if all(letter_result == 'correct' for letter_result in result):
            self.solved = True
            self.solved_in = self.guesses_so_far

        return result
