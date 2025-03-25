# agents/planner_agent.py

from crewai import Agent, Task, Crew

from llm.llm_wrapper import LocalLLM


class GoalPlanner:
    def __init__(self, model_name="mistral"):
        self.llm = LocalLLM(model_name=model_name)
        self.agent = Agent(
            role="Goal Planner",
            goal="Break down user goals into tangible, scheduled tasks.",
            backstory="An expert productivity coach helping users achieve their goals effectively.",
            verbose=True,
            allow_delegation=False,
            tools=[],  # We’ll add calendar tool later
            llm=self.llm.generate  # Pass the Ollama-backed function
        )

    def plan(self, user_goal: str) -> str:
        prompt = f"""
        You are a productivity assistant. Your task is to break down the following user goal into a list of SMART subtasks (Specific, Measurable, Achievable, Relevant, Time-bound). Spread them over the next few weeks, and include the frequency if needed.
        
        User goal: "{user_goal}"
        
        Provide the output as a numbered list with one task per line.
        """
        task = Task(
            description=prompt,
            agent=self.agent
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        result = crew.run()
        return result
