#! /usr/bin/python3

import os
import json
import time
import pickle
import random
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import DesiredCapabilities

CHROME_EXE = "/usr/local/bin/chromedriver"
CHROME_BINARY = "/usr/bin/brave-browser"
BASE_URL = "/https://noise.cash/"
WALLET_URL = "https://noise.cash/settings/wallet"
EXPLORE_URL = "https://noise.cash/explore"
TEMP_MAIL_URL = "https://generator.email"
DEFAULT_PASS = "hadron*5000"


class NoiseCash:
    def __init__(self, browser, headless=True):

        self.browser = browser
        self.headless = headless

        if self.browser.lower() == "chrome":
            self.opts = self.get_chrome_options(self.headless)
            self.driver = webdriver.Chrome(options=self.opts)
        elif self.browser.lower() == "firefox":
            self.opts = self.get_firefox_options(self.headless)
            driver = webdriver.Chrome(
                options=self.opts,
                executable_path=CHROME_EXE,
                desired_capabilities=capabilities,
            )
        else:
            print("Given browser not supported!")
            exit(-1)

    def get_chrome_options(self, headless):

        opts = webdriver.ChromeOptions()

        opts.add_argument("log-level=3")
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--ignore-certificate-errors")
        opts.add_argument("disable-infobars")

        opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        opts.binary_location = CHROME_BINARY
        return opts

    def get_firefox_options(self, headless):

        opts = webdriver.firefox.options.Options()
        if headless:
            opts.add_argument("--headless")
        return opts

    def close_driver(self):
        self.driver.close()

    def change_proxy(self):
        new_proxy = random.choice(self.PROXIES)

        driver = self.proxy_driver()
        print("--- Switched proxy to: %s" % new_proxy)
        time.sleep(1)

    def generate_user(self, total_user_count):
        user_count = 0
        approved_mails = []
        approved_names = []

        while user_count < total_user_count:
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

                mail = name + "@" + domain
                if mail not in approved_mails:
                    approved_mails.append(mail)

                name = "".join([i for i in name if not i.isdigit()])
                name = re.sub("[^A-Za-z0-9]+", "", name)

                if name not in approved_names:
                    approved_names.append(names)

                print("--- User name %s\temail %s" % (name, email))
                print("--- Starting noise")
                self.driver.execute_script('window.open("%s", "_blank");')

                time.sleep(3)
                noise_handle = self.driver.window_handles[1]
                self.driver.switch_to.window(noise_handle)
                self.driver.get(BASE_URL + "register")

            except:
                pass


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
