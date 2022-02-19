from words import ALL_WORDS
import string

class WordleGame:

    # ====================
    def __init__(self):

        self.available_words = ALL_WORDS
        self.confirmed_letters = "_____"
        self.present = []
        self.absent = []
        self.not_in_position = []
        self.solved = False

    # ====================
    def update(self, suggestion: str, result: list):

        # Update confirmed letters and present/absent lists based on
        # latest result
        confirmed_letters = list(self.confirmed_letters)
        for i in range(5):
            if result[i] == 'correct':
                confirmed_letters[i] = suggestion[i]
            elif result[i] == 'present':
                self.present.append(suggestion[i])
                self.not_in_position.append((suggestion[i], i))
            elif result[i] == 'absent':
                self.absent.append(suggestion[i])
        self.confirmed_letters = ''.join(confirmed_letters)
        if "_" not in self.confirmed_letters:
            self.solved = True
            return

        # Update lists of 'present' and 'absent' letters and available words
        self.available_words = [
            word for word in self.available_words
            if contains_all(word, self.present)
            and does_not_contain(word, self.absent)
            and does_not_contain_in_position(word, self.not_in_position)
            and matches_confirmed_letters(word, self.confirmed_letters)
        ]
        print(len(self.available_words))

    # ====================
    def get_suggestion(self):

        # Count occurences of each letter in each position
        position_letter_counts = {i: {letter: 0
                                      for letter in string.ascii_letters}
                                  for i in range(5)}
        for word in self.available_words:
            for i in range(5):
                position_letter_counts[i][word[i]] += 1

        # Calculate probabilities of each letter in each position
        num_words = len(self.available_words)
        position_letter_probabilities = {
            i: {letter: count/num_words
                for letter, count in position_letter_counts[i].items()}
            for i in range(5)
        }

        # Only suggest words with repeated letters if there are no other options
        words = [word for word in self.available_words
                 if no_repeated_letters(word)]
        if not words:
            words = self.available_words

        # Get probability of each word
        word_probabilities = [(sum([position_letter_probabilities[i][letter]
                                    for i, letter in enumerate(list(word))]),
                               word)
                              for word in words]
        return max(word_probabilities)[1]


# ====================
def matches_confirmed_letters(word, confirmed_letters):

    for index, letter in enumerate(confirmed_letters):
        if letter != "_":
            if word[index] != letter:
                return False
    else:
        return True


# ====================
def contains_all(word, letters):

    for letter in letters:
        if letter not in word:
            return False
    else:
        return True


# ====================
def does_not_contain(word, letters):

    for letter in letters:
        if letter in word:
            return False
    else:
        return True


# ====================
def does_not_contain_in_position(word, letters_and_positions):

    for letter, position in letters_and_positions:
        if word[position] == letter:
            return False
    else:
        return True


# ====================
def no_repeated_letters(word):

    for letter in word:
        if word.count(letter) > 1:
            return False
    else:
        return True
