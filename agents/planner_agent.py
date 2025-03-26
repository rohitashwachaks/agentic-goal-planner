import ast
import json
from datetime import datetime, timedelta, UTC
import re

from crewai.crews import CrewOutput
from crewai import Agent, Task, Crew

from llm.llm_wrapper import LLMRouter
from models.schema import PlannedTask


def plan_tasks(tasks_output: CrewOutput) -> list[PlannedTask]:
    """
    Format the output from the CrewAI agent into a list of PlannedTask models.

    Args:
        tasks_output (CrewOutput): The output from the CrewAI agent containing the planned tasks.

    Returns:
        list[PlannedTask]: A list of PlannedTask models.
    """
    task_list = []
    if not tasks_output or not tasks_output.raw:
        return task_list

    task_str = tasks_output.raw.strip('```').lstrip('json')
    task_json = json.loads(task_str)
    task_list = [PlannedTask.model_validate(task) for task in task_json]

    # Split the output into lines and parse each line to extract task details
    # for idx, line in enumerate(tasks_output.raw.split('\n')):
    #     line = line.strip()
    #     if not line:
    #         continue
    #
    #     # extract the json object within '''{...}'''
    #     # match = re.match(r'^\s*{.*}$', line)
    #     match = re.match(r'^\s*```.*?```$', line)
    #     if match:
    #         # Remove the ``` and parse the JSON
    #         json_str = line.strip('```')
    #         try:
    #             task_data = json.loads(json_str)
    #             task = PlannedTask(
    #                 action=task_data.get('action'),
    #                 contribution=task_data.get('contribution'),
    #                 scheduled_date=task_data.get('scheduled_date'),
    #                 duration_minutes=task_data.get('duration_minutes', 60),  # Default to 60 minutes if not specified
    #                 end_date=task_data.get('end_date'),  # Default to None if not specified
    #                 frequency=task_data.get('frequency', 1)  # Default to 1 if not specified,
    #             )
    #             task_list.append(task)
    #         except json.JSONDecodeError as e:
    #             print(f"Error parsing JSON: {e}")
    #             continue
    return task_list


class GoalPlanner:
    def __init__(self):
        self.llm = LLMRouter().get_llm()  # unified interface
        self.agent = Agent(
            role="Goal Planner",
            goal="Turn user goals into actionable SMART tasks.",
            backstory="An expert productivity coach helping users achieve their goals effectively.",
            allow_delegation=False,
            verbose=True,
            llm=self.llm  # LiteLLM-compatible function
        )

    def plan(self, user_goal: str) -> CrewOutput:
        prompt = f"""
        You are a productivity assistant. 
        Your task is to break down the following user goal into a list of progressive SMART subtasks (Specific, Measurable, Achievable, Relevant, Time-bound).
        Spread them over the next few weeks, and include the frequency.
        Each task should be clearly defined and actionable.
        
        User goal: "{user_goal}"
        
        Provide the output as a list with one task per line.
        Each task must be a JSON object with the following fields:
        - action: A clear and actionable description of the task.
        - contribution: A brief explanation of how this task contributes to the overall goal.
        - scheduled_date: The date when the task should be completed (YYYY-MM-DD).
        - duration_minutes: The estimated time in minutes to complete the task (default to 60 if not specified).
        - frequency: Indicating how often the task should be repeated (e.g., daily, weekly).
        - end_date: The date when the task should end (optional).
        """
        task = Task(
            description=prompt,
            agent=self.agent,
            expected_output="list of tasks. Each task is a JSON object with fields: action, contribution, scheduled_date, duration_minutes, frequency and end_date.",
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        result: CrewOutput = crew.kickoff()
        return result
