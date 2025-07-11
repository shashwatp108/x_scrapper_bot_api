# 🐦 X Scraper Bot API

This is a FastAPI-based bot that scrapes tweets from a public Twitter account using Selenium and exports them to a CSV file. It logs into Twitter using your own credentials (stored securely in a `.env` file).

---

## 🚀 Features

- Scrapes tweets, likes, and tweet URLs
- Auto-login with credentials
- Headless browser automation using Firefox + Selenium
- CSV export for scraped data
- Exposed as a REST API (`/scrape?username=elonmusk`)

---

## 🛠 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/shashwatp108/x_scrapper_bot_api.git
cd x_scrapper_bot_api

2. Create Virtual Environment

python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate    # On Windows

3. Install Dependencies

pip install -r requirements.txt

4. Create a .env File

TWITTER_USERNMAE=youremail@example.com
TWITTER_PASSWORD=yourpassword


5. Run the api server

uvicorn main:app --reload


API usage:

GET http://127.0.0.1:8000/scrape?username=elonmusk


