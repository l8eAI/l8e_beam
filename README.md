# l8e-beam 빔

**l8e-beam** is a Python SDK that provides simple, powerful decorators for preparing data for AI agent contexts.  
Its primary features are robust **PII (Personally Identifiable Information) redaction** and **structured audit logging**.

It is designed to be a simple, *drop-in* solution for developers who need to ensure data privacy and maintain traceability before passing data to language models or other AI systems.

---

## Installation

You can install **l8e-beam** directly from PyPI:

```bash
pip install l8e-beam
````

---

## Usage

The SDK provides decorators to easily add functionality to your data processing functions.

### PII Redaction

The core feature is the `@redact_pii` decorator, which can be configured to use different models depending on your needs for speed versus accuracy.

---

#### Basic Usage (Fast Model)

By default, the decorator uses a small, fast model (`ModelType.SM`) that is suitable for general-purpose redaction.

```python
from pii_redactor import redact_pii, ModelType

@redact_pii()  # Using the default ModelType.SM
def process_user_query(query_data: dict):
    # The 'query_data' dictionary will have all PII in its values redacted
    # before this code runs.
    print("Inside function:", query_data)
    return query_data

user_info = {
    "user": "John Smith",
    "query": "Book a flight from New York to London for me."
}

redacted_info = process_user_query(user_info)
# redacted_info will be:
# {'user': '[REDACTED]', 'query': 'Book a flight from [REDACTED] to [REDACTED] for me.'}
```

---

#### High-Accuracy Usage (Transformer Model)

For text that is more complex or requires higher accuracy, you can specify the transformer model (`ModelType.TRF`).

```python
from pii_redactor import redact_pii, ModelType

@redact_pii(model=ModelType.TRF)
def process_complex_document(document: dict):
    # This will use the more powerful transformer model for redaction.
    return document

document = {
    "author": "Paris Hilton",
    "destination": "Paris, France",
    "company": "Hilton Hotels" 
}

redacted_document = process_complex_document(document)
# redacted_document will be:
# {'author': '[REDACTED]', 'destination': '[REDACTED], [REDACTED]', 'company': '[REDACTED]'}
```

---

### Audit Logging (Work in Progress)

The `@log_audit` decorator provides a simple way to create a structured audit trail for any function.
It logs the function's inputs, outputs, and a timestamp as a JSON object, which is ideal for monitoring and debugging AI agent interactions.


---

## Model Selection

You can choose the model that best fits your use case by passing a `ModelType` enum member to the decorator.

| Model           | ModelType Member | Accuracy (F-Score) | Size     | Speed | Use Case                                              |
| --------------- | ---------------- | ------------------ | -------- | ----- | ----------------------------------------------------- |
| **Small**       | `ModelType.SM`   | \~0.86             | \~12 MB  | Fast  | General purpose, high-throughput tasks.               |
| **Transformer** | `ModelType.TRF`  | >0.90              | \~400 MB | Slow  | High-accuracy tasks, complex sentences, critical PII. |

The **F-score** represents a balance between precision (how many entities found were correct) and recall (how many of the total entities were found). A higher score is better.

---

## Design Decisions

### Why Dictionary Keys Are Not Redacted

The `@redact_pii` decorator is designed to recursively redact PII found in string **values** within any data structure (lists, dictionaries, etc.), but it intentionally does **not** redact dictionary keys.

This is a critical design choice to preserve the structural integrity of the data.
Programs that receive the redacted data often rely on specific key names (e.g., `"user"`, `"location"`, `"id"`) to function correctly.

Redacting these keys would likely break the downstream application.
The primary goal is to protect the sensitive information contained in the values while ensuring the data remains usable.

---

## Running Tests

To run the test suite for this package:

1. Clone the repository.

2. Install the development dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run pytest:

   ```bash
   pytest
   ```

```
