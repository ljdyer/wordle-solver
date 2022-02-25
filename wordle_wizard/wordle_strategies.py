"""
Strategy 1: Probabilities of letters in positions
Strategy 2: Probabilities of letters, regardless of position
"""

from collections import Counter


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


# ====================
def no_repeated_letters(word: str) -> bool:
    """Return True only if no letter appears more than once in the word"""

    return all([word.count(letter) < 2 for letter in word])
