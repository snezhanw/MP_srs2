from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_google_genai import ChatGoogleGenerativeAI
import os

@CrewBase
class SrsProject():
    """SrsProject crew для адаптации иностранных студентов в KazNU"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7, 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    @agent
    def cultural_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['cultural_analyst'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False 
        )

    @agent
    def campus_guide(self) -> Agent:
        return Agent(
            config=self.agents_config['campus_guide'],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def cultural_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['cultural_analysis_task'],
        )

    @task
    def campus_guide_task(self) -> Task:
        return Task(
            config=self.tasks_config['campus_guide_task'],
        )

    @crew
    def crew(self) -> Crew: 
        """Создает экипаж SrsProject"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )