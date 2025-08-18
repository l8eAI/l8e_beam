import re
from l8e_beam.recognizers.base import RegexRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS


# Example 1: Simple regex-only recognizer
class EmailRecognizer(RegexRecognizer):
    name = DEFAULT_RECOGNIZERS.EMAIL.value
    regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

    def anonymize(self, text: str) -> str:
        return self.faker.email()
