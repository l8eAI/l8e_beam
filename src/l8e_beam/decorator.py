import spacy
from functools import wraps
from importlib import resources
from l8e_beam.redactor import PiiDecoratorBackend
# from .redactor import _recursive_redact, _get_model
from l8e_beam.enums import ModelType, PiiAction


def redact_pii(model: ModelType = ModelType.SM, action: PiiAction = PiiAction.REDACT):
    """
    A decorator to process PII in the inputs and outputs of a function.

    Args:
        model (ModelType): The spaCy model to use (e.g., ModelType.SM for the
                           small model, ModelType.LG for the large one).
        action (PiiAction): The action to perform on found PII (REDACT,
                            ANONYMIZE, or IGNORE).
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