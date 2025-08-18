import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from spacy.tokens import Doc
import faker
# --- Component 1: The Finding Dataclass ---
@dataclass
class Finding:
    """A dataclass to hold the results of a PII detection."""
    text: str
    pii_type: str
    start: int
    end: int
    recognizer: 'Recognizer' # Reference to the recognizer that found this PII
    score: float = 0.75 # Default score for regex matches


class Recognizer(ABC):
    """A generic base class for all PII recognizers."""
    faker = faker.Faker()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyze(self, text: str, findings: List[Finding]):
        """The main analysis method to be implemented by subclasses."""
        pass

    def anonymize(self, text: str) -> str:
        return f"[REDACTED {self.name}]"

class RegexRecognizer(Recognizer):
    @property
    @abstractmethod
    def regex(self) -> re.Pattern:
        pass

    def validate(self, text: str) -> bool:
        return True

    def analyze(self, text: str, findings: List[Finding]):
        for match in self.regex.finditer(text):
            matched_text = match.group(0)
            if self.validate(matched_text):
                findings.append(Finding(
                    text=matched_text,
                    pii_type=self.name,
                    start=match.start(),
                    end=match.end(),
                    score=0.85, # Higher confidence for validated regex
                    recognizer=self
                ))

class SpacyRecognizer(Recognizer):
    """
    Base class for recognizers that use a spaCy NER model.
    It operates on a pre-processed spaCy Doc object for efficiency.
    """
    @property
    @abstractmethod
    def label(self) -> str:
        """The spaCy entity label to look for (e.g., 'PERSON')."""
        pass
    
    # Redefine analyze to accept a spaCy Doc object
    def analyze(self, doc: Doc, findings: List[Finding]):
        for ent in doc.ents:
            if ent.label_ == self.label:
                findings.append(Finding(
                    text=ent.text,
                    pii_type=self.name,
                    start=ent.start_char,
                    end=ent.end_char,
                    score=0.90, # Higher confidence for spaCy entities
                    recognizer=self
                ))