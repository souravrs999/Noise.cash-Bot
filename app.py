# Necessary imports
import time
import os
import json
import numpy as np
import random

# Fake user agent
from fake_useragent import UserAgent

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class NoiseCash:
    def __init__(self, user, mail, pswd):

        self.user = user
        self.mail = mail
        self.pswd = pswd
        self.login_url = "https://noise.cash/login"
        self.wallet_url = "https://noise.cash/settings/wallet"
        self.chamber_url = [
            "https://noise.cash/n/url1",
            "https://noise.cash/n/url2",]
        self.driver = webdriver.Chrome(
            executable_path=str(os.environ.get("CHROMEDRIVER_PATH")),
            options=self._getOpts(),
        )
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.wait = WebDriverWait(self.driver, 10)

    def _getOpts(self):

        opts = webdriver.ChromeOptions()

        # Basic chrome flags
        opts.add_argument("--headless")
        opts.add_argument("--incognito")
        opts.add_argument("no-first-run")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--log-level-3")
        opts.add_argument("--disable-webgl")
        opts.add_argument("start-maximized")
        opts.add_argument("--disable-infobars")
        opts.add_argument("window-size=1280,720")
        opts.add_argument("--disable-xss-auditor")
        opts.add_argument("--disable-web-security")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-setuid-sandbox")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("no-default-browser-check")
        opts.add_argument("--ignore-certificate-errors")
        opts.add_argument("--allow-running-insecure-content")
        opts.add_argument(f"--user-agent={UserAgent().random}")
        opts.add_argument("--disable-blink-features")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("enable-experimental-web-platform-features")

        # Experimental features
        prefs = {"profile.managed_default_content_settings.images": 2}
        opts.add_experimental_option("prefs", prefs)
        opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.set_capability("unhandledPromptBehavior", "accept")

        # Chrome binary
        opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        return opts

    # Function to return elem's presence state
    def __getXEP(self, elem):
        return self.wait.until(
            ec.presence_of_element_located((By.XPATH, elem)),
            message=f"--- Could not find {elem}",
        )

    # Fuction to return elements clickable state
    def __getXEC(self, elem):
        return self.wait.until(
            ec.element_to_be_clickable((By.XPATH, elem)),
            message=f"--- Could not find {elem}",
        )

    def Close(self):

        # Close everything down
        self.driver.close()
        self.driver.quit()

    def Wallet(self):

        # Open the wallets file and return a random address
        # from it
        with open("wallets.txt", "r") as f:
            wallets = [x.split("\n")[0] for x in f.readlines()]
        return str(random.choice(wallets))

    def Login(self):

        if self.driver.current_url != self.login_url:
            self.driver.delete_all_cookies()
            self.driver.refresh()
            self.driver.get(self.login_url)

            print(f"--- User {self.user}")
            print("--- Inputting mail and password")
            email_field = self.__getXEP('//*[@id="email"]').send_keys(self.mail)
            pswd_field = self.__getXEP('//*[@id="password"]').send_keys(self.pswd)
            # remember = self.__getXEP('//*[@id="remember_me"]').click()
            print("--- Clicking on Login btn")
            login_btn = self.__getXEC(
                "/html/body/div/div/div[2]/form/div[4]/button"
            ).click()

    def Logout(self):

        try:
            avatar = self.__getXEP(
                "/html/body/div/div/nav/div/div/div[3]/div[2]/div/div[1]/button/div[1]"
            ).click()
            logout = self.__getXEP(
                "/html/body/div/div/nav/div/div/div[3]/div[2]/div[2]/div[2]/div/div/form/a"
            ).click()
            print("--- Logged out")
        except:
            pass

    def _modalHandler(self):

        try:
            modal_close = self.__getXEC(
                "/html/body/div[2]/div/div[3]/button[1]"
            ).click()
            print("--- Closed_modal")
        except:
            pass

    # Get some random joke to post
    def getRandJoke(self):

        jokes = json.load(open("reddit_jokes.json"))
        randomJoke = np.random.choice(jokes)
        return randomJoke["title"] + randomJoke["body"]

    # Get some random quote to post
    def getRandQuote(self):

        quotes = json.load(open("quotes.json"))
        randomQuote = np.random.choice(quotes)
        return randomQuote["Quote"] + randomQuote["Author"]

    def likeShit(self):
        print("--- Liking stuff")
        for x in range(1, 21):
            likeBtnsXpaths = f'//*[@id="app"]/div/main/div/div/div[4]/div/div[{x}]/div/div[2]/div[2]/div[3]/div[8]/button'
            likeBtn = self.__getXEC(likeBtnsXpaths).click()

    def PostJokes(self):

        if self.driver.current_url not in self.chamber_url:
            self.driver.get(np.random.choice(self.chamber_url))
        self.likeShit()
        try:
            random_joke = self.getRandJoke()
            random_joke = "".join(
                np.random.choice([str.upper, str.lower], p=[0.05, 0.95])(c)
                for c in random_joke
            )
            txt_area = self.__getXEC(
                "/html/body/div/div/main/div/div/div[2]/div/div/textarea"
            ).click()
            txt_area = self.driver.find_element_by_xpath(
                "/html/body/div/div/main/div/div/div[2]/div/div/textarea"
            )
            txt_area.send_keys(random_joke)
            print(f"-- Text {random_joke}")

            try:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[2]/div/div/div[1]/div[3]/button"
                ).click()
                print("--- Posted succesfully")
            except:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[2]/div/div/div[1]/div[2]/button"
                ).click()
                print("--- Posted succesfully")
        except Exception as e:
            print(f"--- Error Could not post")
            pass

    def PostQuotes(self):

        if self.driver.current_url not in self.chamber_url:
            self.driver.get(random.choice(self.chamber_url))
        self.likeShit()
        try:
            random_quote = self.getRandQuote()
            random_quote = "".join(
                np.random.choice([str.upper, str.lower], p=[0.05, 0.95])(c)
                for c in random_quote
            )
            txt_area = self.__getXEC(
                "/html/body/div/div/main/div/div/div[2]/div/div/textarea"
            ).click()
            txt_area = self.driver.find_element_by_xpath(
                "/html/body/div/div/main/div/div/div[2]/div/div/textarea"
            )
            txt_area.send_keys(random_quote)
            print(f"-- Text {random_quote}")

            try:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[2]/div/div/div[1]/div[3]/button"
                ).click()
                print("--- Posted succesfully")
            except:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[2]/div/div/div[1]/div[2]/button"
                ).click()
                print("--- Posted succesfully")
        except Exception as e:
            print(f"--- Error could not post")
            pass

    def changeWallet(self):

        if self.driver.current_url != self.wallet_url:
            self.driver.get(self.wallet_url)

        rec = np.random.choice([True, False], p=[0.3, 0.7])
        curr_addr = self.__getXEP('//*[@id="cashaddr"]')
        curr_addr_val = curr_addr.get_attribute("value")

        if "bitcoincash" not in curr_addr_val:
            curr_addr.send_keys(self.Wallet())
            self.__getXEC(
                "/html/body/div/div/main/div/div/div[2]/div[2]/div/div[2]/button"
            ).click()
            print("--- Changed wallet address")

        elif bool(rec):
            curr_addr = self.__getXEP('//*[@id="cashaddr"]')
            curr_addr.send_keys(Keys.CONTROL + "a")
            curr_addr.send_keys(Keys.DELETE)

            curr_addr.send_keys(self.Wallet())
            min_amount = self.__getXEP('//*[@id="minPayout"]').send_keys(0)
            self.__getXEC(
                "/html/body/div/div/main/div/div/div[2]/div[2]/div/div[2]/button"
            ).click()
            print("--- Changed wallet address")

    def randomTip(self):

        if self.driver.current_url not in self.chamber_url:
            self.driver.get(os.random(self.chamber_url))

        try:
            self.__getXEP(
                "/html/body/div/div/main/div/div/div[3]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div[5]/div/div/div[1]"
            ).click()
            try:
                self.__getXEP(
                    "/html/body/div/div/main/div/div/div[3]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div[5]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button"
                ).click()
            except Exception:
                for i in range(0, 50):
                    driver.find_element_by_xpath(
                        "/html/body/div/div/main/div/div/div[3]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div[5]/div/div[2]/div[2]/div/div/div/div[5]/input"
                    ).send_keys(Keys.ARROW_RIGHT)
            except:
                pass
            self.__getXEP(
                "/html/body/div/div/main/div/div/div[3]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div[5]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]"
            ).click()
            try:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[3]/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div[5]/div/div[2]/div[2]/div/div/div/div[6]/div[2]/div/button"
                ).click()
            except:
                self.__getXEC(
                    "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/button"
                ).click()
        except Exception as e:
            print(f"--- Error: {e}")
            pass


if __name__ == "__main__":

    with open("users.txt", "r") as f:
        users = f.readlines()
    while True:
        for user in users:
            user = user.split("\n")[0].split(",")
            try:
                bot = NoiseCash(user[0], user[1], <your_password>)
                bot.Login()
                topic = random.choice(["joke", "quote"])
                print(f"--- Topic {topic}")
                if topic == "joke":
                    bot.PostJokes()
                elif topic == "quote":
                    bot.PostQuotes()
                # bot.randomTip()
                bot.changeWallet()
                bot.Logout()
                bot.Close()
            except Exception as e:
                print(f"--- Error {e}")
                bot.Close()
