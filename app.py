from selenium import webdriver
import time
import os
import random
import numpy as np
import json

opts = webdriver.ChromeOptions()
# opts.add_argument("--proxy-server=%s" % proxy)
opts.add_argument("--headless")
opts.add_argument("window-size=1920,1080")
opts.add_argument("start-maximized")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")
opts.binary_location = "/app/.apt/usr/bin/google-chrome-stable"

driver = webdriver.Chrome(chrome_options=opts)
bch_wallet = "bitcoincash:qrgdukh0as64t5cjl37jq8cpm3hca4605q8jzk2xaj"
stored_cookies = ["noisecash_session", "XSRF-TOKEN", "session_entropy"]


def login(mail):
    driver.get("https://noise.cash/")

    try:
        login_page = driver.find_element_by_xpath(
            "/html/body/div/div/nav/div/div/div[2]/div/a[1]"
        ).click()

    except Exception:
        driver.get("https://noise.cash/login")

    if driver.current_url != "https://noise.cash/login":
        for cookie in stored_cookies:
            driver.delete_cookie(cookie)
        driver.get("https://noise.cash/login")

    try:
        email_field = driver.find_element_by_xpath('//*[@id="email"]').send_keys(mail)
        password_field = driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            "hadron*5000"
        )

        login_btn = driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/form/div[4]/button"
        ).click()
        print("trying to login")

    except Exception:
        print("could not login")
        pass

    time.sleep(10)


def logout():

    if driver.current_url != "https://noise.cash/explore":
        driver.get("https://noise.cash/explore")

    user = driver.find_element_by_xpath(
        "/html/body/div/div/nav/div/div/div[3]/div[2]/div/div[1]/button"
    ).click()
    time.sleep(1)
    logout = driver.find_element_by_xpath(
        "/html/body/div/div/nav/div/div/div[3]/div[2]/div[2]/div[2]/div/div/form/a"
    ).click()
    print("logging out")


def issue_handler():

    try:
        tip_modal = driver.find_element_by_xpath("/html/body/div[2]/div")
        driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/button[1]").click()
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
        txt_area = driver.find_element_by_xpath(
            "/html/body/div/div/main/div/div/div[1]/div/div/textarea"
        )

        txt_area.click()
        time.sleep(1)

        txt_area.send_keys(random_quote)
        print("\n" + random_quote)

        post_btn = driver.find_element_by_xpath(
            "/html/body/div/div/main/div/div/div[1]/div/div/div/div[3]/button"
        ).click()
        # time.sleep(60)

    except Exception as e:
        print(e)


def change_wallet():

    if driver.current_url != "https://noise.cash/settings/wallet":
        driver.get("https://noise.cash/settings/wallet")

    curr_addr = driver.find_element_by_xpath('//*[@id="cashaddr"]')
    curr_addr_val = curr_addr.get_attribute("value")
    print(curr_addr_val)

    try:
        if curr_addr_val != bch_wallet:
            curr_addr.send_keys(Key.CONTROL + "a")
            curr.addr.send_keys(Key.DELETE)

            curr_addr.send_keys(bch_wallet)
            driver.find_element_by_xpath(
                "/html/body/div/div/main/div/div/div[2]/div[2]/div/div[2]/button"
            ).click()
            print("changed wallet address")

    except:
        pass


if __name__ == "__main__":

    user_count = 1
    with open("users.txt", "r") as f:
        users = f.readlines()
        f.close()

    while True:
        for user in users:
            try:
                user = user.split("\n")[0].split(",")
                print(f"User: [{user_count}] {user[0]}")

                login(user[1])
                time.sleep(5)

                issue_handler()
                post()

                change_wallet()

                logout()
                # driver.close()
                time.sleep(1)
                user_count += 1

            except Exception as e:
                print(e)
                pass