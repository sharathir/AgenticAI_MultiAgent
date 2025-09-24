# main_autogen.py

import os
import autogen
from autogen.agentchat import AssistantAgent, UserProxyAgent
from autogen.agentchat.groupchat import GroupChat, GroupChatManager
from insurance_tools_autogen import check_mvr, apply_underwriting_rules, issue_policy

# 1. Configuration Setup
# Using a simple OpenAI config structure. Replace with your actual LLM config (e.g., Ollama).
config_list_ollama = [
    {
        "model": os.getenv("OLLAMA_MODEL", "llama3.2:latest"), # Use the model you pulled (e.g., llama3)
        "api_type": "ollama",
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    }
]

llm_config = {"config_list": config_list_ollama, "cache_seed": 42}


# 2. Agent Definitions

# 1. Quote Agent: Gathers and structures initial data.
quote_agent = AssistantAgent(
    name="Quote_Agent",
    system_message=(
        "You are the friendly, front-end sales interface. Your goal is to extract "
        "Customer Name, Age, Vehicle Year/Make/Model, Location, and Driving History "
        "from the user's initial message. **You MUST present this collected data as a "
        "single, clean structured message (e.g., Python dict or JSON string)** for the next agent, "
        "and then state: 'Data collection complete. Pass to Underwriting_Agent.' "
        "Do not call any tools."
    ),
    llm_config=llm_config,
)

# 2. Underwriting Agent: Calls tools to assess risk.
underwriting_agent = AssistantAgent(
    name="Underwriting_Agent",
    system_message=(
        "You are a meticulous Senior Underwriter. Your task is to receive the structured customer data, "
        "use the 'check_mvr' tool with the Driving History, then use the 'apply_underwriting_rules' tool "
        "with ALL collected data and the MVR report to determine the binding decision. "
        "Your final output MUST be the full decision (APPROVED/ESCALATE) and the quote amount, and "
        "then state: 'Underwriting complete. Pass to Policy_Agent.'"
    ),
    llm_config=llm_config,
)

# 3. Policy Agent: Issues the policy using a tool.
policy_agent = AssistantAgent(
    name="Policy_Agent",
    system_message=(
        "You are the administrative expert. Receive the final underwriting decision and quote. "
        "Use the 'issue_policy' tool with the full decision and quote as input. "
        "Your final message must be the confirmation or escalation, ending with 'TERMINATE'."
    ),
    llm_config=llm_config,
)

# 4. User Proxy Agent: Orchestrates and executes tools.
user_proxy = UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"use_docker": False},  # Set to True for security
    max_consecutive_auto_reply=15,
)

# 3. Register Tools for Execution
# Register the functions with the agents who will suggest them (LLM) and the agent who will run them (Proxy)
autogen.register_function(
    check_mvr,
    caller=underwriting_agent, 
    executor=user_proxy, 
    description=check_mvr.__doc__,
)

autogen.register_function(
    apply_underwriting_rules,
    caller=underwriting_agent, 
    executor=user_proxy, 
    description=apply_underwriting_rules.__doc__,
)

autogen.register_function(
    issue_policy,
    caller=policy_agent, 
    executor=user_proxy, 
    description=issue_policy.__doc__,
)


# 4. Group Chat and Manager Setup
# The manager orchestrates the sequential flow based on agent system messages/prompts.
group_chat = GroupChat(
    agents=[user_proxy, quote_agent, underwriting_agent, policy_agent], 
    messages=[], 
    max_round=20,
    speaker_selection_method="auto"  # LLM decides the next speaker
)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)


# 5. Initiate the Workflow
customer_input = (
    "Hello, I need a quote. My name is Alex Johnson, I'm 35. "
    "My car is a 2022 Tesla Model 3. I live in Austin, Texas, "
    "and I have a clean driving record with no claims in 5 years."
)

print("--- Starting Automated Quote Generation & Policy Issuance AutoGen Workflow ---")
chat_result = user_proxy.initiate_chat(
    manager,
    message=customer_input,
)

print("\n\n######################################################################")
print("## Final Result: Policy Issuance and Customer Communication ##")
print("######################################################################")
print(chat_result.summary)