# src/l8e_beam/recognizers/pii_processor.py

"""
The core PII processing engine.

This module contains the `PiiProcessor` class, which is responsible for
orchestrating the entire PII detection and sanitization process. It manages
all the registered recognizers and applies the requested action (redact,
anonymize, or ignore) to the findings.
"""

from l8e_beam.enums import PiiAction, ModelType
# from .base import Finding, RegexRecognizer, SpacyRecognizer
from typing import List, Any
import spacy


class PiiProcessor:
    """
    Orchestrates all recognizers to find, sort, and process PII in text
    and other data structures.
    """
    def __init__(
        self,
        regex_recognizers: List, # List[RegexRecognizer]
        spacy_recognizers: List, # List[SpacyRecognizer]
        nlp: spacy.Language
    ):
        """
        Initializes the PiiProcessor.

        Args:
            regex_recognizers: A list of instantiated `RegexRecognizer` objects.
            spacy_recognizers: A list of instantiated `SpacyRecognizer` objects.
            nlp: A loaded spaCy language model.
        """
        self.regex_recognizers = regex_recognizers
        self.spacy_recognizers = spacy_recognizers
        self.nlp = nlp

    def get_findings(self, text: str) -> List: # List[Finding]
        """
        Finds all PII in a string by running all registered recognizers.

        This method optimizes the process by running the spaCy NLP model
        only once on the text, then passing the processed `Doc` object to all
        spaCy-based recognizers.

        Args:
            text: The input text to scan.

        Returns:
            A list of all `Finding` objects, consolidated from all recognizers.
        """
        findings = []
        
        # 1. Run all regex recognizers first
        for recognizer in self.regex_recognizers:
            recognizer.analyze(text, findings)
            
        # 2. Run spaCy NLP process ONCE
        doc = self.nlp(text)
        
        # 3. Run all spaCy recognizers on the processed doc
        for recognizer in self.spacy_recognizers:
            recognizer.analyze(doc, findings)
            
        return findings

    def process(self, text: str, action: PiiAction = PiiAction.REDACT) -> str:
        """
        Applies a PII action to a single string.

        It gets all findings, sorts them to handle overlaps correctly, and then
        rebuilds the string with the PII either redacted, anonymized, or ignored.

        Args:
            text: The input text.
            action: The action to perform on the PII.

        Returns:
            The processed string.
        """
        findings = self.get_findings(text)
        if not findings:
            return text

        findings.sort(key=lambda f: f.start)

        new_text_parts = []
        last_end = 0
        for finding in findings:
            if finding.start < last_end:
                continue

            new_text_parts.append(text[last_end:finding.start])

            # --- Main Logic Change Here ---
            replacement_text = ""
            if action == PiiAction.REDACT:
                replacement_text = f"[REDACTED {finding.pii_type}]"
            elif action == PiiAction.ANONYMIZE:
                # Use the recognizer stored in the finding to generate fake data
                replacement_text = finding.recognizer.anonymize(finding.text)
            elif action == PiiAction.IGNORE:
                replacement_text = finding.text
            
            new_text_parts.append(replacement_text)
            last_end = finding.end

        new_text_parts.append(text[last_end:])

        return "".join(new_text_parts)
    
    def process_recursive(self, data: Any, action: PiiAction) -> Any:
        """
        Recursively traverses data structures to process all string values.

        This method can handle nested dictionaries, lists, and tuples, as well
        as any object with a `.dict()` method (like Pydantic models).

        Args:
            data: The data structure to process.
            action: The PII action to apply.

        Returns:
            A new data structure of the same type with all strings processed.
        """
        if isinstance(data, str):
            return self.process(data, action)
        elif isinstance(data, dict):
            return {k: self.process_recursive(v, action) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_recursive(item, action) for item in data]
        # FIX: Added a condition to handle tuples
        elif isinstance(data, tuple):
            return tuple(self.process_recursive(item, action) for item in data)
        elif hasattr(data, 'dict') and callable(getattr(data, 'dict')):
            # Convert to a dict and process its values
            sanitized_dict = self.process_recursive(data.dict(), action)
            # Get the original class of the object
            original_class = type(data)
            try:
                # Re-create the object from the sanitized dict
                return original_class(**sanitized_dict)
            except TypeError:
                # Fallback for objects that can't be re-instantiated this way
                return sanitized_dict
        else:
            # For any other data type, return it unchanged
            return data