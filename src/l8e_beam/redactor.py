import spacy
from importlib import resources
from .enums import ModelType

# --- 1. Setup and Model Loading ---
# This part finds the bundled spaCy model within your package
# and loads it into memory. It runs only once when the module is imported.

# Cache to store loaded models so we don't reload them every time.
_LOADED_MODELS = {}

def _get_model(model: ModelType):
    """Loads a spaCy model from the package, caching it after first load."""
    if model in _LOADED_MODELS:
        return _LOADED_MODELS[model]

    with resources.path('l8e_beam.model', model.value) as model_path:
        nlp = spacy.load(model_path)
        _LOADED_MODELS[model] = nlp
        return nlp

def _redact_text(text: str, nlp) -> str:
    doc = nlp(text)
    pii_labels = {"PERSON", "ORG", "GPE", "LOC", "DATE"}
    new_text = list(text)
    for ent in reversed(doc.ents):
        if ent.label_ in pii_labels:
            new_text[ent.start_char:ent.end_char] = "[REDACTED]"
    return "".join(new_text)

def _recursive_redact(data, nlp):
    """Recursively traverses data structures to find and redact strings."""
    if isinstance(data, str):
        return _redact_text(data, nlp)
    elif isinstance(data, dict):
        return {k: _recursive_redact(v, nlp) for k, v in data.items()}
    elif isinstance(data, list):
        return [_recursive_redact(item, nlp) for item in data]
    # ... handle other iterable types as needed
    else:
        return data