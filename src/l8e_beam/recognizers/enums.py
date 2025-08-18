from enum import Enum

class DEFAULT_RECOGNIZERS(Enum):
    """Enum to define the default recognizers available in the library."""
    # Regex-based
    CREDIT_CARD = "CREDIT_CARD"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    
    # spaCy-based
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ORGANIZATION = "ORG"
    GPE = "GPE" # Geopolitical Entity (countries, cities, states)
    DATE = "DATE"