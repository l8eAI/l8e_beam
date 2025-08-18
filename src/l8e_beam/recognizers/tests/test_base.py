# tests/recognizers/test_base.py

import unittest
from l8e_beam.recognizers.base import Finding, Recognizer

class MockRecognizer(Recognizer):
    name = "MOCK"
    def analyze(self, text, findings): pass

class TestFinding(unittest.TestCase):
    def test_finding_creation(self):
        """Test that a Finding object can be created with correct attributes."""
        recognizer_instance = MockRecognizer()
        finding = Finding(
            text="test",
            pii_type="MOCK",
            start=0,
            end=4,
            recognizer=recognizer_instance,
            score=0.9
        )
        self.assertEqual(finding.text, "test")
        self.assertEqual(finding.pii_type, "MOCK")
        self.assertEqual(finding.recognizer, recognizer_instance)
        self.assertEqual(finding.score, 0.9)

if __name__ == '__main__':
    unittest.main()