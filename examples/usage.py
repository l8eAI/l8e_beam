# examples/usage.py

# To run this example:
# 1. Make sure you have installed the package in editable mode:
#    pip install -e .
# 2. Run this script from the root of the project:
#    python examples/usage.py

from l8e_beam import redact_pii, ModelType

# --- Example 1: Using the default, fast 'SM' model ---

@redact_pii() # Default is model=ModelType.SM
def process_with_small_model(data: dict):
    """
    This function is decorated to use the small, fast spaCy model.
    It's good for general cases but may miss some nuanced PII.
    """
    print("--- Inside function (SM Model) ---")
    print(f"    Data received: {data}")
    
    # In a real application, you would process the now-redacted data.
    summary = (
        f"Processed request for user '{data.get('user')}' "
        f"regarding trip to '{data.get('destination')}'."
    )
    return {"summary": summary, "data": data}


# --- Example 2: Using the accurate 'TRF' (Transformer) model ---

@redact_pii(model=ModelType.TRF)
def process_with_transformer_model(data: dict):
    """
    This function is decorated to use the large, more accurate transformer model.
    It's better at understanding context and catching tricky PII.
    """
    print("--- Inside function (TRF Model) ---")
    print(f"    Data received: {data}")

    summary = (
        f"Processed request for user '{data.get('user')}' "
        f"regarding trip to '{data.get('destination')}'."
    )
    return {"summary": summary, "data": data}


if __name__ == "__main__":
    # Define a tricky piece of data. The name "Paris" can be a person or a place.
    # The small model might get this wrong, but the transformer should understand the context.
    user_data = {
        "user": "Jane Doe",
        "destination": "Paris, France",
        "notes": "Meeting with John Smith about the new Acme Corp project."
    }

    print("="*60)
    print("RUNNING WITH THE SMALL (SM) MODEL")
    print("="*60)
    sm_result = process_with_small_model(user_data)
    print("\n--- Final Result (SM Model) ---")
    print(sm_result)

    print("\n" + "="*60)
    print("RUNNING WITH THE LARGE (TRF) MODEL")
    print("="*60)
    trf_result = process_with_transformer_model(user_data)
    print("\n--- Final Result (TRF Model) ---")
    print(trf_result)

    print("\n" + "="*60)
    print("OBSERVATION")
    print("="*60)
    print("Notice how the TRF model correctly identified 'Jane doe' as a person")
    print("and 'Paris, France' as a location, redacting both. The SM model may")
    print("have made mistakes, demonstrating the trade-off between speed and accuracy.")

