# agents/planner_agent.py
import os
from datetime import datetime, timedelta, UTC
import re

from crewai import Agent, Task, Crew
from crewai.crews import CrewOutput
from litellm import completion

from llm.llm_wrapper import LocalLLM
from models.schema import PlannedTask


def _parse_tasks_to_models(tasks_output: str) -> list[PlannedTask]:
    lines = tasks_output.strip().split('\n')
    today = datetime.now(UTC).date()
    tasks = []
    for idx, line in enumerate(lines):
        match = re.match(r"\d+\.\s+(.*)", line.strip())
        if match:
            desc = match.group(1)
            date = (today + timedelta(days=idx)).isoformat()
            task = PlannedTask(description=desc, scheduled_date=date)
            tasks.append(task)
    return tasks


class GoalPlanner:

    def __init__(self, model_name="mistral"):
        self.llm = LocalLLM(model_name=model_name)
        self.agent = Agent(
            role="Goal Planner",
            goal="Break down user goals into tangible, scheduled tasks. follow the SMART principle.",
            backstory="An expert productivity coach helping users achieve their goals effectively.",
            verbose=True,
            allow_delegation=False,
            tools=[],  # We’ll add calendar tool later
            llm=completion(model=os.getenv("LITELLM_MODEL_NAME", 'ollama/mistral'))  # Pass the Ollama-backed function
        )

    def plan(self, user_goal: str) -> CrewOutput:
        prompt = f"""
        You are a productivity assistant. Your task is to break down the following user goal into a list of SMART subtasks (Specific, Measurable, Achievable, Relevant, Time-bound). Spread them over the next few weeks, and include the frequency if needed.
        
        User goal: "{user_goal}"
        
        Provide the output as a numbered list with one task per line.
        """
        task = Task(
            description=prompt,
            agent=self.agent,
            expected_output="numbered list of tasks"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        result: CrewOutput = crew.kickoff()
        return result
