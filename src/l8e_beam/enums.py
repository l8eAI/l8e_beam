from enum import Enum

# Enum for model selection to provide type safety and clarity.

class ModelType(Enum):
    """
    Enum for selecting the spaCy model for Named Entity Recognition (NER).
    
    Attributes:
        SM: The small, fast, general-purpose model (`en_core_web_sm`).
        TRF: The large, slower, but more accurate transformer model (`en_core_web_trf`).
    """
    SM = "en_core_web_sm-3.7.1"
    TRF = "en_core_web_trf-3.7.3"


class PiiAction(Enum):
    """
    Enum to define the action to take on a PII finding.
    
    Attributes:
        REDACT: Replaces the PII with a placeholder label (e.g., `[PERSON]`).
        ANONYMIZE: Replaces the PII with realistic fake data.
        IGNORE: Takes no action and leaves the original text.
    """

    REDACT = "redact"
    ANONYMIZE = "anonymize"
    IGNORE = "ignore"