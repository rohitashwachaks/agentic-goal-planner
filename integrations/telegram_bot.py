# integrations/telegram_bot.py

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()


class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
        self.chat_id = os.getenv("TELEGRAM_USER_ID")

    def send_message(self, message: str):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Already inside an async event loop, create a task
            asyncio.create_task(self._send_async(message))
        else:
            # No event loop running: safe to use asyncio.run()
            asyncio.run(self._send_async(message))

    async def _send_async(self, message: str):
        await self.bot.send_message(chat_id=self.chat_id, text=message)
# # Example usage
#
# notifier = TelegramNotifier()
# notifier.send_message("Hello! Your workout starts in 30 minutes 💪")
