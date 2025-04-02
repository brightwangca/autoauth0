from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool
from pathlib import Path
import yaml

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CodebaseAnalysisCrew:
    """Crew for analyzing codebase for Auth0 integration"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self, project_path: str = None):
        super().__init__()
        self.project_path = project_path
    
    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            allow_delegation=True,
            tools=[
                DirectoryReadTool(directory=self.project_path),
                FileReadTool()
            ],
            verbose=True
        )
    
    @agent
    def requirements_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_analysis_agent'],
            allow_delegation=False,
            tools=[
                DirectoryReadTool(directory=self.project_path),
                FileReadTool()
            ],
            verbose=True
        )
    
    @agent
    def codebase_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['codebase_analysis_agent'],
            allow_delegation=False,
            tools=[
                DirectoryReadTool(directory=self.project_path),
                FileReadTool()
            ],
            verbose=True
        )

    @agent
    def auth0_integration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['auth0_integration_agent'],
            allow_delegation=False,
            tools=[
                DirectoryReadTool(directory=self.project_path),
                FileReadTool()
            ],
            verbose=True
        )

    @agent
    def validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['validation_agent'],
            allow_delegation=False,
            tools=[
                DirectoryReadTool(directory=self.project_path),
                FileReadTool()
            ],
            verbose=True
        )
    
    @task
    def analyze_requirements(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_requirements_task'],
            agent=self.requirements_analysis_agent(),
            context=[{
                "description": "Analyze Auth0 integration requirements from documentation",
                "expected_output": "A structured JSON report containing Auth0 integration requirements and configurations",
                "project_path": self.project_path
            }]
        )
    
    @task
    def analyze_codebase(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_codebase_task'],
            agent=self.codebase_analysis_agent(),
            context=[{
                "description": "Analyze the codebase to identify files that need Auth0 integration",
                "expected_output": "A structured JSON report containing files to modify and framework considerations",
                "project_path": self.project_path
            }]
        )

    @task
    def integrate_auth0(self) -> Task:
        return Task(
            config=self.tasks_config['integrate_auth0_task'],
            agent=self.auth0_integration_agent(),
            context=[{
                "description": "Implement Auth0 integration based on analysis",
                "expected_output": "Modified code files with Auth0 integration",
                "project_path": self.project_path
            }]
        )

    @task
    def validate_integration(self) -> Task:
        return Task(
            config=self.tasks_config['validate_integration_task'],
            agent=self.validation_agent(),
            context=[{
                "description": "Validate Auth0 integration for security and correctness",
                "expected_output": "Validation report with security assessment",
                "project_path": self.project_path
            }]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

class AutoAuth0Crew:
    def __init__(self, project_path: str):
        self.project_path = project_path
    
    def run(self):
        analysis = self.run_codebase_analysis()
        return analysis
    
    def run_codebase_analysis(self):
        crew = CodebaseAnalysisCrew(self.project_path).crew()
        return crew.kickoff()
