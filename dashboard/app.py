import os

os.chdir('../')  # Ensure the working directory is set to the project root

import streamlit as st
from storage.task_db import TaskDB
from datetime import datetime, timedelta

from models.schema import PlannedTask

# Showing nicely structured task data
st.json(PlannedTask(
    description="Read 10 pages",
    scheduled_date="2025-03-26"
).dict())

st.set_page_config(page_title="Agentic Goal Tracker", layout="wide")

db = TaskDB()

st.title("🧠 Agentic Goal Tracker")

# Add Task Section
with st.expander("➕ Add a New Task"):
    desc = st.text_input("Task Description")
    date = st.date_input("Schedule Date", value=datetime.today())
    if st.button("Add Task"):
        db.add_task(desc, date.isoformat())
        st.success(f"Added task: {desc}")

# Weekly Summary Section
st.subheader("📊 Weekly Task Summary")

summary = db.get_weekly_summary()
if summary:
    for row in summary:
        scheduled_date, description, status, resched_to = row
        resched_text = f" 🔁 Rescheduled → {resched_to}" if resched_to else ""
        st.markdown(f"- **[{status.upper()}]** `{scheduled_date}` — {description}{resched_text}")
else:
    st.info("No tasks found.")

# Task Completion Rate
st.subheader("✅ Weekly Completion Rate")
if summary:
    done = sum(1 for row in summary if row[2] == "done")
    total = len(summary)
    rate = round((done / total) * 100, 1)
    st.progress(rate / 100)
    st.markdown(f"**{done} / {total}** tasks completed — **{rate}%**")
