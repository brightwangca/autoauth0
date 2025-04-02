from crewai import Agent
from typing import Dict, List
import json
from pathlib import Path
import yaml
from ..tasks.codebase_analysis_tasks import CodebaseAnalysisTasks

class CodebaseAnalysisAgent:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.config = self._load_config()
        self.agent = self._create_agent()
        self.tasks = CodebaseAnalysisTasks()

    def _load_config(self) -> Dict:
        """Loads the agent configuration from YAML."""
        config_path = Path(__file__).parent.parent / "config" / "agents.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config['codebase_analysis_agent']

    def _create_agent(self) -> Agent:
        """Creates the Codebase Analysis Agent with its specific role and tools."""
        return Agent(
            role=self.config['role'],
            goal=self.config['goal'],
            backstory=self.config['backstory'],
            verbose=self.config['verbose'],
            allow_delegation=self.config['allow_delegation'],
            tools=[
                self._directory_read_tool,
                self._file_read_tool
            ],
            llm_config=self.config.get('llm', {})
        )

    def analyze_codebase(self) -> Dict:
        """Analyzes the codebase and returns a structured report of integration points."""
        analysis_prompt = self.tasks.get_analysis_prompt(self.project_path)
        result = self.agent.execute(analysis_prompt)
        return self._parse_analysis_result(result)

    def analyze_file(self, file_path: str) -> Dict:
        """Analyzes a specific file for Auth0 integration requirements."""
        try:
            file_content = self._file_read_tool(file_path)
            analysis_prompt = self.tasks.get_file_analysis_prompt(file_path, file_content)
            result = self.agent.execute(analysis_prompt)
            return self._parse_analysis_result(result)
        except Exception as e:
            return {"error": f"Failed to analyze file {file_path}: {str(e)}"}

    def analyze_framework(self, framework_type: str) -> Dict:
        """Analyzes framework-specific Auth0 integration requirements."""
        analysis_prompt = self.tasks.get_framework_analysis_prompt(framework_type)
        result = self.agent.execute(analysis_prompt)
        return self._parse_analysis_result(result)

    def _parse_analysis_result(self, result: str) -> Dict:
        """Parses the agent's analysis result into a structured format."""
        try:
            # Attempt to parse as JSON if the result is in JSON format
            return json.loads(result)
        except json.JSONDecodeError:
            # If not JSON, create a structured format from the text
            return {
                "files_to_modify": [],
                "framework_considerations": [],
                "dependencies": [],
                "raw_analysis": result
            }

    def _directory_read_tool(self, path: str) -> List[str]:
        """Tool to read directory contents."""
        try:
            dir_path = Path(self.project_path) / path
            return [str(p.relative_to(self.project_path)) for p in dir_path.iterdir()]
        except Exception as e:
            return [f"Error reading directory: {str(e)}"]

    def _file_read_tool(self, file_path: str) -> str:
        """Tool to read file contents."""
        try:
            full_path = Path(self.project_path) / file_path
            return full_path.read_text()
        except Exception as e:
            return f"Error reading file: {str(e)}" 