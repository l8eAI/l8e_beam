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

    Args:
        data: The data to process.
        action: The PII action to perform.
        model: The spaCy model to use for NER.
        custom_recognizers: A list of user-defined recognizer instances to add.
        disabled_recognizers: A list of names of default recognizers to disable.
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
