from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
from os import makedirs, getcwd
from os.path import dirname, join
import pandas as pd

URL_LIST_PATH = join(getcwd(), 'urls.txt')
VID_INFO_PATH = join(getcwd(), 'vid_info.xlsx')
TITLE_XPATH = '//*[@id="container"]/h1/yt-formatted-string'
VIEWS_XPATH = '//*[@id="count"]/ytd-video-view-count-renderer/span[1]'
UL_DATE_XPATH = '//*[@id="info-strings"]/yt-formatted-string'


# ====================
def get_vid_info(driver, url):

    driver.get(url)

    try:
        title = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, TITLE_XPATH))).text
    except TimeoutException:
        raise RuntimeError(f'No title found for {url}.')

    try:
        num_views = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, VIEWS_XPATH))).text
        num_views = ''.join([c for c in num_views if c.isnumeric()])
    except TimeoutException:
        raise RuntimeError(f'No number of views found for {url}.')

    try:
        ul_date = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, UL_DATE_XPATH))).text
    except TimeoutException:
        raise RuntimeError(f'No upload date found for {url}.')

    return (title, num_views, ul_date)


# ====================
def get_lines_from_file(file_path: str) -> str:

    with open(file_path, errors='ignore') as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    return lines


# ====================
def get_single_elem_by_xpath(driver, xpath):

    if elem_list := driver.find_elements(By.XPATH, xpath):
        return elem_list[0]
    else:
        return None


# ====================
def get_all_vid_info(driver, url_list):

    total_urls = len(url_list)
    all_vid_info = []
    errors = []

    try:
        for count, url in enumerate(url_list):
            try:
                os.system('cls')
                print(f'Video info obtained for {count} of {total_urls} URLs so far.')
                print(f'Getting video info for {url}.')
                print(url)
                vid_info = get_vid_info(driver, url)
                all_vid_info.append(vid_info)
                if count > 0 and count % 10 == 0:
                    save_to_excel(all_vid_info)
            except RuntimeError as e:
                errors.append(str(e))
                continue
    except KeyboardInterrupt:
        print()
        print(f'You terminated the program when it was checking URL number: {count+1}')
    finally:
        print()
        print(f'Number of errors: {len(errors)}.')
        for error in errors:
            print(error)


# ====================
def save_to_excel(vid_info):

    vid_info_df = pd.DataFrame(vid_info)
    vid_info_df.columns = ['Title', 'Number of views', 'Upload date']
    vid_info_df.to_excel(VID_INFO_PATH)


# ====================
if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./chromedriver', options=options)

    url_list = get_lines_from_file(URL_LIST_PATH)
    print(len(url_list))

    try:
        get_all_vid_info(driver, url_list)
    except Exception as e:
        print(e)
        quit()
    else:
        print('Program terminated normally.')
    finally:
        driver.quit()
        print('Driver has been terminated.')

    driver.quit()
