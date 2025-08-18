import unittest
from unittest.mock import patch, Mock
from l8e_beam.api import sanitize_pii
from l8e_beam.enums import PiiAction, ModelType
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS


class TestSanitizePiiApi(unittest.TestCase):
    """Unit tests for the sanitize_pii API function."""


    @patch('l8e_beam.api.PiiProcessor')
    @patch('l8e_beam.api._get_model')
    def test_basic_call_with_defaults(self, mock_get_model, MockPiiProcessor):
        """
        Verify the function calls the processor with default recognizers and parameters.
        """
        mock_email_recognizer = Mock()
        mock_email_recognizer.name = 'EMAIL' # This sets the attribute
        
        mock_person_recognizer = Mock()
        mock_person_recognizer.name = 'PERSON' # This sets the attribute

        # Patch the lists with our configured mocks for this test only.
        with patch('l8e_beam.api.REGEX_RECOGNIZERS', [mock_email_recognizer]), \
             patch('l8e_beam.api.SPACY_RECOGNIZERS', [mock_person_recognizer]):
            
            mock_nlp = "mock_nlp_object"
            mock_get_model.return_value = mock_nlp
            mock_processor_instance = MockPiiProcessor.return_value
            
            sanitize_pii("test data")

            mock_get_model.assert_called_once_with(ModelType.SM)
            MockPiiProcessor.assert_called_once()
            args, kwargs = MockPiiProcessor.call_args

            # Now this assertion correctly compares a string to a string.
            self.assertEqual(kwargs['regex_recognizers'][0].name, 'EMAIL')
            self.assertEqual(kwargs['spacy_recognizers'][0].name, 'PERSON')
            self.assertEqual(kwargs['nlp'], mock_nlp)

            mock_processor_instance.process_recursive.assert_called_once_with(
                "test data", action=PiiAction.REDACT
            )

    @patch('l8e_beam.api.PiiProcessor')
    @patch('l8e_beam.api._get_model')
    def test_with_disabled_recognizer(self, mock_get_model, MockPiiProcessor):
        """
        Test that default recognizers can be disabled.
        """
        # FIX: Create mocks and set their .name attribute directly.
        mock_email = Mock()
        mock_email.name = 'EMAIL'

        mock_phone = Mock()
        mock_phone.name = 'PHONE'

        # Patch the list with our properly configured mocks.
        with patch('l8e_beam.api.REGEX_RECOGNIZERS', [mock_email, mock_phone]):
            sanitize_pii(
                "test data",
                disabled_recognizers=[DEFAULT_RECOGNIZERS.EMAIL]
            )

            MockPiiProcessor.assert_called_once()
            args, kwargs = MockPiiProcessor.call_args

            recognizer_names = [r.name for r in kwargs['regex_recognizers']]

            # This assertion will now pass because the EMAIL mock was successfully filtered out.
            self.assertEqual(len(recognizer_names), 1)
            self.assertIn('PHONE', recognizer_names)
            self.assertNotIn('EMAIL', recognizer_names)

    @patch('l8e_beam.api.PiiProcessor')
    @patch('l8e_beam.api._get_model')
    def test_non_default_action_and_model(self, mock_get_model, MockPiiProcessor):
        """
        Test that custom 'action' and 'model' parameters are used correctly.
        """
        mock_processor_instance = MockPiiProcessor.return_value

        sanitize_pii(
            "test data", 
            action=PiiAction.ANONYMIZE,
            model=ModelType.TRF
        )

        # Verify the correct model was loaded
        mock_get_model.assert_called_once_with(ModelType.TRF)
        
        # Verify the correct action was passed to the processing method
        mock_processor_instance.process_recursive.assert_called_once_with(
            "test data", action=PiiAction.ANONYMIZE
        )

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)