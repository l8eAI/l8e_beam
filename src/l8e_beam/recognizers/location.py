"""A recognizer for detecting non-GPE locations."""
from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS


class LocRecognizer(SpacyRecognizer):
    """
    Detects non-GPE locations (e.g., mountains, bodies of water) using
    the 'LOC' entity from a spaCy model.
    """
    name = DEFAULT_RECOGNIZERS.LOCATION.value # Location (non-GPE locations, mountains, bodies of water)
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.address()
