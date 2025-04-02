# Auto-Auth0

Auto-Auth0 is an intelligent application that simplifies and accelerates the process of integrating Auth0 authentication into your web projects. It uses a CrewAI-powered system to analyze your codebase, read your requirements from a markdown file, and manage the integration process.

## Architecture

The application uses **CrewAI** and **Python**:
- It hosts specialized AI agents (Codebase Analyzer, Auth0 Integrator, etc.).
- It performs codebase analysis, reads requirements from `knowledge/auth0_integration.md`.
- It generates Auth0 integration code and validates the results.

## Agent Specifications

---

### 1. Codebase Analysis Agent

- **Role:** Analyzer
- **Goal:** Identify key code sections in the developer's project suitable for Auth0 integration.
- **Backstory:** Expert in navigating code structures across various frameworks to locate integration points seamlessly.
- **Delegation:** Passes detailed code analysis reports and suggestions to the Auth0 Integration Agent.
- **Depends On:** None

**Inputs:** Project directory path, file tree
**Outputs:** JSON/YAML report with integration points, file classifications, and hints

**Tools:**
- **File & Code Access:**
  - `DirectoryReadTool` (Required): Explore folder and file structures
  - `FileReadTool` or `CodeReadTool` (Required): Read relevant source files
- **Search & Reference:**
  - `GitHubSearchTool` (Optional): Search example codebases
- **Custom:**
  - `Tree-sitter`: Parse language-specific syntax trees

**Tasks:**
- [Required] Detect framework and language (e.g., React, Node.js, Django)
- [Required] Generate summary report with:
  - Framework/language
  - Recommended integration points (paths, line refs)
  - File classification (routes, middleware, etc.)
  - Comments for downstream agents
- [Optional] Tree traversal/parsing with Tree-sitter
- [Optional] Identify entry points, route definitions, etc.
- [Optional] Classify files by role

---

### 2. Auth0 Integration Agent

- **Role:** Code Generator
- **Goal:** Generate and inject secure, framework-specific Auth0 code based on analysis and user requirements.
- **Backstory:** Expert engineer building maintainable auth code across frameworks
- **Delegation:** Outputs files and integration summary to Validation Agent
- **Depends On:** Codebase Analysis Agent, User-provided `knowledge/auth0_integration.md` file

**Inputs:** Analysis report, `knowledge/auth0_integration.md` file contents
**Outputs:** Modified code files, code diff map (optional)

**Tools:**
- **File & Code Access:**
  - `FileReadTool` (Required): Read source files for context and the `auth0_integration.md` file.
  - `FileWriteTool` (Required): Inject generated code
- **LLM & Docs:**
  - Claude/GPT-4 (Required): Generate integration logic
  - `Code Docs RAG Search` (Required): Retrieve best practices from Auth0 docs
- **Search & Reference:**
  - `GitHubSearchTool` (Optional): Reference open-source examples
- **Custom:**
  - Code formatter/injector: Style-consistent insertion

**Tasks:**
- [Required] Parse analysis report and `auth0_integration.md` file.
- Generate code: config files, handlers, middleware logic
- [Required] Insert code using write tool
- [Optional] Respect style/framework conventions
- [Optional] Output change map

---

### 3. Validation Agent

- **Role:** Security Auditor
- **Goal:** Validate Auth0 integration code for correctness and security
- **Backstory:** Security-first reviewer trained on OWASP and modern auth practices
- **Delegation:** Sends feedback to Code Generation Agent if needed
- **Depends On:** Auth0 Integration Agent

**Inputs:** Generated codebase, integration summary
**Outputs:** Validation report with confidence score and recommendations

**Tools:**
- **File & Code Access:**
  - `FileReadTool` (Required): Review integrated files
- **Security Heuristics:**
  - OWASP Guidelines (Required): Auth security checklist
  - Heuristic rule checker (Required): Scan for common vulnerabilities
- **Search & Reference:**
  - `GitHubSearchTool` (Optional): Compare with verified codebases
- **Custom:**
  - Static validation rule set: Detect anti-patterns

**Tasks:**
- Scan for required components (token handling, session, logout)
- [Required] Detect insecure practices (hardcoded secrets, CSRF)
- [Optional] Match against best practices
- [Required] Output annotated checklist with confidence score

## Prerequisites

- Python >=3.10 <3.13
- Auth0 account with appropriate permissions
- OpenAI API key
- Git repository with appropriate access (if using related tools)

## Installation

1. Install UV (Python package manager), if you don't have it:
```bash
pip install uv
```

2. Create a virtual environment and install project dependencies:
```bash
# Create venv (example using standard venv)
python -m venv .venv
source .venv/bin/activate # Or `.venv\Scripts\activate` on Windows

# Install dependencies using uv (or pip)
uv pip install -r requirements.txt # Or pip install -r requirements.txt
# Alternatively, if using crewai install:
# crewai install
```

3. Configure environment variables. Create a `.env` file in the project root and add your keys:
```
OPENAI_API_KEY=your_openai_api_key
# Required if using Auth0-specific tools/API calls:
# AUTH0_DOMAIN=your_auth0_domain
# AUTH0_CLIENT_ID=your_auth0_client_id
# AUTH0_CLIENT_SECRET=your_auth0_client_secret
# Required if using GitHub tools:
# GITHUB_TOKEN=your_github_token
```

## Running the Application

1.  **Prepare Requirements:** Fill in the `knowledge/auth0_integration.md` file with your specific Auth0 integration requirements. Detail things like:
    *   Authentication methods desired (e.g., Email/Password, Google Social Login)
    *   Application Type (e.g., Regular Web App, Single Page App)
    *   Callback URL(s)
    *   Logout URL(s)
    *   Role-Based Access Control (RBAC) needs
    *   Multi-Factor Authentication (MFA) requirements
    *   Any other specific configurations.

2.  **Run the Crew:**
    Open a terminal in the project root directory (with your virtual environment activated) and run the main script:
    ```bash
    python src/auto_auth0/main.py
    ```
    You may need to adjust `src/auto_auth0/main.py` to pass the correct initial inputs (like the target project path) to the `kickoff` method if they are not hardcoded or handled via arguments. Currently, it uses placeholder inputs.

## Usage

1.  Ensure your `.env` file is correctly configured.
2.  Modify the `knowledge/auth0_integration.md` file with your project's specific Auth0 needs.
3.  Run the application using `python src/auto_auth0/main.py`.
4.  The AI agents will execute sequentially:
    *   Analyze your codebase.
    *   Read requirements from `knowledge/auth0_integration.md`.
    *   Generate and attempt to inject the Auth0 code.
    *   Validate the integration.
5.  Review the output logs and the changes made to your codebase.

## Features

- Intelligent codebase analysis
- Requirements definition via Markdown file
- Automated Auth0 code generation
- Security best practice validation
- Multi-framework support (potential, depending on agent capabilities)

## Development

The project structure:
```
src/                  # Back-end source code
  auto_auth0/
    config/         # Configuration files (agents.yaml, tasks.yaml)
    agents/         # AI agent definitions (loaded from config in crew.py)
    tasks/          # Task definitions (loaded from config in crew.py)
    tools/          # Custom tools (FileReadTool, etc.)
    crew.py         # Main crew orchestration logic
    main.py         # Script to run the crew
    # ... other backend modules
knowledge/            # Directory for knowledge files
  auth0_integration.md # User-defined requirements file
auto_auth0_tests/     # Test codebases
  python-web-app/   # Cleaned Python web app for testing
  # ... other test cases
.env                # Environment variables (sensitive keys)
requirements.txt      # Backend Python dependencies
README.md
LICENSE
# ... other project files (.gitignore, etc.)
```

## Configuration

The back-end system can be configured through several YAML files:
- `src/auto_auth0/config/agents.yaml`: Define AI agent roles and capabilities
- `src/auto_auth0/config/tasks.yaml`: Configure specific Auth0 integration tasks
- `src/auto_auth0/crew.py`: Customize agent interactions and workflows
- `src/auto_auth0/main.py`: Adjust execution flow and initial inputs