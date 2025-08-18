from .base import SpacyRecognizer

class LocRecognizer(SpacyRecognizer):
    name = "LOC" # Location (non-GPE locations, mountains, bodies of water)
    label = "LOC"

    def anonymize(self, text: str) -> str:
        return self.faker.address()
