# src/l8e_beam/__init__.py

"""
# l8e-beam: A Python SDK for PII Redaction and Anonymization

This package provides a simple and powerful way to protect Personally
Identifiable Information (PII) in data before it's used in AI agent
contexts or other sensitive applications.

## 🚀 Core Features

- **PII Detection**: Identifies PII such as names, emails, and phone numbers.
- **Multiple Actions**: Supports redaction (e.g., `[PERSON]`) and anonymization (e.g., "Jane Doe" -> "Markus Kramer").
- **Flexible Models**: Choose between a fast, general-purpose model (`SM`) and a more accurate transformer model (`TRF`).
- **Extensible**: Easily add custom PII recognizers or disable default ones.
- **Easy Integration**: Provides both a simple decorator and a direct API for fine-grained control.

## 🛠️ Two Main Interfaces

This library offers two primary ways to handle PII:

1.  **The Decorator (`@redact_pii`)**
    The easiest method for "set-and-forget" PII protection on all inputs and outputs of a function.
    Best for simple, comprehensive coverage.

2.  **The Direct API (`sanitize_pii`)**
    A flexible function for advanced use cases, allowing you to process specific data blobs,
    add custom rules, or disable default ones on the fly. Best for complex or dynamic workflows.

## ✅ Quickstart Example

```python
from l8e_beam import redact_pii, PiiAction

@redact_pii(action=PiiAction.REDACT)
def process_report(report: dict):
    # The 'report' dictionary is already sanitized
    # before this code block is executed.
    return report

incident_report = {"details": "Client Susan Miller reported an outage in Berlin."}

# The decorator will process the input and the return value
redacted_report = process_report(incident_report)

# Output: {'details': 'Client [REDACTED PERSON] reported an outage in [REDACTED GPE].'}
"""
from l8e_beam.decorator import redact_pii
from l8e_beam.enums import ModelType, PiiAction
from l8e_beam.api import sanitize_pii
from l8e_beam.recognizers.base import Finding, RegexRecognizer, SpacyRecognizer
from l8e_beam.recognizers.enums import DEFAULT_RECOGNIZERS

__all__ = [
"redact_pii",
"sanitize_pii",
"ModelType",
"PiiAction",
"DEFAULT_RECOGNIZERS",
"RegexRecognizer",
"SpacyRecognizer",
"Finding"
]
