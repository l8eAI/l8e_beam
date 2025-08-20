"""A recognizer for detecting phone numbers."""
import re
from l8e_beam.recognizers.base import RegexRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

# Example 3: Recognizer with custom anonymization using Faker
class PhoneRecognizer(RegexRecognizer):
    """Detects common phone number formats using a regular expression."""
    name = DEFAULT_RECOGNIZERS.PHONE.value
    regex = re.compile(r"(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
    def anonymize(self, text: str) -> str:
        return self.faker.phone_number()
