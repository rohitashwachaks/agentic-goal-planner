# storage/task_db.py

import sqlite3
from datetime import datetime

DB_NAME = "task_data.db"

class TaskDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                scheduled_date TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                rescheduled_to TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

    def add_task(self, description: str, scheduled_date: str):
        with self.conn:
            self.conn.execute(
                "INSERT INTO tasks (description, scheduled_date) VALUES (?, ?)",
                (description, scheduled_date)
            )

    def update_status(self, description: str, status: str):
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET status = ? WHERE description = ? AND status = 'pending'",
                (status, description)
            )

    def update_rescheduled_date(self, description: str, new_date: str):
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET rescheduled_to = ? WHERE description = ? AND status = 'missed'",
                (new_date, description)
            )

    def get_pending_tasks(self, date: str):
        with self.conn:
            result = self.conn.execute(
                "SELECT description FROM tasks WHERE scheduled_date = ? AND status = 'pending'",
                (date,)
            )
            return [row[0] for row in result.fetchall()]

    def get_weekly_summary(self):
        with self.conn:
            result = self.conn.execute("""
                SELECT scheduled_date, description, status, rescheduled_to
                FROM tasks
                ORDER BY scheduled_date DESC
                LIMIT 50
            """)
            return result.fetchall()
