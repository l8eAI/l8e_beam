import re
from .base import RegexRecognizer

# Example 1: Simple regex-only recognizer
class EmailRecognizer(RegexRecognizer):
    name = "EMAIL"
    regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

    def anonymize(self, text: str) -> str:
        return self.faker.email()
