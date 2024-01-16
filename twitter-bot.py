from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
import time
from selenium.common.exceptions import NoSuchElementException
import csv

# create a list of chromedriver options
options_list = []
for i in range(1):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir=./UserData/Profile{i + 1}")
    options_list.append(options)


def is_element_present(driver, selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
        print("Element " + selector + " exists!")
        return True
    except NoSuchElementException:
        print("Element " + selector + " exists!")
        return False


# define a function that takes an options object and runs a chromedriver instance
def run_chromedriver(opt):
    driver = webdriver.Chrome(options=opt)
    driver.get("https://twitter.com")
    # do the necessary operations
    # task1; task2; task3
    # close instance after completed
    # time.sleep(5)
    # driver.quit()

    # create a WebDriverWait object with a timeout of 10 seconds
    wait = WebDriverWait(driver, 10)

    if not is_element_present(driver, "div[data-testid='UserAvatar-Container-septianibnyohan']"):
        # wait until the element with href="/login" is visible
        button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/login']")))

        # click the button
        button.click()

        input_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']")))
        input_name.send_keys("septianibnyohan@gmail.com")

        button_next = driver.find_element(By.CSS_SELECTOR,
                                          "#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-14lw9ot.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div > div > div > div:nth-child(6)")
        button_next.click()

        # data-testid="ocfEnterTextTextInput"
        input_username = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']")))
        input_username.send_keys("septianibnyohan")

        button_next = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='ocfEnterTextNextButton']")))
        button_next.click()

        input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        input_password.send_keys("Twitter01#")

        # data-testid="LoginForm_Login_Button"
        button_login = driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']")
        button_login.click()

    while True:
        print("Sleep 5")
        time.sleep(5)


# create a list of processes
process_list = []
for options in options_list:
    process = Process(target=run_chromedriver, args=(options,))
    process_list.append(process)

# start the processes
for process in process_list:
    process.start()

# wait for the processes to finish
for process in process_list:
    process.join()
