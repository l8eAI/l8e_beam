from l8e_beam.recognizers.base import SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

class GpeRecognizer(SpacyRecognizer):
    name = DEFAULT_RECOGNIZERS.GPE.value # Geopolitical Entity (countries, cities, states)
    label = name

    def anonymize(self, text: str) -> str:
        return self.faker.country()
