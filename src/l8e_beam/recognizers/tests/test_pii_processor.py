# tests/test_pii_processor.py

import unittest
from unittest.mock import Mock, MagicMock

from l8e_beam.recognizers.pii_processor import PiiProcessor
from l8e_beam.enums import PiiAction
from l8e_beam.recognizers.base import Finding

# A mock Pydantic-like class for testing
class MockPydanticModel:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def dict(self):
        return {"user": self.user, "message": self.message}
        
    # Add an equality method for easier testing
    def __eq__(self, other):
        return isinstance(other, MockPydanticModel) and self.user == other.user and self.message == other.message

class TestPiiProcessor(unittest.TestCase):

    def setUp(self):
        """Set up a PiiProcessor with mock recognizers."""
        # Mock recognizers
        self.mock_email_recognizer = Mock(name="EMAIL")
        self.mock_person_recognizer = Mock(name="PERSON")
        
        # Configure anonymize return values
        self.mock_email_recognizer.anonymize.return_value = "fake@email.com"
        self.mock_person_recognizer.anonymize.return_value = "Fake Name"

        # --- FIX: Make mock analyze methods dynamic ---
        # The mocks now inspect the text they receive.
        def mock_email_analyze(text, findings):
            if "test@example.com" in text:
                start = text.find("test@example.com")
                findings.append(Finding("test@example.com", "EMAIL", start, start + len("test@example.com"), self.mock_email_recognizer))
        
        def mock_person_analyze(doc, findings):
            # This mock now looks for specific names in the doc's text
            names_to_find = ["John Doe", "Jane Smith"]
            for name in names_to_find:
                if name in doc.text:
                    start = doc.text.find(name)
                    findings.append(Finding(name, "PERSON", start, start + len(name), self.mock_person_recognizer))

        self.mock_email_recognizer.analyze = mock_email_analyze
        self.mock_person_recognizer.analyze = mock_person_analyze

        # Mock the nlp object to just pass the text through
        mock_nlp = MagicMock()
        mock_nlp.side_effect = lambda text: MagicMock(text=text, ents=[])

        self.processor = PiiProcessor(
            regex_recognizers=[self.mock_email_recognizer],
            spacy_recognizers=[self.mock_person_recognizer],
            nlp=mock_nlp
        )

    def test_process_redact(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.REDACT)
        self.assertEqual(result, "[REDACTED PERSON]'s email is [REDACTED EMAIL].")

    def test_process_anonymize(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.ANONYMIZE)
        self.assertEqual(result, "Fake Name's email is fake@email.com.")

    def test_process_ignore(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.IGNORE)
        self.assertEqual(result, text)

    def test_process_handles_overlapping_findings(self):
        """Ensure the processor correctly handles overlapping findings."""
        text = "Contact Jane Smith now."
        
        finding1 = Finding("Jane Smith", "PERSON", 8, 18, self.mock_person_recognizer)
        finding2 = Finding("Smith", "LAST_NAME", 13, 18, Mock()) 
        
        self.processor.get_findings = Mock(return_value=[finding1, finding2])
        
        result = self.processor.process(text, action=PiiAction.REDACT)
        self.assertEqual(result, "Contact [REDACTED PERSON] now.")

    def test_process_recursive_with_nested_structures(self):
        data = {
            "level1": "User is John Doe.",
            "level2_list": [
                "Contact at test@example.com",
                {"level3_user": "Another user is Jane Smith"}
            ]
        }
        result = self.processor.process_recursive(data, action=PiiAction.REDACT)
        expected = {
            "level1": "User is [REDACTED PERSON].",
            "level2_list": [
                "Contact at [REDACTED EMAIL]",
                {"level3_user": "Another user is [REDACTED PERSON]"}
            ]
        }
        self.assertEqual(result, expected)

    def test_process_recursive_with_tuple(self):
        data = ("User is John Doe.", "Email is test@example.com")
        result = self.processor.process_recursive(data, action=PiiAction.REDACT)
        self.assertEqual(result, ("User is [REDACTED PERSON].", "Email is [REDACTED EMAIL]"))

    def test_process_recursive_with_pydantic_like_object(self):
        pydantic_obj = MockPydanticModel(
            user="John Doe",
            message="Please use test@example.com"
        )
        result = self.processor.process_recursive(pydantic_obj, action=PiiAction.ANONYMIZE)

        self.assertIsInstance(result, MockPydanticModel)
        self.assertEqual(result.user, "Fake Name")
        # FIX: The expected result should be the full sentence with the email replaced.
        self.assertEqual(result.message, "Please use fake@email.com")

    def test_process_recursive_with_empty_structures(self):
        """Test that empty data structures are handled gracefully."""
        self.assertEqual(self.processor.process_recursive({}, PiiAction.REDACT), {})
        self.assertEqual(self.processor.process_recursive([], PiiAction.REDACT), [])
        self.assertEqual(self.processor.process_recursive((), PiiAction.REDACT), ())
        self.assertEqual(self.processor.process_recursive("", PiiAction.REDACT), "")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
