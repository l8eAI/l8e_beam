# To run this example:
# 1. Make sure you have installed the package in editable mode:
#    pip install -e .
# 2. Run this script from the root of the project:
#    python examples/usage.py

import pprint
from l8e_beam import redact_pii, ModelType, PiiAction

# --- Example 1: Anonymizing with the default, fast 'SM' model ---

@redact_pii(action=PiiAction.ANONYMIZE) # Default model is ModelType.SM
def anonymize_user_profile(profile: dict):
    """
    This function anonymizes a user profile using the small, fast spaCy model.
    It replaces detected PII with realistic fake data.
    """
    print("--- Inside anonymize_user_profile (SM Model) ---")
    print("    Data has been processed. Now performing business logic...")
    
    # In a real app, you would now work with the anonymized data.
    profile['status'] = 'processed'
    return profile

# --- Example 2: Anonymizing with the accurate 'TRF' (Transformer) model ---

@redact_pii(model=ModelType.TRF, action=PiiAction.ANONYMIZE)
def anonymize_sensitive_notes(notes: str):
    """
    This function uses the large, more accurate transformer model to find
    and anonymize PII that requires more contextual understanding.
    """
    print("\n--- Inside anonymize_sensitive_notes (TRF Model) ---")
    print("    Notes have been processed.")
    return notes

# --- Example 3: Redacting with the accurate 'TRF' (Transformer) model ---

@redact_pii(model=ModelType.TRF, action=PiiAction.REDACT)
def redact_incident_report(report: dict):
    """
    This function redacts a report using the transformer model. It replaces
    PII with a placeholder label indicating the type of PII found.
    """
    print("\n--- Inside redact_incident_report (TRF Model) ---")
    print("    Report has been processed.")
    return report

# --- Main execution block ---


if __name__ == "__main__":
    # --- ANONYMIZE WITH SMALL MODEL ---
    user_profile = {
        "username": "jdoe_123",
        "contact": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "555-867-5309"
        },
        "last_login_ip": "192.168.1.101"
    }

    print("="*60)
    print("RUNNING ANONYMIZATION WITH THE SMALL (SM) MODEL")
    print("="*60)
    print("\nOriginal User Profile:")
    pprint.pprint(user_profile)

    anonymized_profile = anonymize_user_profile(user_profile)

    print("\nAnonymized User Profile:")
    pprint.pprint(anonymized_profile)
    
    # --- ANONYMIZE WITH TRANSFORMER MODEL ---
    sensitive_notes = (
        "Project Alpha report: The project lead, May, will follow up. "
        "Her colleague, April, confirmed the budget."
    )

    print("\n" + "="*60)
    print("RUNNING ANONYMIZATION WITH THE LARGE (TRF) MODEL")
    print("="*60)
    print("\nOriginal Sensitive Notes:")
    print(f'    "{sensitive_notes}"')

    anonymized_notes = anonymize_sensitive_notes(sensitive_notes)

    print("\nAnonymized Sensitive Notes:")
    print(f'    "{anonymized_notes}"')

    # --- REDACT WITH TRANSFORMER MODEL ---
    incident_report = {
        "incident_id": "INC-45892",
        "details": "Client Susan Miller reported a service outage in Berlin.",
        "assigned_to": "tech_ops",
        "company": "affiliated with Acme Corporation"
    }

    print("\n" + "="*60)
    print("RUNNING REDACTION WITH THE LARGE (TRF) MODEL")
    print("="*60)
    print("\nOriginal Incident Report:")
    pprint.pprint(incident_report)

    redacted_report = redact_incident_report(incident_report)

    print("\nRedacted Incident Report:")
    pprint.pprint(redacted_report)

    # --- OBSERVATION ---
    print("\n" + "="*60)
    print("OBSERVATION")
    print("="*60)
    print("1. ANONYMIZE replaces PII with realistic-looking fake data (e.g., 'John Doe' -> 'Mary Smith').")
    print("2. REDACT replaces PII with a placeholder (e.g., 'Susan Miller' -> '[REDACTED PERSON]').")
    print("3. The TRF model correctly understands that 'May' and 'April' are names in the context of the sentence,")
    print("   while a less advanced model might mistake them for dates.")