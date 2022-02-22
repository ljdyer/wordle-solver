from collections import Counter


# ====================
def letter_probs(available_words: list):
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
def letter_position_probs(available_words: list):
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
def no_repeated_letters(word: str) -> bool:
    """Return True only if no letter appears more than once in the word"""

    return all([word.count(letter) < 2 for letter in word])
