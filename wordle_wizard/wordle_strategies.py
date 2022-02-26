"""
Strategy 1: Probabilities of letters in positions
Strategy 2: Probabilities of letters, regardless of position
"""

from collections import Counter
from helper.json_helper import load_json

FREQUENT_WORDS = load_json('word_freqs/frequent_words.json')


# ====================
def strategy_1(available_words: list):
    """Probability of letters in positions"""

    # Count occurences of each letter in each position among the
    # available words
    position_letter_counts = {
        i: Counter([word[i] for word in available_words])
        for i in range(5)
    }

    # Only suggest words with repeated letters if there are no other
    # options
    words = [word for word in available_words
             if no_repeated_letters(word)]
    if not words:
        words = available_words

    # Get sum of counts for each word
    word_probabilities = [
        sum([position_letter_counts[i][letter]
            for i, letter in enumerate(list(word))])
        for word in words
    ]
    # Get word with highest total count
    _, suggestion = max(zip(word_probabilities, words))

    return suggestion


# ====================
def strategy_2(available_words: list):
    """Probabilities of letters, regardless of position"""

    # Count occurences of each letter among the available words
    letter_counts = Counter()
    for word in available_words:
        letter_counts.update(list(word))

    # Only suggest words with repeated letters if there are no other
    # options
    words = [word for word in available_words
             if no_repeated_letters(word)]
    if not words:
        words = available_words

    # Get sum of counts for each word
    word_probabilities = [sum([letter_counts[letter] for letter in word])
                          for word in words]
    # Get word with highest total count
    _, suggestion = max(zip(word_probabilities, words))

    return suggestion


"""COMING SOON"""

# # ====================
# def strategy_3(available_words: list):
#     """Probability of letters in positions, with bonus for frequent words"""

#     # Count occurences of each letter in each position among the
#     # available words
#     position_letter_counts = {
#         i: Counter([word[i] for word in available_words])
#         for i in range(5)
#     }

#     # Only suggest words with repeated letters if there are no other
#     # options
#     words = [word for word in available_words
#              if no_repeated_letters(word)]
#     if not words:
#         words = available_words

#     # Get sum of counts for each word
#     word_probabilities = [
#         sum([position_letter_counts[i][letter]
#             for i, letter in enumerate(list(word))])
#         * get_frequency_bonus(word)
#         for word in words
#     ]

#     # Get word with highest total count
#     _, suggestion = max(zip(word_probabilities, words))

#     return suggestion


# ====================
def no_repeated_letters(word: str) -> bool:
    """Return True only if no letter appears more than once in the word"""

    return all([word.count(letter) < 2 for letter in word])


# # ====================
# def get_frequency_bonus(word: str) -> bool:

#     try:
#         freq_rank = FREQUENT_WORDS.index(word)
#     except ValueError:
#         freq_rank = 0
#     finally:
#         if freq_rank:
#             return 2/(freq_rank ** -3)
#         else:
#             return 1
