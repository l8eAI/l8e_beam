from .base import SpacyRecognizer

class OrgRecognizer(SpacyRecognizer):
    name = "ORG"
    label = "ORG"

    def anonymize(self, text: str) -> str:
        return self.faker.company()
