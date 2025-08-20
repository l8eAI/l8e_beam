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
    """Loads a spaCy model from the package, caching it after first load."""
    if model in _LOADED_MODELS:
        return _LOADED_MODELS[model]

    with resources.path('l8e_beam.model', model.value) as model_path:
        nlp = spacy.load(model_path)
        _LOADED_MODELS[model] = nlp
        return nlp


class PiiDecoratorBackend:
    """
    Manages PiiProcessor instances and handles the recursive processing
    logic for the decorator. This class ensures that spaCy models are
    loaded only once per model type and cached for efficiency.
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
        Retrieves a PiiProcessor from the cache or creates a new one if it
        doesn't exist for the requested model.
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
        A wrapper around the processor's recursive method.
        """
        rdata = self.processor.process_recursive(data, action=self.action)
        return rdata
