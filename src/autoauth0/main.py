#!/usr/bin/env python
import os
import textwrap
from pathlib import Path
from dotenv import load_dotenv
from src.autoauth0.crew import AutoAuth0Crew

# Load environment variables from .env file
load_dotenv()

def main():
    print(textwrap.dedent("""
        Welcome to Auto-Auth0

        This tool will analyze your codebase and integrate Auth0 authentication.
    """))

    project_path = "/Users/brightwang/Documents/Github/autoauth0/auto_auth0_tests/auth0-python-web-app"
    print(f"\nAnalyzing project at: {project_path}\n")

    if not os.path.exists(project_path):
        print(f"Error: Project path {project_path} does not exist.")
        return

    crew = AutoAuth0Crew(project_path)
    result = crew.run()
    print(result)

if __name__ == "__main__":
    main()
