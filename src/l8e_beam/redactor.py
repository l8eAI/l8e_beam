# src/l8e_beam/redactor.py

"""
Backend components for the PII decorator.

This module contains the logic for loading and caching spaCy models and
the PiiProcessor instances. The primary goal is to ensure that these
heavy objects are created only once and then reused, which significantly
improves performance when the decorator is used on multiple functions or
called multiple times.

This is not part of the public-facing API but is crucial for the
decorator's functionality.
"""
from functools import wraps
from typing import Dict, Any
from importlib import resources
import spacy

# Import the main processor and the action/model enums
from l8e_beam.recognizers.pii_processor import PiiProcessor
from l8e_beam.enums import ModelType, PiiAction

# Import the pre-loaded recognizer lists
from l8e_beam.recognizers.recognizers import REGEX_RECOGNIZERS, SPACY_RECOGNIZERS

_LOADED_MODELS = {}

def _get_model(model: ModelType):
    """
    Loads a spaCy model from the package's internal resources.

    This function caches the model in the `_LOADED_MODELS` dictionary after
    the first load to prevent costly re-initialization on subsequent calls.

    Args:
        model (ModelType): The enum member representing the model to load.

    Returns:
        A loaded spaCy Language object.
    """
    if model in _LOADED_MODELS:
        return _LOADED_MODELS[model]

    with resources.path('l8e_beam.model', model.value) as model_path:
        nlp = spacy.load(model_path)
        _LOADED_MODELS[model] = nlp
        return nlp


class PiiDecoratorBackend:
    """
    Manages PiiProcessor instances for the decorator.

    This class ensures that a `PiiProcessor` is instantiated only once per
    spaCy model type. It holds a class-level cache (`_PROCESSORS`) to store
    these instances. When the `@redact_pii` decorator is used, this backend
    is created, which then retrieves or creates the appropriate processor
    to handle the PII sanitization.

    Attributes:
        model (ModelType): The spaCy model to use for NER.
        nlp (spacy.Language): The loaded spaCy model object.
        action (PiiAction): The PII action to perform (REDACT, ANONYMIZE, IGNORE).
        processor (PiiProcessor): The processor instance for the given model.
    """
    # Class-level cache to store processor instances, keyed by model name
    _PROCESSORS: Dict[str, PiiProcessor] = {}

    def __init__(self, model: ModelType, action: PiiAction):
        """
        Initializes the backend with a specific model and action.

        Args:
            model (ModelType): The spaCy model to use for NER.
            action (PiiAction): The PII action to perform (REDACT, ANONYMIZE, IGNORE).
        """
        self.model = model
        self.nlp = _get_model(model)
        self.action = action
        self.processor = self._get_processor()


    def _get_processor(self) -> PiiProcessor:
        """
        Retrieves a PiiProcessor from the cache or creates a new one.

        This method checks the `_PROCESSORS` cache for an existing processor
        for the requested model. If one is not found, it creates a new
        instance and stores it in the cache for future use.

        Returns:
            The cached or newly created PiiProcessor instance.
        """
        model_name = self.model.value
        if model_name not in self._PROCESSORS:
            # If no processor exists for this model, create and cache it
            print(f"Initializing PiiProcessor with model: {model_name}...")
            self._PROCESSORS[model_name] = PiiProcessor(
                regex_recognizers=REGEX_RECOGNIZERS,
                spacy_recognizers=SPACY_RECOGNIZERS,
                nlp=self.nlp
            )
        return self._PROCESSORS[model_name]


    def process_data(self, data: Any) -> Any:
        """
        A wrapper around the processor's recursive processing method.

        This is the main method called by the decorator to sanitize the
        input arguments and the return value of the decorated function.

        Args:
            data: The data to be sanitized (can be any type).

        Returns:
            The sanitized data.
        """
        rdata = self.processor.process_recursive(data, action=self.action)
        return rdata
