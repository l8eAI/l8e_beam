# tests/test_pii_processor.py

import unittest
from unittest.mock import Mock, MagicMock

from l8e_beam.recognizers.pii_processor import PiiProcessor
from l8e_beam.enums import PiiAction
from l8e_beam.recognizers.base import Finding

class TestPiiProcessor(unittest.TestCase):

    def setUp(self):
        """Set up a PiiProcessor with mock recognizers."""
        self.mock_regex_recognizer = Mock()
        self.mock_spacy_recognizer = Mock()

        # Mock the analyze methods to add specific findings
        def mock_regex_analyze(text, findings):
            if "test@example.com" in text:
                finding = Finding("test@example.com", "EMAIL", 20, 36, self.mock_regex_recognizer, 0.9)
                findings.append(finding)
        
        def mock_spacy_analyze(doc, findings):
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    finding = Finding(ent.text, "PERSON", ent.start_char, ent.end_char, self.mock_spacy_recognizer, 0.9)
                    findings.append(finding)
        
        self.mock_regex_recognizer.analyze = mock_regex_analyze
        self.mock_spacy_recognizer.analyze = mock_spacy_analyze

        # Mock the anonymize methods
        self.mock_regex_recognizer.anonymize.return_value = "fake@email.com"
        self.mock_spacy_recognizer.anonymize.return_value = "Fake Name"

        # Mock spaCy nlp object
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_ent = MagicMock(text="John Doe", label_="PERSON", start_char=0, end_char=8)
        mock_doc.ents = [mock_ent]
        mock_nlp.return_value = mock_doc

        self.processor = PiiProcessor(
            regex_recognizers=[self.mock_regex_recognizer],
            spacy_recognizers=[self.mock_spacy_recognizer],
            nlp=mock_nlp
        )

    def test_process_redact(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.REDACT)
        expected = "[REDACTED PERSON]'s email is [REDACTED EMAIL]."
        self.assertEqual(result, expected)

    def test_process_anonymize(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.ANONYMIZE)
        expected = "Fake Name's email is fake@email.com."
        self.assertEqual(result, expected)

    def test_process_ignore(self):
        text = "John Doe's email is test@example.com."
        result = self.processor.process(text, action=PiiAction.IGNORE)
        self.assertEqual(result, text)

    def test_process_recursive(self):
        data = {
            "user": "John Doe's email is test@example.com.",
            "ids": [1, 2, 3]
        }
        result = self.processor.process_recursive(data, action=PiiAction.REDACT)
        expected = {
            "user": "[REDACTED PERSON]'s email is [REDACTED EMAIL].",
            "ids": [1, 2, 3]
        }
        self.assertEqual(result, expected)