"""
wordle_controller.py

Defines a class WordleController for playing Wordle by manipulating
a browser window with selenium.
"""

import atexit
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WORDLE_HOME = 'https://www.nytimes.com/games/wordle/index.html'
ENTER_KEY = '↵'
ACCEPT_COOKIES_XPATH = '//*[@id="pz-gdpr-btn-accept"]'
DEFAULT_WAIT_AFTER_KEY_PRESS = 0.25
DEFAULT_WAIT_AFTER_ENTER_WORD = 2


class WordleController:
    """
    A class to represent a browser window that is displaying the Wordle
    website.

    Method called directly by play_wordle.py:

        guess_word(word: str) -> list
            Enters a word into the game board and returns the result as
            a list of strings ('correct', 'present' or 'absent')
    """

    # ====================
    def __init__(self,
                 wait_after_key_press: float = DEFAULT_WAIT_AFTER_KEY_PRESS,
                 wait_after_enter_word: float = DEFAULT_WAIT_AFTER_ENTER_WORD):

        # Initialize web driver
        self.init_driver()

        # Always quit driver when app finishes
        @atexit.register
        def kill_me():
            self.kill()

        # Get the Wordle page ready
        self.driver.get(WORDLE_HOME)
        self.accept_cookies()
        self.close_instructions()

        # Get access to parts of DOM inside shadow trees
        self.init_game_app()
        self.init_game_theme_manager()
        self.init_keyboard()

        # Set options attributes
        self.wait_after_key_press = wait_after_key_press
        self.wait_after_enter_word = wait_after_enter_word

        # Initialize other attributes
        self.last_played_row = -1
        self.completed = False

    # ====================
    def init_driver(self):
        """Initialise the main web driver"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome('./chromedriver', options=options)

    # ====================
    def accept_cookies(self):
        """Click the button to accept cookies"""

        try:
            (WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  ACCEPT_COOKIES_XPATH)))
                .click())
        except TimeoutException:
            # It's possible the cookies dialogue wasn't displayed, so move on
            # for now
            pass

    # ====================
    def close_instructions(self):
        """Close the instructions modal"""

        # Instructions are displayed in a modal that disappears when we click
        # anywhere in the document body
        try:
            (WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                .click())
        except TimeoutException:
            # This is an problem. Raise an exception.
            raise RuntimeError('Unable to locate document body.')

    # ====================
    def init_game_app(self):
        """Get access to the part of the DOM inside the tag <game-app>, which
        is a shadow host"""

        self.game_app = (self.driver.find_element(By.CSS_SELECTOR, "game-app")
                         .shadow_root)

    # ====================
    def init_game_theme_manager(self):
        """Get access to the part of DOM inside the tag <game-theme-manager>,
        which appears to be a shadow host from inspection of the HTML but for
        some reason can be accessed as-is"""

        self.game_theme_manager = (self.game_app
                                   .find_element(By.CSS_SELECTOR,
                                                 "game-theme-manager"))

    # ====================
    def init_keyboard(self):
        """Get access to the part of the DOM inside the tag <keyboard>, which
        is a shadow host"""

        self.keyboard = (self.game_theme_manager
                         .find_element(By.CSS_SELECTOR, "game-keyboard")
                         .shadow_root)

    # ====================
    def guess_word(self, word: str) -> list:
        """Enter a word into the game board and get the result"""

        self.enter_word(word)
        return self.get_last_played_row_result()

    # ====================
    def get_last_played_row_result(self) -> list:
        """Get the result from the last played row on the game board

        Returns a list of 5 strings which are either 'correct', 'absent', or
        'present'

        E.g. ['correct', 'absent', 'absent', 'present', 'absent']"""

        row = (self.game_theme_manager
               .find_elements(
                   By.CSS_SELECTOR, "game-row")[self.last_played_row]
               .shadow_root)
        tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
        result = []
        for i in range(5):
            tile = tiles[i].shadow_root
            tile_div = tile.find_element(By.CSS_SELECTOR, "div.tile")
            result.append(tile_div.get_attribute('data-state'))
        if all([x == 'correct' for x in result]):
            self.completed = True
        return result

    # ====================
    def enter_word(self, word: str):
        """Enter a word into the next row of the game board"""

        if not len(word) == 5:
            raise ValueError('Words must be five letters long.')
        else:
            for letter in word:
                self.press_key(letter.lower())
                sleep(self.wait_after_key_press)
            self.press_key(ENTER_KEY)
        self.last_played_row += 1
        sleep(self.wait_after_enter_word)

    # ====================
    def press_key(self, key: str):
        """Press a key on the keyboard"""

        button = (self.keyboard
                  .find_element(By.CSS_SELECTOR, f"button[data-key={key}]"))
        button.click()

    # ====================
    def kill(self):
        """Quit the driver"""

        self.driver.quit()
        print('Driver terminated.')
        print()
