# tests/recognizers/test_regex_recognizers.py

import unittest
from unittest.mock import patch

from l8e_beam.recognizers.email import EmailRecognizer
from l8e_beam.recognizers.phone import PhoneRecognizer
from l8e_beam.recognizers.credit_card import CreditCardRecognizer
from l8e_beam.recognizers.base import Finding

class TestRegexRecognizers(unittest.TestCase):

    def test_email_recognizer(self):
        recognizer = EmailRecognizer()
        text = "Contact us at test@example.com for more info."
        findings = []
        recognizer.analyze(text, findings)
        
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].text, "test@example.com")
        self.assertEqual(findings[0].pii_type, "EMAIL")

    def test_phone_recognizer(self):
        recognizer = PhoneRecognizer()
        text = "Call me at 555-867-5309 anytime."
        findings = []
        recognizer.analyze(text, findings)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].text, "555-867-5309")
        self.assertEqual(findings[0].pii_type, "PHONE")

    def test_credit_card_recognizer_validation(self):
        recognizer = CreditCardRecognizer()
        
        # Test a valid VISA number
        valid_card = "4242424242424242"
        self.assertTrue(recognizer.validate(valid_card))
        
        invalid_card = "4992739871634640"
        self.assertFalse(recognizer.validate(invalid_card))

    @patch('l8e_beam.recognizers.base.Recognizer.faker')
    def test_anonymize_methods(self, mock_faker):
        """Test the anonymize methods with a mocked Faker instance."""
        mock_faker.email.return_value = "fake@email.com"
        email_recognizer = EmailRecognizer()
        self.assertEqual(email_recognizer.anonymize("test"), "fake@email.com")