"""A recognizer for detecting organization names."""
from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

class OrgRecognizer(SpacyRecognizer):
    """Detects organization names using the 'ORG' entity from a spaCy model."""
    name = DEFAULT_RECOGNIZERS.ORGANIZATION.value
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.company()
