import datetime

from crewai.crews import CrewOutput
from sympy.physics.units import frequency

from agents.planner_agent import GoalPlanner, plan_tasks
from agents.task_feedback_agent import TaskFeedbackAgent
from integrations.calendar import CalendarService
from integrations.telegram_bot import TelegramNotifier
from storage.task_db import task_db


class GoalExecutionWorkflow:
    def __init__(self):
        self.db = task_db
        self.planner = GoalPlanner()
        self.calendar = CalendarService()
        self.notifier = TelegramNotifier.get_instance()

    def run(self, user_goal: str):
        print(f"\n🧠 Planning for goal: {user_goal}\n")
        tasks_output = self.planner.plan(user_goal)

        print(f"📋 Tasks:\n{tasks_output}")

        task_list = plan_tasks(tasks_output)
        task_str = "\n\n".join([f"- **{task.action}**: {task.contribution} (scheduled: {task.scheduled_date})" for task in task_list])
        self.notifier.send_message(f"🧠 Goal breakdown for: {user_goal}\n\n{task_str}")

        now = datetime.datetime.now(datetime.UTC)

        for idx, task in enumerate(task_list):
            task_time_str = max(task.scheduled_date, now.date().strftime("%Y-%m-%d"))
            task_time = datetime.datetime.fromisoformat(task_time_str)
            start_time = task_time.replace(hour=10, minute=0).isoformat()

            end_time = start_time
            if task.end_date:
                end_time = datetime.datetime.fromisoformat(task.end_date).replace(hour=10, minute=0).isoformat()
                if end_time < start_time:
                    end_time = start_time

            freq = task.frequency

            for event_date in [start_time, end_time, freq]:
                if event_date < now.isoformat():
                    # Skip scheduling for past events
                    continue
                event_link = self.calendar.create_event(
                    summary=task.action,
                    start_time=start_time,
                    duration_minutes=task.duration_minutes,
                    description=f"Task from goal: {user_goal}\n Contribution: {task.contribution}"
                )
                self.notifier.send_message(f"📅 Scheduled: {task} on {start_time[:10]}\n{event_link}")
                # self.db.add_task(description=task, scheduled_date=start_time[:10])

    def run_daily_checkin(self, task_today: str):
        llm = self.planner.llm.generate
        feedback_agent = TaskFeedbackAgent(llm)

        print(f"\nDid you complete this task today? 👉 {task_today}")
        response = input("Type yes or no: ").strip().lower()
        was_done = response in ['yes', 'y']

        self.db.update_status(task_today, "done" if was_done else "missed")
        feedback = feedback_agent.review_task(task_today, was_done)
        print(f"\n🤖 Agent says:\n{feedback}")
        self.notifier.send_message(feedback)

        if not was_done:
            # Reschedule logic: push to next day at same time
            tomorrow = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
            start_time = tomorrow.replace(hour=10, minute=0).isoformat()
            link = self.calendar.create_event(
                summary=task_today,
                start_time=start_time,
                duration_minutes=60,
                description="Rescheduled task"
            )
            self.notifier.send_message(f"🔁 Task rescheduled to tomorrow\n{link}")

    def run_daily_checkin_all(self):
        today = datetime.datetime.now(datetime.UTC).date().isoformat()
        tasks_today = self.db.get_pending_tasks(today)

        if not tasks_today:
            self.notifier.send_message("✅ No pending tasks for today. You legend.")
            return

        self.notifier.send_message(f"🧾 Daily Check-in: {len(tasks_today)} tasks")

        llm = self.planner.llm.generate
        feedback_agent = TaskFeedbackAgent(llm)

        for task in tasks_today:
            print(f"\n📌 Task: {task}")
            self.notifier.send_message(f"📌 Task: {task}\nDid you complete it? (yes/no)")
            response = input(f"Did you complete this task? 👉 {task} (yes/no): ").strip().lower()
            was_done = response in ['yes', 'y']

            feedback = feedback_agent.review_task(task, was_done)
            self.notifier.send_message(f"🤖 {feedback}")
            self.db.update_status(task, "done" if was_done else "missed")

            if not was_done:
                # Reschedule to tomorrow
                tomorrow = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
                new_time = tomorrow.replace(hour=10, minute=0).isoformat()
                self.calendar.create_event(
                    summary=task,
                    start_time=new_time,
                    duration_minutes=60,
                    description="Rescheduled task"
                )
                self.db.update_rescheduled_date(task, tomorrow.date().isoformat())
                self.notifier.send_message(f"🔁 Rescheduled '{task}' to {tomorrow.date().isoformat()}")

    def send_weekly_summary(self):
        rows = self.db.get_weekly_summary()
        if not rows:
            self.notifier.send_message("No tasks found for this week.")
            return

        summary_lines = ["📊 Weekly Task Summary:\n"]
        for row in rows:
            date, desc, status, resched = row
            resched_info = f" → Rescheduled to {resched}" if resched else ""
            summary_lines.append(f"- [{status.upper()}] {desc} ({date}){resched_info}")

        summary = "\n".join(summary_lines)
        self.notifier.send_message(summary)
