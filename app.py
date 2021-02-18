from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import time
import os
import random
import numpy as np
import json


def get_opts():
    opts = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}

    opts.add_argument("--headless")
    opts.add_argument("--disable-infobars")
    opts.add_argument("window-size=1920,1080")
    opts.add_argument("start-maximized")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--log-level-3")
    opts.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
    return opts


def bch_wallet():

    with open("wallets.txt", "r") as f:
        wallets = [x.split("\n")[0] for x in f.readlines()]

    wallet = random.choice(wallets)
    return str(wallet)


def login(mail):

    driver.delete_all_cookies()
    driver.refresh()
    driver.get("https://noise.cash/login")

    email_field = wait.until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="email"]')),
        message="could not locate email field",
    )
    email_field.send_keys(mail)
    pswd_field = wait.until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="password"]')),
        message="could not locate password field",
    )
    pswd_field.send_keys("hadron*5000")

    login_btn = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div[2]/form/div[4]/button")
        ),
        message="could not find login btn",
    )
    login_btn.click()
    print("trying to login")


def logout():

    if driver.current_url != "https://noise.cash/explore":
        driver.get("https://noise.cash/explore")

    user = wait.until(
        ec.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/nav/div/div/div[3]/div[2]/div/div[1]/button")
        ),
        message="could not find avatar",
    )
    user.click()
    logout = wait.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/nav/div/div/div[3]/div[2]/div[2]/div[2]/div/div/form/a",
            )
        ),
        message="could not find logout btn",
    )
    logout.click()
    print("logging out")


def issue_handler():

    try:
        tip_modal = wait.until(
            ec.presence_of_element_located((By.XPATH, "/html/body/div[2]/div")),
            message="no modal",
        )
        wait.until(
            ec.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[3]/button[1]")
            )
        ).click()
        print("closed_modal")
    except Exception as e:
        pass


def get_random_quote():

    with open("jokes.json", "r") as f:
        jokes = json.load(f)
        jokes = [i["body"] for i in jokes]

    with open("quotes.txt", "r") as f:
        quotes = f.read().split("\n.\n")

    with open("jokes.txt", "r") as f:
        clean_jokes = f.read().split("\n.\n")

    random_text = np.random.choice(
        [random.choice(jokes), random.choice(quotes), random.choice(clean_jokes)],
        p=[0.4, 0.3, 0.3],
    )
    return random_text


def post():

    try:
        if driver.current_url != "https://noise.cash/explore":
            driver.get("https://noise.cash/explore")

        random_quote = get_random_quote()
        txt_area = wait.until(
            ec.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/main/div/div/div[1]/div/div/textarea")
            ),
            message="could not find textarea",
        )
        txt_area.click()
        txt_area.send_keys(random_quote)
        print("\n" + random_quote)

        try:
            wait.until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div/main/div/div/div[1]/div/div/div[1]/div[2]/button",
                    )
                )
            ).click()
        except Exception as e:
            wait.until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div/main/div/div/div[1]/div/div/div[1]/div[3]/button",
                    )
                )
            ).click()

    except Exception as e:
        print("could not find button")


def change_wallet():

    if driver.current_url != "https://noise.cash/settings/wallet":
        driver.get("https://noise.cash/settings/wallet")

    curr_addr = wait.until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="cashaddr"]'))
    )
    curr_addr_val = curr_addr.get_attribute("value")
    print(curr_addr_val)

    curr_addr.send_keys(Keys.CONTROL + "a")
    curr_addr.send_keys(Keys.DELETE)

    curr_addr.send_keys(bch_wallet())
    wait.until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div/div/main/div/div/div[2]/div[2]/div/div[2]/button",
            )
        ),
        message="could not find save button",
    ).click()
    time.sleep(3)
    print("changed wallet address")


def random_tip():

    if driver.current_url != "https://noise.cash/explore":
        driver.get("https://noise.cash/explore")

    try:
        wait.until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div/div[1]",
                )
            )
        ).click()
        wait.until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/button",
                )
            )
        ).click()

        try:
            for i in range(0, 100):
                driver.find_element_by_xpath(
                    "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[5]/input"
                ).send_keys(Keys.ARROW_RIGHT)
        except:
            pass

        wait.until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]",
                )
            )
        ).click()
        try:
            wait.unti(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[6]/div[2]/div/button",
                    )
                )
            ).click()
        except:
            wait.until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div/main/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[5]/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/button",
                    )
                )
            ).click()

    except Exception as e:
        pass


if __name__ == "__main__":

    user_count = 1
    with open("users.txt", "r") as f:
        users = f.readlines()
        f.close()

    driver = webdriver.Chrome(chrome_options=get_opts())
    wait = WebDriverWait(driver,10)
    while True:
        for user in users:
            try:
                user = user.split("\n")[0].split(",")
                print(f"User: [{user_count}] {user[0]}")
                login(user[1])
                time.sleep(5)
                issue_handler()
                post()
                random_tip()
                change_wallet()
                logout()
                user_count += 1
                # driver.close()
            except Exception as e:
                print(e)
                pass
                # driver.close()

    driver.close()
