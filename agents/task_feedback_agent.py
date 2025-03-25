# agents/task_feedback_agent.py

from crewai import Agent, Task, Crew

class TaskFeedbackAgent:
    def __init__(self, llm_func):
        self.agent = Agent(
            role="Task Tracker",
            goal="Track task completion and reschedule missed ones.",
            backstory="An assistant who checks if tasks are done and reschedules if needed.",
            allow_delegation=False,
            verbose=True,
            llm=llm_func
        )

    def review_task(self, task_description, was_done: bool):
        prompt = f"""
User had the following task scheduled today:
"{task_description}"

They {'completed' if was_done else 'missed'} the task.

If they completed it, acknowledge and give a small motivational push.
If they missed it, reschedule it for another day and suggest a suitable time.

Respond in 2-3 lines.
"""
        task = Task(description=prompt, agent=self.agent)
        crew = Crew(agents=[self.agent], tasks=[task], verbose=True)
        result = crew.run()
        return result
