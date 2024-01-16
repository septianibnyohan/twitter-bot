import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from SessionLogin import SessionLogin


class TwitterLogin:
    @staticmethod
    def get_2fa_code(url):
        resp = requests.get(url)

        soup2 = BeautifulSoup(resp.text, "html.parser")
        result2 = soup2.find("span", class_="codetxt")

        return result2.text

    @staticmethod
    def fill_email(wait, twitter_user):
        input_email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']")))
        input_email.send_keys(twitter_user.email)

        css_next_in_email = ("#layers > div:nth-child(2) > div > div > div > div > div > "
                             "div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r"
                             "-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r"
                             "-1pjcn9w.r-1279nm1 > div > div > "
                             "div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-14lw9ot.r-1wbh5a2 > "
                             "div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div > div > div > "
                             "div:nth-child(6)")

        button_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_next_in_email)))
        button_next.click()

    @staticmethod
    def fill_username(wait, twitter_user):
        input_username = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')))
        input_username.send_keys(twitter_user.username)

        css_next_in_username = 'div[data-testid="ocfEnterTextNextButton"]'

        button_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_next_in_username)))
        button_next.click()

    @staticmethod
    def fill_password(wait, twitter_user):
        input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        input_password.send_keys(twitter_user.password)

        css_next_in_password = 'div[data-testid="LoginForm_Login_Button"]'

        button_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_next_in_password)))
        button_next.click()

    def fill_verification_code(self, wait, twitter_user):
        input_verification = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')))
        code_2fa = self.get_2fa_code(twitter_user.two_fa_url)
        input_verification.send_keys(code_2fa)

        css_next_in_verification = 'div[data-testid="ocfEnterTextNextButton"]'

        button_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_next_in_verification)))
        button_next.click()

    def fill_current_session_login(self, wait, twitter_user):
        try:
            title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modal-header > span > span")))

            if title.text == SessionLogin.EMAIL.value:
                self.fill_email(wait, twitter_user)
            elif title.text == SessionLogin.USERNAME.value:
                self.fill_username(wait, twitter_user)
            elif title.text == SessionLogin.PASSWORD.value:
                self.fill_password(wait, twitter_user)
            elif title.text == SessionLogin.VERIFICATION_CODE.value:
                self.fill_verification_code(wait, twitter_user)
        except Exception as e:
            print(e)
            css_nav_account_switcher = 'div[data-testid="SideNav_AccountSwitcher_Button"]'
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_nav_account_switcher)))
            print('login success')
            print('modal-header not existed')