# src/l8e_beam/recognizers/__init__.py

"""
PII Recognizer System for l8e-beam.

This sub-package contains the pluggable system for detecting Personally
Identifiable Information (PII). It uses a hybrid approach with two main
types of recognizers:

1.  **`RegexRecognizer`**: For pattern-based detection (e.g., emails, phone numbers).
2.  **`SpacyRecognizer`**: For model-based, contextual detection (e.g., names, locations).

The system is designed to be extensible. Advanced users can create their
own custom recognizers by inheriting from these base classes.

The `PiiProcessor` is the engine that orchestrates all loaded recognizers
to find and process PII within text.
"""
