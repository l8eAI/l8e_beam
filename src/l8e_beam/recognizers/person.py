from .base import SpacyRecognizer

class PersonRecognizer(SpacyRecognizer):
    name = "PERSON"
    label = "PERSON"
    
    def anonymize(self, text: str) -> str:
        return self.faker.name()
