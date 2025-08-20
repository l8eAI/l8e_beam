from enum import Enum

class DEFAULT_RECOGNIZERS(Enum):
    """
    Enum to define the default recognizers available in the library.
    
    This is used in the `sanitize_pii` function to disable specific recognizers.
    
    Attributes:
        CREDIT_CARD: Recognizer for credit card numbers.
        EMAIL: Recognizer for email addresses.
        PHONE: Recognizer for phone numbers.
        PERSON: Recognizer for people's names.
        LOCATION: Recognizer for non-geopolitical locations.
        ORGANIZATION: Recognizer for company and organization names.
        GPE: Recognizer for geopolitical entities (countries, cities, states).
        DATE: Recognizer for dates.
    """
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