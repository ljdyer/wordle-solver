from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from wordle_solver import WordleGame
import traceback

WORDLE_HOME = 'https://www.nytimes.com/games/wordle/index.html'
ENTER_KEY = '↵'


# ====================
def play_wordle(driver):

    # Get ready to play in browser window
    driver.get(WORDLE_HOME)
    sleep(1)
    agree_cookies(driver)
    sleep(0.5)
    close_instructions(driver)
    sleep(0.5)
    keyboard = get_keyboard(driver)

    # Start the game simulator
    this_game = WordleGame()
    guesses_so_far = 0

    while not this_game.solved:
        suggestion = this_game.get_suggestion()
        guess_word(keyboard, suggestion)
        sleep(3)
        result = get_row_result(driver, guesses_so_far)
        this_game.update(suggestion, result)
        guesses_so_far += 1
    sleep(10)


# ======================
def get_game_app(driver):

    game_app = driver.find_element(By.CSS_SELECTOR, "game-app")
    game_app_shadow_root = game_app.shadow_root
    return game_app_shadow_root


# ======================
def get_game_theme_manager(driver):

    # Game theme manager appears to be a shadow host based on looking at
    # the DOM, but for some reason we don't have to get the shadow root
    game_app = get_game_app(driver)
    game_theme_manager = game_app.find_element(By.CSS_SELECTOR, "game-theme-manager")
    return game_theme_manager


# ======================
def get_keyboard(driver):

    game_theme_manager = get_game_theme_manager(driver)
    game_keyboard = game_theme_manager.find_element(By.CSS_SELECTOR, "game-keyboard")
    game_keyboard_shadow_root = game_keyboard.shadow_root
    return game_keyboard_shadow_root


# ====================
def get_row(driver, row_num: int):

    game_theme_manager = get_game_theme_manager(driver)
    row_one = game_theme_manager.find_elements(By.CSS_SELECTOR, "game-row")[row_num]
    row_one_shadow_root = row_one.shadow_root
    return row_one_shadow_root


# ====================
def get_row_result(driver, row_num):

    result = []
    row = get_row(driver, row_num)
    for i in range(5):
        letter = row.find_elements(By.CSS_SELECTOR, "game-tile")[i]
        letter_shadow_root = letter.shadow_root
        tile_div = letter_shadow_root.find_element(By.CSS_SELECTOR, "div.tile")
        result.append(tile_div.get_attribute('data-state'))
    return result


# ====================
def agree_cookies(driver):

    if agree_cookies := driver.find_elements(By.XPATH, '//*[@id="pz-gdpr-btn-accept"]'):
        agree_cookies[0].click()


# ====================
def close_instructions(driver):

    if game_area := driver.find_elements(By.TAG_NAME, 'body'):
        game_area[0].click()


# ====================
def press_key(keyboard, key: str):

    button = keyboard.find_element(By.CSS_SELECTOR, f"button[data-key={key}]")
    button.click()


# ====================
def guess_word(keyboard, word: str, delay_time: float = 0.5):

    if not len(word) == 5:
        raise ValueError('Words must be five letters long.')
    else:
        for letter in word:
            press_key(keyboard, letter.lower())
            sleep(delay_time)
        press_key(keyboard, ENTER_KEY)


# ====================
if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('./chromedriver', options=options)
    # driver = webdriver.Chrome('./chromedriver')

    try:
        play_wordle(driver)
    except Exception as e:
        print('The following exception occured:')
        print(traceback.format_exc())
        quit()
    else:
        print('the program terminated normally.')
    finally:
        driver.quit()
        print('The driver has been terminated.')
