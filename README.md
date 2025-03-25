# 🧠 Agentic AI Goal Planner


[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%E2%9C%A8-red?logo=streamlit)](https://streamlit.io/)
[![Google Calendar API](https://img.shields.io/badge/Google%20Calendar-API-blue?logo=googlecalendar)](https://developers.google.com/calendar)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](#)

A local-first, agentic productivity system powered by LLMs — break down your goals, schedule them automatically, track progress, and adapt your plan in real time. Fully integrated with Google Calendar, Telegram, and a Streamlit dashboard. Built with Ollama, CrewAI, and love.


## 📌 Overview

The **Agentic AI Goal Planner** is your intelligent life operating system. It helps you manage your goals across multiple life areas (career, fitness, learning, etc.), turns them into tangible actions using local LLMs, schedules them, tracks your progress, and keeps you on track with reminders and adaptive planning.

- ✅ Natural language goal input
- 🧠 LLM-powered SMART task planning
- 📅 Google Calendar auto-scheduling
- 🔁 Daily task tracking + rescheduling
- 💬 Telegram bot interface
- 📊 Streamlit dashboard for visual insights
- 🔒 100% local-first and privacy-preserving

---

## 🧠 Architecture Diagram

```
flowchart TD
    A[🧑 User Input: Goal Description] --> B[🤖 Planning Agent (CrewAI)]
    B --> C[✅ Task Breakdown (Pydantic validated)]
    C --> D[📅 Calendar Sync (Google API)]
    C --> E[💽 Task DB (SQLite)]
    E --> F[📲 Telegram Bot]
    F --> G[🤖 Feedback Agent: Reschedule Missed Tasks]
    G --> D
    E --> H[📊 Streamlit Dashboard]
```


⸻

🧰 Tech Stack

Layer	Tech / Tool	Description
💬 LLM Backend	Ollama + LiteLLM	Run local models (e.g., Mistral, LLaMA2)
🧠 Agents & Planning	CrewAI	Modular agent orchestration
📆 Scheduling	Google Calendar API	Schedule SMART tasks
💬 Notifications	python-telegram-bot	Bot-based reminders and interactions
💽 Local Storage	SQLite	Tracks tasks, reschedules, history
🖥 Dashboard	Streamlit	Progress dashboard UI
✅ Data Validation	Pydantic	Structured schema for tasks and goals



⸻

🚀 Getting Started

1. Clone the Repo
	
	git clone https://github.com/your-username/agentic-goal-planner.git
	cd agentic-goal-planner

2. Set Up .env File
	
	Create a .env in the root directory:
	```markdown
	TELEGRAM_BOT_TOKEN=your_bot_token
	TELEGRAM_USER_ID=123456789
	GOOGLE_CALENDAR_ID=primary
	LITELLM_MODEL_NAME=ollama/mistral
	LITELLM_OLLAMA_URL=http://localhost:11434
	```
3. Install Dependencies

	```bash
	pip install -r requirements.txt
	```

4. Get Google Calendar Credentials
	•	Go to https://console.cloud.google.com/
	•	Create a project → Enable Google Calendar API
	•	Set up OAuth 2.0 for a “Desktop App”
	•	Download your credentials.json into the project root
	•	First run will authenticate and store token.json

⸻

⚙️ Usage

Plan a New Goal

python main.py

Choose 1. Plan a new goal, enter something like:

I want to build muscle and eat healthy over the next 90 days.

→ Your AI agent will:
	•	Break it into SMART tasks
	•	Schedule them into Google Calendar
	•	Log them in local DB
	•	Send a Telegram summary

⸻

Run a Daily Check-In

python main.py

Choose 2. Daily task check-in

→ You’ll be prompted for task completion
→ Missed tasks will be automatically rescheduled
→ Telegram will notify you with feedback

⸻

View Weekly Summary

python main.py

Choose 3. Weekly summary

→ Get completion stats, missed tasks, and motivation report in Telegram + dashboard

⸻

🖥 Streamlit Dashboard

Start the dashboard to view tasks and summaries:

streamlit run dashboard/app.py



⸻

🤖 Telegram Bot Commands

Once running, you can talk to your agent from anywhere:

Command	Action
/start	Welcome and help message
/checkin	Run daily task check-in
/summary	Weekly task summary
/plan (coming soon)	Plan a goal via chat



⸻

🧩 Project Structure

agentic-goal-planner/
├── agents/                  # CrewAI-based planning and feedback agents
├── integrations/            # Google Calendar + Telegram integrations
├── workflows/               # End-to-end pipeline orchestration
├── llm/                     # LLM wrapper (Ollama/LiteLLM)
├── storage/                 # SQLite task DB
├── dashboard/               # Streamlit UI
├── models/                  # Pydantic schemas
├── main.py                  # CLI entry point
├── .env                     # Env vars
├── requirements.txt



⸻

✅ What’s Next
	•	Plan goals via Telegram /plan command
	•	Add Notion sync (optional)
	•	Schedule around preferred focus windows
	•	Voice control (Whisper + mobile integration)
	•	Weekly agent to reprioritize stalled goals

⸻

🛡 Privacy First

This system is 100% local-first. Your goals, calendar, and progress are:
	•	Never sent to OpenAI or any cloud unless you choose
	•	Run using local models via Ollama (Mistral, LLaMA2, etc.)
	•	Stored securely in local SQLite DB

⸻

📖 License

MIT License – use, modify, and build your own life OS ⚡

⸻

👋 Acknowledgements

Built with ❤️ using:
	•	CrewAI
	•	Ollama
	•	python-telegram-bot
	•	Streamlit
	•	Pydantic

⸻

✨ Star the Repo if You Like It!

Helping yourself plan your goals with AI?
Give it a ⭐ and share your feedback!

---