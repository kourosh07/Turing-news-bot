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
