from .base import SpacyRecognizer

class DateRecognizer(SpacyRecognizer):
    name = "DATE"
    label = "DATE"

    def anonymize(self, text: str) -> str:
        return self.faker.date()
