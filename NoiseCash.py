#! /usr/bin/python3

# Necessary Imports
import re
import os
import json
import time
import pickle
import random
import numpy as np

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import DesiredCapabilities

# Declare some variables
CHROME_BINARY = "/app/.apt/usr/bin/google-chrome-stable"
BASE_URL = "/https://noise.cash/"
WALLET_URL = "https://noise.cash/settings/wallet"
EXPLORE_URL = "https://noise.cash/explore"
TEMP_MAIL_URL = "https://generator.email"
DEFAULT_PASS = "hadron*5000"


class NoiseCash:
    def __init__(self, browser, headless=True, debug=True, total_users=100):

        self.browser = browser
        self.headless = headless
        self.debug = debug
        self.total_users = total_users

        if self.browser.lower() == "chrome":
            self.opts = self.get_chrome_options(self.headless)
            self.driver = webdriver.Chrome(options=self.opts)
        elif self.browser.lower() == "firefox":
            self.opts = self.get_firefox_options(self.headless)
            driver = webdriver.Firefox(options=self.opts)
        else:
            print("Given browser not supported!")
            exit(-1)

    def get_chrome_options(self, headless):

        # Returns chrome options
        opts = webdriver.ChromeOptions()

        opts.add_argument("log-level=3")
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("window-size=1920,1080")
        opts.add_argument("start-maximized")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        opts.binary_location = CHROME_BINARY

        return opts

    def get_firefox_options(self, headless):

        # Returns firefox options
        opts = webdriver.firefox.options.Options()
        if headless:
            opts.add_argument("--headless")
        return opts

    def close_driver(self):

        # Close the current browser instance
        self.driver.close()

    def bch_wallet(self):

        # Select a random bch wallet address from the list
        # and return it
        with open("wallets.txt" "r") as f:
            wallets = [x.split("\n")[0] for x in f.readlines()]
        wallet = random.choice(wallets)

        return "bitcoincash:" + str(wallet)

    def generate_user(self):

        user_count = 0
        approved_mails = []
        approved_names = []

        # Some flags we need
        code_generated = False
        code = None

        # Generate number of dummy accounts as specified by the user
        while user_count < self.total_users:
            try:
                print("--- Starting temp mail")
                self.driver.get(TEMP_MAIL_URL)

                mail_handle = self.current_window_handle
                domain_radio = self.driver.find_element_by_xpath(
                    "/html/body/div[3]/div/div/div[2]/div[2]/div[1]/label"
                ).click()

                name = str(
                    self.driver.find_element_by_xpath(
                        '//*[@id="userName"]'
                    ).get_attribute("value")
                )
                domain = str(
                    self.driver.find_element_by_xpath(
                        '//*[@id="domainName2"]'
                    ).get_attribute("value")
                )

                # Stitch the name and domain provided by tempmail
                # to create a valid username and email by stripping
                # all the unnecessary stuff
                mail = name + "@" + domain
                if mail not in approved_mails:
                    approved_mails.append(mail)

                name = "".join([i for i in name if not i.isdigit()])
                name = re.sub("[^A-Za-z0-9]+", "", name)

                # If a dummy account with that name already exist
                # dont mind including it to the users list
                if name not in approved_names:
                    approved_names.append(names)

                print("--- User name %s\temail %s" % (name, email))
                print("--- Starting noise")
                self.driver.execute_script('window.open("%s", "_blank");')

                time.sleep(3)
                # Switch to noise cash window and visit the registration panel
                noise_handle = self.driver.window_handles[1]
                self.driver.switch_to.window(noise_handle)
                self.driver.get(BASE_URL + "register")

                try:
                    self.driver.find_element_by_xpath('//*[@id="name"]').send_keys(name)
                    self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(
                        mail
                    )
                    self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
                        DEFAULT_PASS
                    )
                    self.driver.find_element_by_xpath(
                        '//*[@id="password_confirmation"]'
                    ).send_keys(DEFAULT_PASS)
                    self.driver.find_element_by_xpath(
                        "/html/body/div/div/div[2]/form/div[5]/button"
                    ).click()

                except Exception as e:
                    print("--- Error filling the fields.")
                    self.close_driver()

                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div[2]/form/div[3]/button"
                ).click()

                if self.driver.current_window_handle != mail_handle:
                    self.driver.switch_to.window(mail_handle)

                # Wait for the code to be recieved
                while not code_generated:
                    try:
                        if code is not None:
                            code = None

                        code = self.driver.find_element_by_xpath(
                            "/html/body/div[4]/div/div/div/div[2]/div[1]/div[2]"
                        ).text.split()[3]
                        print("--- Code recieved succesfully.")
                        code_generated = True

                    except:
                        time.sleep(5)
                        self.driver.refresh()

                if self.driver.current_window_handle != noise_handle:
                    self.driver.switch_to.window(noise_handle)
                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div/div[2]/form/div[1]/input"
                ).send_keys(code)
                print("--- Sending recieved code %s" % code)

                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div/div[2]/form/div[2]/button[1]"
                ).click()

                # Agreeing to their terms
                time.sleep(15)
                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div[2]/div/div[3]/button"
                ).click()
                time.sleep(15)
                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div[2]/div/div/form/label[1]/input"
                ).click()
                self.driver.find_element_by_xpath(
                    "/html/body/div/div/div[2]/div/div/form/div/button[2]"
                ).click()

                time.sleep(3)
                # Randomly change the wallet adresses from the ones available
                self.driver.get(WALLET_URL)
                self.driver.find_element_by_xpath('//*[@id="cashaddr"]').send_keys(
                    self.bch_wallet()
                )
                self.driver.find_element_by_xpath(
                    "/html/body/div/div/main/div/div/div[2]/div[2]/div/div[2]/button"
                ).click()
                print("--- Changed wallet address.")

                with open("users.txt", "a") as f:
                    print("--- Writing the mail to users.txt")
                    f.write("%s,%s\n" % (name, mail))

                print("--- Quitting instance.")
                self.close_driver()

            except Exception as e:
                self.close_driver()


if __name__ == "__main__":

    Bot = NoiseCash()

    running = True
    loop_count = 0

    while running:
        try:

            Bot.generate_user(2)
            Bot.close_driver()

        except Exception as e:
            print(e)
