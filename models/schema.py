from dataclasses import dataclass, field
from datetime import datetime, UTC
from dataclasses_json import dataclass_json
from huggingface_hub.constants import default_home
from pydantic import BaseModel
from typing import Optional


class Goal(BaseModel):
    description: str
    priority: Optional[str] = "medium"
    target_date: Optional[str] = None  # e.g., "2025-06-01"


class PlannedTask(BaseModel):
    action: str  # Action to be taken
    contribution: str  # Contribution to the goal
    scheduled_date: str = datetime.now(UTC).strftime("%Y-%m-%d")  # "YYYY-MM-DD"
    duration_minutes: int = 60
    frequency: str = "daily"  # e.g., "daily", "weekly"
    end_date: Optional[str] = None  # "YYYY-MM-DD" or None
    status: Optional[str] = None  # e.g., "pending", "done", "missed"
    rescheduled_to: Optional[str] = None


class TaskFeedback(BaseModel):
    description: str
    was_done: bool
    original_date: str
    rescheduled_date: Optional[str] = None
