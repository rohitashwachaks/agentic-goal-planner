# integrations/telegram_bot.py

import os
import asyncio
import random
from telegram import Bot
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class TelegramNotifier:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self, token: str, chat_id: str, rate_limit_per_sec: int = 1, max_retries: int = 5):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self._semaphore = asyncio.Semaphore(rate_limit_per_sec)
        self.max_retries = max_retries

    @classmethod
    def get_instance(cls) -> "TelegramNotifier":
        """Singleton method to get the TelegramNotifier instance."""
        if cls._instance is None:
            asyncio.run(cls._get_instance())
        return cls._instance

    @classmethod
    async def _get_instance(cls) -> "TelegramNotifier":
        async with cls._lock:
            if cls._instance is None:
                token = os.getenv("TELEGRAM_BOT_TOKEN")
                chat_id = os.getenv("TELEGRAM_USER_ID")
                if not token or not chat_id:
                    raise ValueError("Telegram token or user ID not set in .env")
                cls._instance = TelegramNotifier(token, chat_id)
        return cls._instance

    def send_message(self, message: str):
        """Send a message to the Telegram chat."""
        asyncio.run(self._send_message(message))

    async def _send_message(self, message: str):
        async with self._semaphore:
            for attempt in range(1, self.max_retries + 1):
                try:
                    await self.bot.send_message(chat_id=self.chat_id, text=message)
                    return  # success
                except Exception as e:
                    wait_time = self._get_backoff(attempt)
                    print(f"⚠️ Attempt {attempt}: Telegram send failed: {e}. Retrying in {wait_time:.2f}s...")
                    await asyncio.sleep(wait_time)
            print(f"❌ Failed to send Telegram message after {self.max_retries} attempts.")

    def _get_backoff(self, attempt: int) -> float:
        # Exponential backoff with jitter: base * 2^attempt + random(0, 0.5)
        base = 0.5
        return base * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
