from typing import Any, List, Optional
import spacy

from l8e_beam.enums import PiiAction, ModelType
from l8e_beam.recognizers.base import Recognizer, RegexRecognizer, SpacyRecognizer
from l8e_beam.recognizers.pii_processor import PiiProcessor
from l8e_beam.recognizers.recognizers import REGEX_RECOGNIZERS, SPACY_RECOGNIZERS
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS
from l8e_beam.redactor import _get_model

def sanitize_pii(
    data: Any,
    action: PiiAction = PiiAction.REDACT,
    model: ModelType = ModelType.SM,
    custom_recognizers: Optional[List[Recognizer]] = None,
    disabled_recognizers: Optional[List[DEFAULT_RECOGNIZERS]] = None
) -> Any:
    """
    A direct API for processing data with fine-grained control over recognizers.

    This function recursively traverses data structures (dictionaries, lists, tuples)
    and processes any strings found. It is ideal for complex, dynamic, or
    non-decorator workflows where you need full control.

    Args:
        data: The data to process (e.g., a string, dictionary, list).
        action: The PII action to perform (`REDACT`, `ANONYMIZE`, or `IGNORE`).
        model: The spaCy model to use for NER (`SM` or `TRF`).
        custom_recognizers: A list of user-defined recognizer instances to add.
        disabled_recognizers: A list of default recognizers to disable.

    Returns:
        The processed data with PII handled according to the specified action.

    Example (Disabling a Recognizer):
        ```python
        from l8e_beam import sanitize_pii, PiiAction, DEFAULT_RECOGNIZERS

        report = "Contact support@example.com about the issue with John Smith."

        # Redact the person's name, but leave the email address untouched
        processed_report = sanitize_pii(
            report,
            action=PiiAction.REDACT,
            disabled_recognizers=[DEFAULT_RECOGNIZERS.EMAIL]
        )
        # 'Contact support@example.com about the issue with [REDACTED PERSON].'
        ```

    Example (Adding a Custom Recognizer):
        ```python
        import re
        from l8e_beam import sanitize_pii, RegexRecognizer, PiiAction

        # 1. Define your custom recognizer class
        class UuidRecognizer(RegexRecognizer):
            name = "UUID"
            regex = re.compile(r"[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}", re.I)

        # 2. Pass an instance to the API
        log_entry = "Request failed for user_id: 123e4567-e89b-12d3-a456-426614174000"
        processed_log = sanitize_pii(
            log_entry,
            action=PiiAction.REDACT,
            custom_recognizers=[UuidRecognizer()]
        )
        # 'Request failed for user_id: [REDACTED UUID]'
        ```
    """
    nlp = _get_model(model)
    custom_recognizers = custom_recognizers or []
    disabled_names = {d.value for d in (disabled_recognizers or [])}

    # Filter out any disabled default recognizers
    enabled_regex = [
        r for r in REGEX_RECOGNIZERS if r.name not in disabled_names
    ]
    enabled_spacy = [
        r for r in SPACY_RECOGNIZERS if r.name not in disabled_names
    ]

    # Combine the enabled default recognizers with any custom ones
    all_regex = enabled_regex + [
        r for r in custom_recognizers if isinstance(r, RegexRecognizer)
    ]
    all_spacy = enabled_spacy + [
        r for r in custom_recognizers if isinstance(r, SpacyRecognizer)
    ]

    processor = PiiProcessor(
        regex_recognizers=all_regex,
        spacy_recognizers=all_spacy,
        nlp=nlp
    )

    return processor.process_recursive(data, action=action)
