# src/l8e_beam/tests/test_redaction.py

import unittest
from unittest.mock import patch, Mock
# Import the actual cache dictionary to clear it
from l8e_beam.redactor import PiiDecoratorBackend, _get_model, _LOADED_MODELS
from l8e_beam.decorator import redact_pii
from l8e_beam.enums import PiiAction, ModelType

class TestPiiDecoratorBackend(unittest.TestCase):
    """Tests the backend logic for model/processor caching."""

    def setUp(self):
        # FIX: Clear the actual cache dictionary (_LOADED_MODELS)
        _LOADED_MODELS.clear()
        PiiDecoratorBackend._PROCESSORS.clear()

    @patch('l8e_beam.redactor.spacy.load')
    @patch('l8e_beam.redactor.resources.path')
    def test_get_model_caching(self, mock_path, mock_spacy_load):
        """Verify that a spaCy model is loaded only once."""
        mock_path.return_value.__enter__.return_value = "fake/path"
        mock_spacy_load.return_value = "mock_model"

        _get_model(ModelType.SM)
        _get_model(ModelType.SM) # Second call should use the cache
        mock_spacy_load.assert_called_once()

    @patch('l8e_beam.redactor.PiiProcessor')
    @patch('l8e_beam.redactor._get_model')
    def test_processor_caching(self, mock_get_model, MockPiiProcessor):
        """Verify that a PiiProcessor is instantiated only once per model."""
        backend = PiiDecoratorBackend(model=ModelType.SM, action=PiiAction.REDACT)
        backend._get_processor()
        backend._get_processor() # Second call should use the cache
        MockPiiProcessor.assert_called_once()

class TestRedactPiiDecorator(unittest.TestCase):
    """Tests the decorator's logic of handling args, kwargs, and return values."""

    @patch('l8e_beam.decorator.PiiDecoratorBackend')
    def test_decorator_passes_correct_action(self, MockBackend):
        """Ensure the decorator initializes the backend with the correct PiiAction."""
        mock_instance = MockBackend.return_value
        # FIX: Configure the mock to return the data it receives. This prevents
        # the TypeError by ensuring the correct number of arguments are passed.
        mock_instance.process_data.side_effect = lambda data: data

        @redact_pii(action=PiiAction.ANONYMIZE)
        def get_user_data(user_id):
            return f"data for {user_id}"

        get_user_data(123)

        # Verify that the backend was created with the ANONYMIZE action
        MockBackend.assert_called_with(model=ModelType.SM, action=PiiAction.ANONYMIZE)