from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import pandas as pd
import time
import os

app = FastAPI()
load_dotenv()

def run_scraper(target_user):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)

    # Load credentials from .env
    TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

    # --- Optional Logout to ensure clean login ---
    try:
        driver.get("https://twitter.com/home")
        time.sleep(5)
        driver.find_element(By.XPATH, '//div[@aria-label="Account menu"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//a[@data-testid="AccountSwitcher_Logout_Button"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]').click()
        print("✅ Logged out successfully.")
        time.sleep(5)
    except Exception as e:
        print(f"⚠️ Could not log out (probably not logged in): {e}")

    # --- Login Flow ---
    driver.get("https://twitter.com/login")
    time.sleep(5)

    try:
        # Step 1: Enter username
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 2 (sometimes Twitter asks again)
        try:
            confirm_input = driver.find_element(By.NAME, "text")
            confirm_input.send_keys(TWITTER_USERNAME)
            confirm_input.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass

        # Step 3: Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
    except Exception as e:
        print("❌ Couldn't find password input. CAPTCHA or login block.")
        driver.quit()
        return None

    # --- Go to Target User Page ---
    driver.get(f"https://twitter.com/{target_user}")
    time.sleep(7)

    # --- Scrape Tweets ---
    tweets = []
    for _ in range(20):
        cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for card in cards:
            try:
                content = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                stats = card.find_elements(By.XPATH, './/div[@data-testid="like"]//span')
                likes = stats[0].text if stats else "0"
                url = card.find_element(By.XPATH, './/time/..').get_attribute("href")
                tweets.append([content, likes, url])
            except:
                continue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    driver.quit()

    # --- Save to CSV ---
    if not tweets:
        print("❌ No tweets found.")
        return None

    df = pd.DataFrame(tweets, columns=["Content", "Likes", "URL"])
    df.drop_duplicates(subset="URL", inplace=True)
    file_path = f"{target_user}_tweets.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Scraped {len(df)} tweets.")
    return file_path

@app.get("/")
def root():
    return {"message": "Twitter Scraper API is running..."}

@app.get("/scrape")
def scrape_tweets(username: str = Query(..., description="Twitter handle without @")):
    file_path = run_scraper(username)
    if file_path:
        return FileResponse(path=file_path, filename=file_path, media_type='text/csv')
    return {"error": "Failed to scrape tweets. Check logs or credentials."}
