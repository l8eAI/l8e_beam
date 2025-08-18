from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

class OrgRecognizer(SpacyRecognizer):
    name = DEFAULT_RECOGNIZERS.ORGANIZATION.value
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.company()
