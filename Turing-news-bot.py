import json
import os
import pytz
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Replace with your Telegram bot token
TELEGRAM_TOKEN = "your_token"
