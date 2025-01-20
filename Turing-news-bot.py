import json
import os
import pytz
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Replace with your Telegram bot token
TELEGRAM_TOKEN = "your_token"

# Replace with your NewsAPI key
NEWS_API_KEY = "your_token"

# CoinGecko API for Bitcoin price
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# NewsAPI endpoint for programming-related news in Farsi
news_url = "https://newsapi.org/v2/everything"

# Parameters for programming-related news in Farsi
news_params = {
    "apiKey": NEWS_API_KEY,
    "q": "برنامه‌نویسی OR کدنویسی OR توسعه نرم‌افزار",  # Keywords in Farsi
    "language": "fa",  # Farsi news
    "domains": "zoomit.ir,digiato.com,tarfandestan.com,narenji.ir,ictnews.ir,itresan.com,technet.ir",  # Trusted Farsi tech sites
    "sortBy": "publishedAt",  # Sort by latest news
    "pageSize": 10  # Fetch 10 articles
}

# File to store group chat IDs
GROUP_CHAT_IDS_FILE = "group_chat_ids.json"

# Load group chat IDs from file
def load_group_chat_ids():
    if os.path.exists(GROUP_CHAT_IDS_FILE):
        with open(GROUP_CHAT_IDS_FILE, "r") as file:
            return json.load(file)
    return []

# Save group chat IDs to file
def save_group_chat_ids(group_chat_ids):
    with open(GROUP_CHAT_IDS_FILE, "w") as file:
        json.dump(group_chat_ids, file)

# Fetch programming-related news
async def fetch_programming_news():
    try:
        response = requests.get(news_url, params=news_params)
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Fetch Bitcoin price
async def fetch_bitcoin_price():
    try:
        response = requests.get(COINGECKO_API_URL)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

# Send daily news to groups
async def send_daily_news(context: ContextTypes.DEFAULT_TYPE):
    group_chat_ids = load_group_chat_ids()
    print("Daily news job triggered at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Group chat IDs:", group_chat_ids)

    programming_news = await fetch_programming_news()
    bitcoin_price = await fetch_bitcoin_price()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Start the message with a friendly greeting
    message = f"🌞 **صبح بخیر!**\n\n"
    message += f"امروز روز {current_date} هست و من اینجا هستم تا شما را با آخرین اخبار برنامه‌نویسی و فناوری به روز کنم. 😊\n\n"

     # Add Bitcoin price section
    if bitcoin_price:
        message += f"💰 **قیمت بیت‌کوین امروز:** ${bitcoin_price}\n\n"






