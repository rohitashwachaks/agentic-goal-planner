import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat ID: {update.effective_chat.id}")


async def hello_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello, world")


load_dotenv()
app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello_world))
app.run_polling()
