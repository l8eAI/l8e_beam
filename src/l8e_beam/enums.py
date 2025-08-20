from enum import Enum

# Enum for model selection to provide type safety and clarity.

class ModelType(Enum):

    SM = "en_core_web_sm-3.7.1"
    TRF = "en_core_web_trf-3.7.3"


class PiiAction(Enum):
    """Enum to define the action to take on a PII finding."""

    REDACT = "redact"
    ANONYMIZE = "anonymize"
    IGNORE = "ignore"