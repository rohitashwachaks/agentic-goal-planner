# integrations/telegram_bot.py

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from workflows.simple_plan_and_schedule import GoalExecutionWorkflow

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

workflow = GoalExecutionWorkflow(model_name="mistral")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey! I'm your Agentic Goal Planner.\nUse /checkin to do a daily task check-in, or /summary to get your weekly progress!")


async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕵️ Running your daily check-in...")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, workflow.run_daily_checkin_all)
    await update.message.reply_text("✅ Check-in complete!")


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Generating your weekly summary...")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, workflow.send_weekly_summary)
    await update.message.reply_text("✅ Summary sent!")


def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("summary", summary))

    print("🤖 Telegram bot running...")
    app.run_polling()
