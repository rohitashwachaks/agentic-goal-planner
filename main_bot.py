import asyncio
import signal
from integrations.telegram_bot_v2 import run_bot  # assuming your telegram bot runs via `app.run_polling()`


async def keep_running():
    print("🧠 Agentic Goal Planner is running... (Press Ctrl+C to stop)")
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def shutdown():
        print("\n🛑 Shutting down gracefully...")
        stop_event.set()

    # Handle SIGINT (Ctrl+C) and SIGTERM
    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    await stop_event.wait()


if __name__ == "__main__":
    try:
        run_bot()  # Telegram bot runs its own async loop
        asyncio.run(keep_running())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
