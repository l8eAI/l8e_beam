import pprint
import re
import uuid

# Import the direct API function and the necessary components
from l8e_beam import sanitize_pii, RegexRecognizer, PiiAction, DEFAULT_RECOGNIZERS

# --- Setup for Example 3: Define a custom recognizer ---
class UuidRecognizer(RegexRecognizer):
    """A custom recognizer to find and handle UUIDs."""
    name = "UUID"
    regex = re.compile(
        r"[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}", 
        re.IGNORECASE
    )

    def anonymize(self, text: str) -> str:
        """Define how to create a fake UUID."""
        return str(uuid.uuid4())

# --- Main execution block ---
if __name__ == "__main__":
    print("="*60)
    print("Advanced API Usage: sanitize_pii")
    print("="*60)

    # --- Example 1: Simple Anonymization of a Dictionary ---
    user_profile = {
        "name": "Jane Doe",
        "contact_info": {
            "email": "jane.doe@example.com"
        }
    }
    print("\n--- 1. Anonymizing a Dictionary ---")
    print("\nOriginal Profile:")
    pprint.pprint(user_profile)
    
    anonymized_profile = sanitize_pii(user_profile, action=PiiAction.ANONYMIZE)
    
    print("\nAnonymized Profile:")
    pprint.pprint(anonymized_profile)
    
    # --- Example 2: Disabling a Default Recognizer ---
    report_text = "Please email security@example.com about the incident involving John Smith."
    
    print("\n\n--- 2. Disabling a Default Recognizer ---")
    print(f"\nOriginal Text:\n  '{report_text}'")
    
    # Redact PII, but ignore emails by disabling the EMAIL recognizer
    redacted_report = sanitize_pii(
        report_text, 
        action=PiiAction.REDACT,
       disabled_recognizers=[DEFAULT_RECOGNIZERS.EMAIL]
    )

    print(f"\nText with EMAIL recognizer disabled:\n  '{redacted_report}'")

    # --- Example 3: Adding a Custom Recognizer ---
    log_entry = f"User authenticated successfully. Session ID is {uuid.uuid4()}."
    
    print("\n\n--- 3. Adding a Custom Recognizer ---")
    print(f"\nOriginal Log Entry:\n  '{log_entry}'")
    
    # Create an instance of our custom recognizer
    uuid_recognizer = UuidRecognizer()
    
    # Redact the log, using the custom recognizer to find the UUID
    redacted_log = sanitize_pii(
        log_entry,
        action=PiiAction.REDACT,
        custom_recognizers=[uuid_recognizer]
    )
    
    print(f"\nRedacted Log with custom UUID recognizer:\n  '{redacted_log}'")