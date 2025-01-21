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

    # Add programming news section
    if programming_news:
        message += "📰 **آخرین اخبار برنامه‌نویسی و فناوری به فارسی:**\n\n"
        for article in programming_news[:10]:  # Show up to 10 articles
            title = article.get('title', 'بدون عنوان')
            description = article.get('description', 'بدون توضیحات')
            url = article.get('url', '#')
            source = article.get('source', {}).get('name', 'منبع نامعلوم')
            message += (
                f"🔹 **{title}**\n"
                f"📝 *{description}*\n"
                f"🌐 *منبع:* {source}\n"
                f"🔗 [مطالعه بیشتر]({url})\n\n"
            )
    else:
        message += "❌ متأسفانه امروز خبری برای برنامه‌نویسی پیدا نکردم. اما نگران نباشید، فردا دوباره تلاش می‌کنم! 😊\n\n"

    # End the message with a warm sign-off
    message += "با آرزوی بهترین‌ها برای شما,\nتیم پژوهشی تورینگ 🚀"

     # Send the message to all groups
    for chat_id in group_chat_ids:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! 👋\n"
        "من یک ربات هستم که هر روز صبح شما را با آخرین اخبار برنامه‌نویسی و قیمت بیت‌کوین به روز می‌کنم. 😊\n\n"
        "برای اضافه کردن این گروه به لیست دریافت اخبار روزانه، از دستور /add_group استفاده کنید.\n"
        "برای دریافت اخبار همین الان، از دستور /news استفاده کنید."
    )

# News command handler
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    programming_news = await fetch_programming_news()
    bitcoin_price = await fetch_bitcoin_price()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Start the message with a friendly greeting
    message = f"🌞 **سلام!**\n\n"
    message += f"امروز روز {current_date} هست و من اینجا هستم تا شما را با آخرین اخبار برنامه‌نویسی و فناوری به روز کنم. 😊\n\n"
    
    # Add Bitcoin price section
    if bitcoin_price:
        message += f"💰 **قیمت بیت‌کوین امروز:** ${bitcoin_price}\n\n"
    
    # Add programming news section
    if programming_news:
        message += "📰 **آخرین اخبار برنامه‌نویسی و فناوری به فارسی:**\n\n"
        for article in programming_news[:10]:  # Show up to 10 articles
            title = article.get('title', 'بدون عنوان')
            description = article.get('description', 'بدون توضیحات')
            url = article.get('url', '#')
            source = article.get('source', {}).get('name', 'منبع نامعلوم')
            message += (
                f"🔹 **{title}**\n"
                f"📝 *{description}*\n"
                f"🌐 *منبع:* {source}\n"
                f"🔗 [مطالعه بیشتر]({url})\n\n"
            )
    else:
        message += "❌ متأسفانه امروز خبری برای برنامه‌نویسی پیدا نکردم. اما نگران نباشید، فردا دوباره تلاش می‌کنم! 😊\n\n"
    
    # End the message with a warm sign-off
    message += "با آرزوی بهترین‌ها برای شما,\nتیم پژوهشی تورینگ 🚀"

    await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)


# Add group command handler
async def add_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    group_chat_ids = load_group_chat_ids()
    if chat_id not in group_chat_ids:
        group_chat_ids.append(chat_id)
        save_group_chat_ids(group_chat_ids)
        await update.message.reply_text(
            "این گروه به لیست دریافت اخبار روزانه اضافه شد! 😊\n\n"
            "از این به بعد، هر روز صبح ساعت ۷ اخبار جدید را برای شما ارسال می‌کنم."
        )
    else:
        await update.message.reply_text(
            "این گروه قبلاً اضافه شده است. 😊\n\n"
            "نگران نباشید، من هر روز صبح اخبار جدید را برای شما ارسال می‌کنم."
        )

# Main function to run the bot
def main() -> None:
    # Define the Tehran time zone
    tehran_tz = pytz.timezone('Asia/Tehran')

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("add_group", add_group))

    application = Application.builder().token(TELEGRAM_TOKEN).build()

