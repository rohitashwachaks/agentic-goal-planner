from crewai import Agent, Task, Crew
from litellm import completion

planner = Agent(
    role="Goal Planner",
    goal="Break down user goals into SMART tasks",
    backstory="An expert productivity coach",
    verbose=True,
    allow_delegation=False,
    llm=completion(model="ollama/mistral")
)

goal_prompt = """
You are a productivity planner. Break this goal into 5 SMART tasks:

'I want to get fit in 3 months.'

Respond as a numbered list.
"""

planning_task = Task(
    description=goal_prompt,
    agent=planner,
    expected_output="list of tasks"
)

crew = Crew(
    agents=[planner],
    tasks=[planning_task]
)

result = crew.kickoff()
print("✅ Result:\n", result)
