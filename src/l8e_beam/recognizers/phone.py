import re
from .base import RegexRecognizer

# Example 3: Recognizer with custom anonymization using Faker
class PhoneRecognizer(RegexRecognizer):
    name = "PHONE"
    regex = re.compile(r"(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
    def anonymize(self, text: str) -> str:
        return self.faker.phone_number()
