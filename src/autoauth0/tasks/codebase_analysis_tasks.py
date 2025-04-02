from typing import Dict
import yaml
from pathlib import Path

class CodebaseAnalysisTasks:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Loads the tasks configuration from YAML."""
        config_path = Path(__file__).parent.parent / "config" / "tasks.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config['codebase_analysis']

    def get_analysis_prompt(self, project_path: str) -> str:
        """Returns the main analysis prompt for the Codebase Analysis Agent."""
        return self.config['main_analysis']['prompt'].format(project_path=project_path)

    def get_file_analysis_prompt(self, file_path: str, file_content: str) -> str:
        """Returns a prompt for analyzing a specific file."""
        return self.config['file_analysis']['prompt'].format(
            file_path=file_path,
            file_content=file_content
        )

    def get_framework_analysis_prompt(self, framework_type: str) -> str:
        """Returns a prompt for analyzing framework-specific requirements."""
        return self.config['framework_analysis']['prompt'].format(framework_type=framework_type) 