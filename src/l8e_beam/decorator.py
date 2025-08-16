import spacy
from functools import wraps
from importlib import resources
from .redactor import _recursive_redact, _get_model
from .enums import ModelType


def redact_pii(model: ModelType = ModelType.SM):
    """
    Decorator factory for PII redaction.

    Args:
        model (ModelType): The model to use for redaction. Use ModelType.SM
                           for the small, fast model, or ModelType.TRF for
                           the large, accurate transformer.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nlp = _get_model(model)
            new_args = tuple(_recursive_redact(arg, nlp) for arg in args)
            new_kwargs = {k: _recursive_redact(v, nlp) for k, v in kwargs.items()}
            result = func(*new_args, **new_kwargs)
            return _recursive_redact(result, nlp)
        return wrapper
    return decorator
