# integrations/telegram_bot.py

import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")


class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)

    def send_message(self, message: str):
        if not TELEGRAM_USER_ID:
            raise ValueError("TELEGRAM_USER_ID is not set in .env")
        self.bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)


# Example usage

notifier = TelegramNotifier()
notifier.send_message("Hello! Your workout starts in 30 minutes 💪")

