# insurance_tools_autogen.py

import random
from typing import Annotated

# Define a custom type hint for data structure passing between agents
StructuredData = Annotated[str, "A structured string or JSON containing collected customer and quote data."]


# --- Tool for Underwriting Agent (MVR Check) ---
def check_mvr(driving_history: StructuredData) -> str:
    """
    Checks the Motor Vehicle Record (MVR) for a customer's driving history.
    Simulates an API call to a state DMV or third-party data provider.
    Returns a structured MVR report and a risk score.
    """
    # NOTE: The LLM will pass the relevant part of the data (driving_history)
    # The actual implementation parses the string input.
    if "DUI" in driving_history or "major accident" in driving_history:
        risk_level = "High Risk"
        risk_score = 0.95
    elif "no claims" in driving_history or "clean record" in driving_history:
        risk_level = "Low Risk"
        risk_score = 0.20
    else:
        risk_level = "Moderate Risk"
        risk_score = 0.55

    mvr_data = f"MVR_REPORT: Risk: {risk_level} (Score: {risk_score:.2f}). Driving History used: {driving_history}"
    return mvr_data

# --- Tool for Underwriting Agent (Rules Engine) ---
def apply_underwriting_rules(customer_data_and_mvr: StructuredData) -> str:
    """
    Applies a set of complex underwriting rules to all collected customer data 
    and MVR to determine a final decision.
    Returns a binding decision: 'APPROVED' or 'ESCALATE to Human', and the quote amount.
    """
    # NOTE: The LLM should pass the full history string here.
    if "High Risk" in customer_data_and_mvr:
        return "Underwriting Decision: ESCALATE to Human Underwriter. High-Risk profile due to MVR."
    elif "Low Risk" in customer_data_and_mvr and "2015" not in customer_data_and_mvr:
        return "Underwriting Decision: APPROVED for straight-through processing. Final Quote: $1200/year."
    else:
        return "Underwriting Decision: APPROVED with conditions. Final Quote: $1800/year."

# --- Tool for Policy Agent (PAS API) ---
def issue_policy(quote_details: StructuredData) -> str:
    """
    Submits finalized quote details to the Policy Administration System (PAS) 
    and simulates the policy issuance process.
    Returns the final policy number and issuance status.
    """
    policy_number = f"POL-{random.randint(100000, 999999)}"
    
    if "APPROVED" in quote_details:
        status = f"Policy successfully issued with Policy Number: {policy_number}. Payment confirmation sent. Final Quote: {quote_details}"
    else:
        status = "Policy issuance failed. Underwriting decision was not APPROVED. Escalating to human underwriter."

    return status