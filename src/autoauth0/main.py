#!/usr/bin/env python
import os
import textwrap
from pathlib import Path
from dotenv import load_dotenv
from crew import AutoAuth0Crew

# Load environment variables from .env file
load_dotenv()

def main():
    print(textwrap.dedent("""
        Welcome to Auto-Auth0

        This tool will analyze your codebase and integrate Auth0 authentication.
    """))

    # Get the absolute path to the test project
    current_dir = Path(__file__).parent.parent.parent
    test_project_path = current_dir / "auto_auth0_tests" / "auth0-python-web-app"
    
    # Initialize and run the crew
    crew = AutoAuth0Crew(str(test_project_path))
    result = crew.run()
    print(result)

if __name__ == "__main__":
    main()
