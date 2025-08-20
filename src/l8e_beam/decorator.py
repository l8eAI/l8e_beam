import spacy
from functools import wraps
from importlib import resources
from l8e_beam.redactor import PiiDecoratorBackend
# from .redactor import _recursive_redact, _get_model
from l8e_beam.enums import ModelType, PiiAction


def redact_pii(model: ModelType = ModelType.SM, action: PiiAction = PiiAction.REDACT):
    """
    A decorator to automatically process PII in a function's arguments and return value.

    This is the easiest way to secure an endpoint or function. It recursively
    scans `args` and `kwargs`, processes any strings, dictionaries, lists, or
    Pydantic models, and then does the same for the function's output.

    Args:
        model (ModelType): The spaCy model to use for NER-based PII detection.
            - `ModelType.SM`: A small, fast, general-purpose model.
            - `ModelType.TRF`: A large, slower, but more accurate transformer model.
        action (PiiAction): The action to perform on found PII.
            - `PiiAction.REDACT`: Replaces PII with a placeholder (e.g., `[REDACTED PERSON]`).
            - `PiiAction.ANONYMIZE`: Replaces PII with realistic fake data.
            - `PiiAction.IGNORE`: Leaves the PII untouched.

    Returns:
        The decorated function, which will have its inputs and outputs sanitized.

    Example:
        ```python
        from l8e_beam import redact_pii, PiiAction

        @redact_pii(action=PiiAction.ANONYMIZE)
        def create_test_user(profile: dict):
            # The profile dictionary is already anonymized
            # before this code runs.
            return profile

        user_profile = {"name": "John Doe", "email": "john.doe@example.com"}
        anonymized_profile = create_test_user(user_profile)
        # anonymized_profile will be something like:
        # {'name': 'Mary Smith', 'email': 'robertholmes@example.org'}
        ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Instantiate the backend. It will handle caching.
            backend = PiiDecoratorBackend(model=model, action=action)

            # 2. Process all inputs to the function
            processed_args = backend.process_data(args)
            processed_kwargs = backend.process_data(kwargs)

            # 3. Call the original function with the processed inputs
            result = func(*processed_args, **processed_kwargs)

            # 4. Process the output of the function
            processed_result = backend.process_data(result)

            return processed_result
        return wrapper
    return decorator