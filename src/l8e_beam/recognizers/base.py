# src/l8e_beam/recognizers/base.py

"""
Base classes for all PII (Personally Identifiable Information) recognizers.

This module provides the foundational components for creating new recognizers.
To create a custom recognizer, you should inherit from one of these base classes:

- `Recognizer`: The generic abstract base class for all recognizers.
- `RegexRecognizer`: A base class for recognizers that use regular expressions.
- `SpacyRecognizer`: A base class for recognizers that use spaCy's NER models.

It also defines the `Finding` dataclass, which is used to standardize the
output of all recognizer `analyze` methods.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from spacy.tokens import Doc
import faker
# --- Component 1: The Finding Dataclass ---
@dataclass
class Finding:
    """
    A dataclass to hold the results of a PII detection.
    
    This object standardizes the information returned by any recognizer.

    Attributes:
        text (str): The actual text that was identified as PII.
        pii_type (str): The type of PII found (e.g., 'EMAIL', 'PERSON').
        start (int): The starting character index of the PII in the original text.
        end (int): The ending character index of the PII in the original text.
        recognizer (Recognizer): A reference to the recognizer instance that found this PII.
        score (float): A confidence score for the finding (0.0 to 1.0).
    """
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
        """The unique name of the recognizer (e.g., 'EMAIL')."""
        pass

    @abstractmethod
    def analyze(self, text: str, findings: List[Finding]):
        """The main analysis method to be implemented by subclasses."""
        pass

    def anonymize(self, text: str) -> str:
        """
        Defines how to generate fake data for this PII type.
        
        By default, it returns a standard redaction placeholder. Subclasses
        should override this to provide more specific anonymization logic
        (e.g., generating a fake email address).
        """
        return f"[REDACTED {self.name}]"

class RegexRecognizer(Recognizer):
    """
    An abstract base class for recognizers that use regular expressions.

    Subclasses must implement the `regex` property.
    """
    @property
    @abstractmethod
    def regex(self) -> re.Pattern:
        """The compiled regular expression pattern to search for."""
        pass

    def validate(self, text: str) -> bool:
        """
        An optional validation step after a regex match.

        This method can be overridden to perform additional checks (like a checksum)
        to reduce false positives. By default, it returns `True`.

        Returns:
            `True` if the match is valid, `False` otherwise.
        """
        return True

    def analyze(self, text: str, findings: List[Finding]):
        """
        Scans the text for matches using the `regex` pattern.
        
        For each match, it calls the `validate` method before creating a `Finding`.
        """
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
    An abstract base class for recognizers that use a spaCy NER model.

    This class operates on a pre-processed spaCy `Doc` object for efficiency,
    as it avoids running the NLP model multiple times. Subclasses must
    implement the `label` property.
    """
    @property
    @abstractmethod
    def label(self) -> str:
        """The spaCy entity label to look for (e.g., 'PERSON')."""
        pass
    
    # Redefine analyze to accept a spaCy Doc object
    def analyze(self, doc: Doc, findings: List[Finding]):
        """
        Scans a spaCy `Doc` object for entities matching the `label`.
        """
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