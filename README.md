# l8e-beam 빔

**l8e-beam** is a Python SDK that provides simple, powerful decorators for preparing data for AI agent contexts.  
Its primary features are robust **PII (Personally Identifiable Information) protection** through **redaction** and **anonymization**.

It is designed to be a simple, *drop-in* solution for developers who need to ensure **data privacy** before passing data to language models or other AI systems.

---

## 📦 Installation

You can install `l8e-beam` directly from the Python Package Index (PyPI):

```bash
pip install l8e-beam
````

Alternatively, to install in editable mode for development:

```bash
pip install -e .
```

---

## 🚀 Usage

The SDK's core feature is the `@redact_pii` decorator, which automatically processes the inputs and outputs of any function to handle sensitive data.

### 🔒 PII Protection Actions

You can control the PII handling behavior by setting the `action` parameter in the decorator.

#### 1. Redaction (Default)

**Redaction** replaces detected PII with a placeholder label, indicating the *type* of information that was removed.
Useful for completely scrubbing sensitive data.

```python
from l8e_beam import redact_pii, PiiAction

@redact_pii(action=PiiAction.REDACT) 
def process_incident_report(report: dict):
    # 'report' has its PII values replaced with placeholders.
    print("Inside function:", report)
    return report

incident_report = {
    "details": "Client Susan Miller reported an outage in Berlin.",
    "company": "affiliated with Acme Corporation"
}

redacted_report = process_incident_report(incident_report)
# {'details': 'Client [PERSON] reported an outage in [GPE].', 
#  'company': 'affiliated with [ORG]'}
```

---

#### 2. Anonymization

**Anonymization** replaces detected PII with realistic-looking **fake data**.
This is useful when you need to preserve the structure and format of the original data for testing or demonstrations.

```python
from l8e_beam import redact_pii, PiiAction

@redact_pii(action=PiiAction.ANONYMIZE)
def create_test_user(profile: dict):
    # 'profile' has its PII values replaced with fake data.
    print("Inside function:", profile)
    return profile

user_profile = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "555-867-5309"
}

anonymized_profile = create_test_user(user_profile)
# {'name': 'Mary Smith', 
#  'email': 'robertholmes@example.org', 
#  'phone': '(555) 321-9876'}
```

---

## 🕵️ What Information is Handled?

The decorator uses a **hybrid approach**, combining machine learning models and regular expressions to detect a wide range of PII.

### spaCy-Based Entities (NER)

Powered by **spaCy’s Named Entity Recognition (NER)**, ideal for contextual information:

* **PERSON**: Names of people (e.g., `John Smith`)
* **ORG**: Companies, agencies, institutions (e.g., `Google`, `Acme Corp`)
* **GPE**: Countries, cities, states (e.g., `Germany`, `London`)
* **LOC**: Non-GPE locations, mountains, water bodies (e.g., `Mount Everest`)

### Pattern-Based Entities (Regex)

Powered by **regular expressions**, ideal for well-defined formats:

* **EMAIL**: Email addresses
* **PHONE**: Phone numbers
* **CREDIT\_CARD**: Common credit card numbers

---

## ✨ How It Works: Hybrid Detection and Validation

`l8e-beam` uses a **robust, multi-stage process** to ensure both broad coverage and high accuracy in PII detection.

* **Hybrid Detection**: The system first uses a combination of methods to identify potential PII:

  * **spaCy NER**: For contextual data like names and locations.
  * **Regular Expressions**: For structured data like email addresses and phone numbers.

* **Validation for Precision**: For certain sensitive data types, detection is followed by a **validation step** to prevent false positives.

  * Example: When a number matching a credit card format is found, it is checked against the **Luhn algorithm**.
  * Only if the number passes this mathematical check is it flagged as PII.
    ✅ This significantly increases precision by ensuring random numbers aren't mistakenly redacted.

---

## ⚡ Model Selection

For NER-based detection, you can choose a model that best fits your use case for **speed vs. accuracy**.

| Model           | ModelType Member | Accuracy (F-Score) | Size     | Speed | Best For                               |
| --------------- | ---------------- | ------------------ | -------- | ----- | -------------------------------------- |
| **Small**       | `ModelType.SM`   | \~0.86             | \~12 MB  | Fast  | General-purpose, high-throughput tasks |
| **Transformer** | `ModelType.TRF`  | >0.90              | \~400 MB | Slow  | High-accuracy tasks, complex sentences |

🔹 The **F-score** balances **precision** (correct entities) and **recall** (entities found). A higher score is better.

```python
from l8e_beam import redact_pii, ModelType, PiiAction

# Use the larger, more accurate model for sensitive documents
@redact_pii(model=ModelType.TRF, action=PiiAction.REDACT)
def process_legal_document(document_text: str):
    return document_text
```

---

## 🧪 Running Tests

To run the test suite:

1. Clone the repository.
2. Install development dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run pytest:

   ```bash
   pytest
   ```

---

## 📌 Roadmap

* [x] **PII Redaction**: Replace PII with placeholders.
* [x] **PII Anonymization**: Replace PII with realistic fake data.
* [x] **Hybrid Detection**: Combine spaCy (NER) and Regex recognizers.
* [ ] **Audit Logging**: Add a `@log_audit` decorator for structured JSON logging.
* [ ] **Granular Control**: Allow users to specify exactly which PII types to handle.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

To set up a development environment, use the `build.sh` script, which will download the required spaCy models, run tests, and build the package:

```bash
chmod +x build.sh
./build.sh
```

---

## 📄 License

MIT License © 2025 **l8e**
