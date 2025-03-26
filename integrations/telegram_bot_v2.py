import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from workflows.simple_plan_and_schedule import GoalExecutionWorkflow

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

workflow = GoalExecutionWorkflow()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        👋 Hey! I'm your Agentic Goal Planner.
        Use ```/goal <<YOUR GOAL HERE>``` to set a goal
        Use ```/checkin``` to do a daily task check-in, 
        or ```/summary``` to get your weekly progress!
        """)


# ✅ NEW: Handle /goal <text>
async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide your goal.\nExample: `/goal I want to run a half marathon in 3 months`", parse_mode="Markdown")
        return

    goal_text = " ".join(context.args)
    await update.message.reply_text(f"🧠 Planning goal: _{goal_text}_", parse_mode="Markdown")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, workflow.run, goal_text)

    await update.message.reply_text("✅ Goal planned and scheduled! Check your calendar 📅 and stay on track 💪")


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
    app.add_handler(CommandHandler("goal", goal))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("summary", summary))

    print("🤖 Telegram bot running...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())
