"""
wordle_evaluate.py

Evaluate Wordle-solving algorithms.
"""

import argparse
from collections import Counter
from os.path import join

import matplotlib.pyplot as plt
import numpy
from tqdm import tqdm

from helper.json_helper import load_json, save_json
from wordle_simulator import WordleSimulator
from wordle_solver import WordleSolver
from words import USED_WORDS

RESULTS_JSON = 'evaluate/eval_results.json'
SAVE_FOLDER = 'evaluate'


# ====================
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Evaluate a Wordle strategy',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('strategy',
                        metavar='strategy',
                        type=str,
                        help='The strategy to evaluate')
    parser.add_argument('-d', '--display-only',
                        dest='display_only',
                        action='store_true',
                        help=('Display previously stored information about the strategy,',
                              'without calculating numbers of guesses required again.'))
    return parser.parse_args()


# ====================
def order_counter(counter: Counter) -> dict:

    return dict(sorted(counter.items()))


# ====================
def get_num_guesses(word: str, strategy: str):

    simulator = WordleSimulator(word)
    this_game = WordleSolver(strategy)

    while not simulator.solved:
        suggestion = this_game.get_suggestion()
        result = simulator.guess_word(suggestion)
        this_game.update(result)

    return simulator.solved_in


# ====================
def get_strategy_result(strategy: str):
    """Get the following information about the strategy specified:

        - The starting word suggested by the solver
        - The frequencies of numbers of guesses required for the words
          in USED_WORDS
        - A word that takes the maximum number of guesses
    """

    # Get first word suggested with this strategy
    solver = WordleSolver(strategy)
    starting_word = solver.get_suggestion()

    # Get numbers of guesses for all words and word that takes maximum
    # number of guesses
    print(f'Getting numbers of guesses for {strategy}.')
    max_guesses = 0
    max_word = None

    all_num_guesses = []
    for word in tqdm(USED_WORDS):
        num_guesses = get_num_guesses(word, strategy=strategy)
        all_num_guesses.append(num_guesses)
        if num_guesses > max_guesses:
            max_guesses = num_guesses
            max_word = word
    print('Finished.')

    return {
        'num_guess_frequencies': Counter(all_num_guesses),
        'starting_word': starting_word,
        'max_word': max_word
    }


# ====================
def display_strategy_info(strategy: str, strategy_info: dict):

    print(f"- Starting word: {strategy_info['starting_word']}")

    # Get words and number of guesses for max_word
    simulator = WordleSimulator(strategy_info['max_word'])
    this_game = WordleSolver(strategy)

    # Get information abuot solution for word requiring maximum amount of
    # guesses
    guesses = []
    while not simulator.solved:
        suggestion = this_game.get_suggestion()
        guesses.append(suggestion)
        result = simulator.guess_word(suggestion)
        this_game.update(result)
    print(f"- Highest number of guesses: {simulator.solved_in}",
          f"for word '{strategy_info['max_word']}'")
    print(' ⇒  '.join(guesses))

    # Generate array of guess numbers from dictionary of frequencies
    all_num_guesses = []
    for num_guesses, frequency in strategy_info[
                                'num_guess_frequencies'].items():
        all_num_guesses.extend([int(num_guesses)] * frequency)

    # Win rate
    win = len([num_guesses for num_guesses in all_num_guesses
               if num_guesses <= 6])
    print(f"- Win rate: {(win/len(all_num_guesses))*100:.2f}%")

    # Mean and standard deviation
    print(f"- Mean: {numpy.mean(all_num_guesses):.2f} guesses")
    print(f"- Standard deviation: {numpy.std(all_num_guesses):.2f} guesses")

    # Display histogram
    plt.hist(all_num_guesses)
    plt.ylabel('Number of guesses')
    plt.xlabel('Frequency (distinct words)')
    plt.title(f'Number of guesses required for words when using {strategy}')
    plt.savefig(join(SAVE_FOLDER, f'{strategy}.png'))
    plt.show()


# ====================
def main():

    # Get command line arguments
    args = get_args()
    strategy = args.strategy
    display_only = args.display_only
    # Get peviously stored results
    results = load_json(RESULTS_JSON)

    if not display_only:
        results[strategy] = get_strategy_result(strategy)
    display_strategy_info(strategy, results[strategy])
    save_json(results, RESULTS_JSON)


# ====================
if __name__ == "__main__":

    main()
