"""A recognizer for detecting credit card numbers."""
import re
from l8e_beam.recognizers.base import RegexRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

# Example 2: Recognizer with a custom validator (Luhn Check)
class CreditCardRecognizer(RegexRecognizer):
    """
    Detects credit card numbers using a regex and validates them with the Luhn algorithm.
    
    This helps to reduce false positives by checking if the number is mathematically valid.
    """
    name = DEFAULT_RECOGNIZERS.CREDIT_CARD.value
    regex = re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13})\b")

    def validate(self, text: str) -> bool:
        """Check credit card number against the Luhn algorithm."""
        digits = [int(d) for d in text if d.isdigit()]
        if len(digits) < 13:
            return False
        for i in range(len(digits) - 2, -1, -2):
            doubled = digits[i] * 2
            digits[i] = doubled if doubled < 10 else doubled - 9
        return sum(digits) % 10 == 0
    
    def anonymize(self, text: str) -> str:
        return self.faker.credit_card_number()
