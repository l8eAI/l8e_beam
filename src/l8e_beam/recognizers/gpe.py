from .base import SpacyRecognizer

class GpeRecognizer(SpacyRecognizer):
    name = "GPE" # Geopolitical Entity (countries, cities, states)
    label = "GPE"

    def anonymize(self, text: str) -> str:
        return self.faker.country()
