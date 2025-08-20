"""A recognizer for detecting geopolitical entities (GPEs)."""
from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

class GpeRecognizer(SpacyRecognizer):
    """
    Detects geopolitical entities (e.g., countries, cities, states) using
    the 'GPE' entity from a spaCy model.
    """
    name = DEFAULT_RECOGNIZERS.GPE.value # Geopolitical Entity (countries, cities, states)
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.country()
