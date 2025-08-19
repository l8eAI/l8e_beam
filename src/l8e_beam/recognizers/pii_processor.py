from l8e_beam.enums import PiiAction, ModelType
# from .base import Finding, RegexRecognizer, SpacyRecognizer
from typing import List, Any
import spacy


class PiiProcessor:
    def __init__(
        self,
        regex_recognizers: List, # List[RegexRecognizer]
        spacy_recognizers: List, # List[SpacyRecognizer]
        nlp: spacy.Language
    ):
        self.regex_recognizers = regex_recognizers
        self.spacy_recognizers = spacy_recognizers
        self.nlp = nlp

    def get_findings(self, text: str) -> List: # List[Finding]
        """
        Orchestrates all recognizers to find PII in the text.

        This method:
        1. Runs all regex-based recognizers.
        2. Runs the spaCy NLP model once for efficiency.
        3. Runs all spaCy-based recognizers on the processed text.
        4. Returns a single, consolidated list of all findings.
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
        Finds and processes all PII in a string based on the specified action.

        Args:
            text (str): The input text.
            action (PiiAction): The action to perform (REDACT or ANONYMIZE).
                                Defaults to REDACT.
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
        Recursively traverses data structures (dicts, lists, tuples) to process strings.
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