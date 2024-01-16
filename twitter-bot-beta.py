import csv
import os
import time
from configparser import ConfigParser
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import TwitterUser
from selenium import webdriver

from TwitterLogin import TwitterLogin


def is_element_present(driver, selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
        print("Element " + selector + " exists!")
        return True
    except NoSuchElementException:
        print("Element " + selector + " not existed!")
        return False


def do_login(wait, user):
    button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/login']")))
    button.click()

    twitter_login = TwitterLogin()

    twitter_login.fill_current_session_login(wait, user)
    twitter_login.fill_current_session_login(wait, user)
    twitter_login.fill_current_session_login(wait, user)
    twitter_login.fill_current_session_login(wait, user)
    # fill_current_session_login(wait, user)


def post_content(wait):
    # Open the file for reading
    f = open('input/post_content.txt', 'r')

    # Read the whole file content
    post_content_txt = f.read()

    textarea_post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetTextarea_0"]')))
    textarea_post.send_keys(post_content_txt)

    button_post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
    button_post.click()

    # Close the file
    f.close()

    print("Post " + post_content_txt)

    time.sleep(3)


def follow_user(driver, wait):
    f = open('input/following.txt', 'r')

    user_following = f.read()

    driver.get("https://twitter.com/" + user_following)

    css_user_following = '//div[@aria-label="Follow @' + user_following + '"]'

    button_follow = wait.until(EC.presence_of_element_located((By.XPATH, css_user_following)))
    button_follow.click()

    f.close()


def post_image(driver, wait):
    driver.get("https://twitter.com")

    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "input", "post_image.png"))

    print(image_path)

    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="fileInput"]')))
    file_input.send_keys(image_path)

    f = open('input/post_content.txt', 'r')
    post_content_txt = f.read()
    f.close()

    textarea_post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetTextarea_0"]')))
    textarea_post.send_keys(post_content_txt)

    button_post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
    button_post.click()

    time.sleep(3)


def run_chrome(opt, user, command):
    driver = webdriver.Chrome(options=opt)
    driver.get("https://twitter.com")

    driver.implicitly_wait(1)
    wait = WebDriverWait(driver, 10)

    if not is_element_present(driver, 'div[data-testid="SideNav_AccountSwitcher_Button"]'):
        do_login(wait, user)

    if command == "post":
        post_content(wait)

    if command == "change_dp":
        print("change_dp")

    if command == "follow":
        follow_user(driver, wait)

    if command == "post_image":
        print("post_image")
        post_image(driver, wait)


def get_user_data_dir():
    config = ConfigParser()
    config.read('config.ini')

    return config.get('section', 'user_data_dir')


def execute(command):
    with open('input/username.csv', newline='') as csvfile:
        user_data_dir = get_user_data_dir()

        csvreader = csv.reader(csvfile, delimiter='|', quotechar='"')
        next(csvreader)

        csv_row_counter = 0
        options_list = []

        for row in csvreader:
            user = TwitterUser.User(row[0], row[1], row[2], row[3], row[4])

            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={user_data_dir}Profile{csv_row_counter + 1}")
            options_list.append(options)

            run_chrome(options, user, command)

            csv_row_counter = csv_row_counter + 1


if __name__ == '__main__':
    while True:
        cmd = input("Enter command: ")
        execute(cmd)
