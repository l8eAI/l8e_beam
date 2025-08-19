# examples/integrate_fastapi.py

# To run this example:
# 1. Make sure you have installed the package in editable mode:
#    pip install -e .
# 2. Install FastAPI and Uvicorn:
#    pip install "fastapi[all]" uvicorn
# 3. Run this script from the root of the project:
#    uvicorn examples.integrate_fastapi:app --reload

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

# Import the necessary components from l8e-beam
from l8e_beam import redact_pii, sanitize_pii, PiiAction, ModelType

# --- 1. Define a Pydantic model for our request body ---
# This represents the data structure our API will accept.
class UserContext(BaseModel):
    user_id: str
    full_name: str
    query: str
    metadata: Optional[dict] = None

# --- 2. Create the FastAPI application ---
app = FastAPI(
    title="l8e-beam FastAPI Integration",
    description="Demonstrating how to use l8e-beam to protect PII in a web API."
)

# --- 3. Simple Usage: Using the @redact_pii Decorator ---
# This is the easiest way to secure an endpoint. The decorator will automatically
# process the `context` argument because it's a Pydantic model, and then
# process the return value before it's sent back to the client.

@app.post("/process-with-decorator")
@redact_pii(action=PiiAction.ANONYMIZE, model=ModelType.TRF)
def process_with_decorator(context: UserContext):
    """
    This endpoint is protected by the @redact_pii decorator.
    It will automatically anonymize the incoming user context.
    """
    print(f"Inside decorator endpoint. Data received: {context.dict()}")
    
    # In a real application, you would now pass this sanitized context
    # to a language model or another service.
    # For this example, we'll just return it.
    return {"status": "processed", "sanitized_context": context}


# --- 4. Advanced Usage: Using the sanitize_pii API ---
# This approach gives you full control inside your endpoint. You can inspect
# the data, apply conditional logic, and then decide how to sanitize it.

@app.post("/process-with-api")
def process_with_api(context: UserContext, redact: bool = Query(True, description="Set to false to ignore PII")):
    """
    This endpoint uses the sanitize_pii function for dynamic control.
    - If `redact=true` (default), it redacts PII.
    - If `redact=false`, it leaves the data as is.
    """
    print(f"Inside API endpoint. Original data: {context.dict()}")

    # Here, we can apply business logic before sanitization.
    # For example, only redact data if a certain condition is met.
    if redact:
        action = PiiAction.REDACT
        print("Redaction is ON. Sanitizing data...")
    else:
        action = PiiAction.IGNORE
        print("Redaction is OFF. Ignoring PII...")

    # Call the sanitize_pii function directly on the data
    sanitized_context = sanitize_pii(
        data=context.dict(), # Pass the data as a dictionary
        action=action,
        model=ModelType.TRF # Use the more accurate model
    )

    # You can now work with the sanitized data
    return {"status": "processed", "final_context": sanitized_context}

# --- 5. How to Run the Application ---
# Use the following command in your terminal from the project root:
# uvicorn examples.integrate_fastapi:app --reload
#
# Then, you can send POST requests to:
# - http://127.0.0.1:8000/process-with-decorator
# - http://127.0.0.1:8000/process-with-api?redact=false
#
# Example request body (for both endpoints):
# {
#   "user_id": "user-123",
#   "full_name": "Jane Doe",
#   "query": "Please book a flight to Paris for me.",
#   "metadata": { "source_ip": "192.168.1.1" }
# }

if __name__ == "__main__":
    import uvicorn
    print("To run this FastAPI application, use the command:")
    print("uvicorn examples.integrate_fastapi:app --reload")
    # This block is for informational purposes; uvicorn is the preferred way to run.
    # uvicorn.run(app, host="0.0.0.0", port=8000)

