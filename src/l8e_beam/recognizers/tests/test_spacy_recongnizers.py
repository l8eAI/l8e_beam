# tests/recognizers/test_spacy_recognizers.py

import unittest
from unittest.mock import Mock, patch

from l8e_beam.recognizers.person import PersonRecognizer
from l8e_beam.recognizers.org import OrgRecognizer
from l8e_beam.recognizers.base import Finding

class TestSpacyRecognizers(unittest.TestCase):

    def setUp(self):
        """Set up a mock spaCy Doc object for testing."""
        self.mock_doc = Mock()
        
        # Create mock Span objects
        mock_person_span = Mock()
        mock_person_span.text = "John Doe"
        mock_person_span.label_ = "PERSON"
        mock_person_span.start_char = 10
        mock_person_span.end_char = 18

        mock_org_span = Mock()
        mock_org_span.text = "Acme Inc."
        mock_org_span.label_ = "ORG"
        mock_org_span.start_char = 25
        mock_org_span.end_char = 34

        self.mock_doc.ents = [mock_person_span, mock_org_span]

    def test_person_recognizer(self):
        recognizer = PersonRecognizer()
        findings = []
        recognizer.analyze(self.mock_doc, findings)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].text, "John Doe")
        self.assertEqual(findings[0].pii_type, "PERSON")
        self.assertEqual(findings[0].start, 10)
        
    def test_org_recognizer(self):
        recognizer = OrgRecognizer()
        findings = []
        recognizer.analyze(self.mock_doc, findings)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].text, "Acme Inc.")
        self.assertEqual(findings[0].pii_type, "ORG")
        self.assertEqual(findings[0].end, 34)

    @patch('l8e_beam.recognizers.base.Recognizer.faker')
    def test_person_anonymize(self, mock_faker):
        mock_faker.name.return_value = "Fake Name"
        recognizer = PersonRecognizer()
        self.assertEqual(recognizer.anonymize("John Doe"), "Fake Name")