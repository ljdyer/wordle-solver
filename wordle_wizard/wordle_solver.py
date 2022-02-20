"""
wordle_solver.py

Defines a class WordleGame that decides which word to guess next in a game
of Wordle based on probabilities of each letter occuring in each position.
"""

from words import ALL_WORDS
from collections import Counter


# ====================
class WordleGame:

    """
    A class to represent a smart AI playing a game of Wordle.

    Methods:

        update(result: list)
            Update the list of available words based on the
            last result

        get_suggestion()
            Suggests the best word to play next given the
            currently available words
        """

    # ====================
    def __init__(self):

        self.available_words = ALL_WORDS
        self.confirmed_letters = "_____"
        self.present = []
        self.absent = []
        self.not_in_position = []
        self.prev_guess = None

    # ====================
    def update(self, result: list):
        """Update the list of available words based on the last result"""

        # Update confirmed letters and present/absent lists based on
        # the latest result
        confirmed_letters = list(self.confirmed_letters)
        for i in range(5):
            if result[i] == 'correct':
                confirmed_letters[i] = self.prev_guess[i]
            elif result[i] == 'present':
                self.present.append(self.prev_guess[i])
                self.not_in_position.append((self.prev_guess[i], i))
            elif result[i] == 'absent':
                self.absent.append(self.prev_guess[i])
        self.confirmed_letters = ''.join(confirmed_letters)

        # Update list of available words
        self.available_words = [
            word for word in self.available_words
            if contains_all(word, self.present)
            and does_not_contain(word, self.absent)
            and does_not_contain_in_position(word, self.not_in_position)
            and matches_confirmed_letters(word, self.confirmed_letters)
        ]

    # ====================
    def get_suggestion(self):
        """Suggest the best word to play next given the currently available
        words"""

        # Count occurences of each letter in each position among the
        # available words
        position_letter_counts = {
            i: Counter([word[i] for word in self.available_words])
            for i in range(5)
        }

        # Note: A previous iteration of this method divided each count by
        # the total number of words to get probabilities that sum to 1, but
        # since the total number of words does not change this step does not
        # make a difference so has been removed.

        # Only suggest words with repeated letters if there are no other
        # options
        words = [word for word in self.available_words
                 if no_repeated_letters(word)]
        if not words:
            words = self.available_words

        # Get sum of counts for each word
        word_probabilities = [
            sum([position_letter_counts[i][letter]
                 for i, letter in enumerate(list(word))])
            for word in words
        ]
        # Get word with highest total count
        _, suggestion = max(zip(word_probabilities, words))
        # Remember the word suggested for the next update
        self.prev_guess = suggestion
        return suggestion


# ====================
def matches_confirmed_letters(word: str, confirmed_letters: str) -> bool:
    """confirmed_letters is a string containing letters and underscores to
    indicate which letters are confirmed in which positions.

    For example, 's_i__' indicates that the first letter must be 's' and the
    third letter must be 'i', but there can be any letters in the remaining
    positions.

    Return True only if the word matches the confirmed letters"""

    return all([word[position] == letter
                for position, letter in enumerate(confirmed_letters)
                if letter != "_"])


# ====================
def contains_all(word: str, letters: list) -> bool:
    """Return True only if the word contains all of the letters
    in the list"""

    return all([letter in word for letter in letters])


# ====================
def does_not_contain(word: str, letters: list) -> bool:
    """Return True only if the word does not contain any of the letters
    in the list"""

    return all([letter not in word for letter in letters])


# ====================
def does_not_contain_in_position(word: str,
                                 letters_and_positions: list) -> bool:
    """letters_and_positions is a list of letters and number tuples, where
    positions are between 0 and 4 (because words are 5 letters long)
    E.g. [('l', 2), ('z', 0)].

    Return True only if word does not contain the letter in the position
    indicated for all of the tuples in the list.
    """

    return all([word[position] != letter
                for letter, position in letters_and_positions])


# ====================
def no_repeated_letters(word: str) -> bool:
    """Return True only if no letter appears more than once in the word"""

    return all([word.count(letter) < 2 for letter in word])
