# Auto-Auth0

Auto-Auth0 is an intelligent tool that automatically adds Auth0 authentication to any web project. It uses AI agents to analyze your codebase, understand your Auth0 requirements, and make the necessary changes to integrate Auth0 authentication.

## What This Tool Does

- Takes your existing web application codebase as input
- Reads your Auth0 integration requirements from a markdown file
- Uses AI agents to analyze your code and determine where Auth0 needs to be added
- Automatically makes the necessary code changes to integrate Auth0
- Validates the integration to ensure it's secure and follows best practices

## What This Tool Is Not

- This is NOT a web application that uses Auth0
- This is NOT an Auth0 configuration tool
- This is NOT a manual integration guide

## Agent Specifications

### 1. Manager Agent

- **Role:** Project Manager
- **Goal:** Efficiently manage the crew and ensure high-quality task completion for Auth0 integration
- **Backstory:** You're an experienced project manager, skilled in overseeing complex authentication integration projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.
- **Delegation:** True (allows delegation to other agents)
- **Process:** Hierarchical (manages other agents in a top-down structure)

The Manager Agent coordinates the work between all other agents, ensuring:
- Proper task delegation and sequencing
- Information flow between agents
- Quality control of outputs
- Overall progress tracking
- Issue resolution and handling
- Final integration validation

**Inputs:** Project directory path, initial requirements
**Outputs:** Final integration report with overall status and any issues encountered

**Tools:**
- **File & Code Access:**
  - `FileReadTool` (Required): Read project files and reports
  - `DirectoryReadTool` (Required): Access project structure

### 2. Requirements Analysis Agent

- **Role:** Requirements Analyzer
- **Goal:** Transform the `auth0_integration.md` file into a concise, structured report for downstream agents.
- **Backstory:** Expert in Auth0 configuration and requirements analysis, skilled at extracting key information from documentation.
- **Delegation:** Passes structured requirements report to Codebase Analysis Agent
- **Depends On:** None

**Inputs:** `knowledge/auth0_integration.md` file contents
**Outputs:** Structured JSON/YAML report with key Auth0 requirements and configurations

**Tools:**
- **File & Code Access:**
  - `FileReadTool` (Required): Read and parse the `auth0_integration.md` file

**Tasks:**
- [Required] Read and analyze the `auth0_integration.md` file to extract and structure key information in the file then generate a concise, actionable report for downstream agents

### 3. Codebase Analysis Agent

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

**Tasks:**
- [Required] Generate summary report with:
  - List of files that need to be modified for Auth0 integration
  - For each file:
    - Current purpose/role of the file
    - Required Auth0-related changes
    - Description of the edits needed
    - Any dependencies or prerequisites for the changes
  - Framework-specific considerations
  - Comments for downstream agents

### 4. Auth0 Integration Agent

- **Role:** Code Generator
- **Goal:** Generate and inject secure, framework-specific Auth0 code based on analysis and user requirements.
- **Backstory:** Expert engineer building maintainable auth code across frameworks
- **Delegation:** Outputs files and integration summary to Validation Agent
- **Depends On:** Requirements Analysis Agent, Codebase Analysis Agent

**Outputs:** Modified code files

**Tools:**
  - `FileReadTool` (Required): Read source files for context
  - `FileWriteTool` (Required): Inject generated code
  - `CodeDocsSearchTool` (Optional): Search Auth0 documentation
  - `SerperDevTool` (Optional): Search for Auth0 implementation examples
  - `ScrapeWebsiteTool` (Optional): Extract code snippets from Auth0 docs

**Tasks:**
- [Required] Update all code to implement Auth0 integration based on analysis report and Codebase Analysis Agent

### 5. Validation Agent

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
  - `CodeDocsSearchTool` (Optional): Search Auth0 documentation
  - `SerperDevTool` (Optional): Search for Auth0 implementation examples
  - `ScrapeWebsiteTool` (Optional): Extract code snippets from Auth0 docs
- **Security Heuristics:**
  - OWASP Guidelines (Required): Auth security checklist
  - Heuristic rule checker (Required): Scan for common vulnerabilities

**Tasks:**
- [Required] Analyze Auth0 integration for common security pitfalls:
  * Hardcoded credentials in code
  * Missing CSRF protection
  * Improper token storage/handling
  * Insecure session management
  * Missing error handling
  * Incorrect callback URL validation
  * Insufficient logging
  * Missing rate limiting
  * Insecure password policies
  * Improper role/permission checks

## Prerequisites

- Python >=3.10 <3.13
- Auth0 account with appropriate permissions
- OpenAI API key (OPENAI_API_KEY)
- Serper API key (SERPER_API_KEY)

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
```

3. Configure environment variables. Create a `.env` file in the project root and add your keys:
```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Usage

1. Ensure your `.env` file is correctly configured.
2. Modify the `knowledge/auth0_integration.md` file with your project's specific Auth0 needs.
3. Run the application using `python src/auto_auth0/main.py`.
4. The AI agents will execute sequentially:
    * Analyze your codebase.
    * Read requirements from `knowledge/auth0_integration.md`.
    * Generate and attempt to inject the Auth0 code.
    * Validate the integration.
5. Review the output logs and the changes made to your codebase.

## Project Structure

```
src/                  # Back-end source code
  auto_auth0/
    config/         # Configuration files (agents.yaml, tasks.yaml)
    agents/         # AI agent definitions
    tasks/          # Task definitions
    tools/          # Custom tools
    crew.py         # Main crew orchestration logic
    main.py         # Script to run the crew
knowledge/            # Directory for knowledge files
  auth0_integration.md # User-defined requirements file
auto_auth0_tests/     # Test codebases for input & output testing
  python-web-app/   # Example Python web app without Auth0 integrated
  auth0-python-web-app/ # Example Python web app *with* Auth0 integrated
.env                # Environment variables (sensitive keys)
requirements.txt      # Backend Python dependencies
```