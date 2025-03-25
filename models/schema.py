# models/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Goal(BaseModel):
    description: str
    priority: Optional[str] = "medium"
    target_date: Optional[str] = None  # e.g., "2025-06-01"


class PlannedTask(BaseModel):
    description: str
    scheduled_date: str  # "YYYY-MM-DD"
    duration_minutes: int = 60
    status: str = "pending"
    rescheduled_to: Optional[str] = None


class TaskFeedback(BaseModel):
    description: str
    was_done: bool
    original_date: str
    rescheduled_date: Optional[str] = None
