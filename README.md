Project Title: e.g., "AutoGen Insurance Quote Agents."

PROJECT SCENARIO:
Scenario: Automated Quote Generation & Policy Issuance same as the way you did for Crew AI, replicate the same and replace CrewAI specifics with Autogen

This scenario focuses on the front-end sales process, from the initial customer inquiry to a fully issued policy.

Quote Agent: This agent would be the customer-facing interface. It would interact with the user to collect all necessary information, such as vehicle details, driving history, and personal information. Its goal is to provide an accurate, instant quote.

Underwriting Agent: The Quote Agent hands off the structured data to the Underwriting Agent. This agent's goal is to assess the risk. It would autonomously call various APIs to pull real-time data (e.g., motor vehicle records, credit scores, loss history) and apply complex underwriting rules to either approve the application for straight-through processing or escalate it to a human underwriter.

Policy Agent: Once the Underwriting Agent provides a binding decision, the Policy Agent is triggered. Its goal is to finalize the sale and issue the policy. It would autonomously generate the policy documents, submit them to the Policy Administration System via an API, and communicate with the customer to confirm payment. 

Description: What the agents do (MVR check, underwriting, policy issue).

Setup/Installation: Provide the exact steps (including the correct pip install commands like pip install autogen-agentchat and pip install ollama fix-busted-json).

Execution: The final command to run the script (python main_autogen.py).

Configuration: Note that the Ollama server must be running (http://localhost:11434).

LLM Used: ollama, llama3.2:latest

MAIN FILES: 
insurance_tools_autogen.py is a library (or module) containing only function definitions (check_mvr, issue_policy, etc.). It has no main execution logic.

main_autogen.py uses the Python import statement to load those functions and make them available to the AutoGen agents.

When you run python main_autogen.py, Python automatically executes the necessary imports, loading the tools file into memory. The tools file's code is executed as part of the import process, but only to define the functions—it doesn't start the agent workflow itself.

1. main_autogen.py (The Orchestrator)
This file contains the main execution logic:

It defines the agents (Quote_Agent, Underwriting_Agent, Policy_Agent).

It configures the tools (check_mvr, apply_underwriting_rules, issue_policy) and registers them with the correct agents.

It sets up the GroupChat and GroupChatManager to orchestrate the flow.

It contains the user_proxy.initiate_chat() command, which starts the entire multi-agent process with the customer's input.

2. insurance_tools_autogen.py (The Library)
This file is a library of functions (tools):

It defines the Python functions for check_mvr, issue_policy, and apply_underwriting_rules.

It is designed to be imported by main_autogen.py. It does not contain any executable code that starts the workflow on its own.

AGENTICAI_MULTIAGENT/         <-- Your main project folder (create this anywhere)
├── autogen_env/          <-- The virtual environment folder (created by `python -m venv`)
│   ├── bin/              <-- (or Scripts/ on Windows) Contains the Python executable
│   └── lib/              <-- Contains installed packages (pyautogen, etc.)
├── main_autogen.py       <-- Your primary script (create this file here)
└── insurance_tools_autogen.py  <-- Your tool definitions (create this file here)