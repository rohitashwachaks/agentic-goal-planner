# agentic-goal-planner
Leverage Agentic AI to build a personal assistant and goal planner

           +-------------------+          +------------------------+
           |   User Inputs     |<-------->|   Interaction Layer    |
           |  (Goals, Priorities)|       | (Chatbot: Web/Phone UI) |
           +---------+---------+          +-----------+------------+
                     |                                |
                     v                                |
           +---------+---------+                      |
           |  Goal Decomposition |                    |
           |  & Task Generator   |<-------------------+
           +---------+---------+
                     |
                     v
         +-----------+------------+
         | Context Awareness Agent|
         | (Calendar, Tasks, Habits|
         |  Profile & Preferences)|
         +-----------+------------+
                     |
                     v
         +-----------+------------+
         |   Planning & Scheduler |
         | (Optimizes tasks based |
         |  on energy, habits, etc)|
         +-----------+------------+
                     |
                     v
         +-----------+------------+
         | Progress & Feedback    |
         | Evaluation Agent       |
         | (Weekly review,       |
         | behavioral adjustments)|
         +-----------+------------+
                     |
                     v
         +-----------+------------+
         |    Execution Engine    |
         | (Calendar & Task Sync, |
         |  Nudges, Reminders)    |
         +------------------------+

```
agentic_goal_planner/
├── agents/
│   └── planner_agent.py       # Uses CrewAI + Ollama/HF model
├── llm/
│   └── llm_wrapper.py         # Local model wrapper (Ollama/HF)
├── integrations/
│   ├── calendar.py            # Google Calendar integration
│   └── telegram_bot.py        # Telegram bot for nudges
├── workflows/
│   └── simple_plan_and_schedule.py  # Orchestrates everything
├── main.py                    # Entry point
├── .env                       # Secrets
├── requirements.txt
```
