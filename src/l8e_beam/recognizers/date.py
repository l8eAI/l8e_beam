"""A recognizer for detecting dates."""
from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS


class DateRecognizer(SpacyRecognizer):
    """Detects dates using the 'DATE' entity from a spaCy model."""
    name = DEFAULT_RECOGNIZERS.DATE.value
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.date()
