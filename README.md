# l8e-beam 빔

**l8e-beam** is a Python SDK that provides simple, powerful tools for preparing data for AI agent contexts.  
Its primary features are robust **PII (Personally Identifiable Information) protection** through **redaction** and **anonymization**.

It is designed to be a flexible solution for developers who need to ensure **data privacy** before passing data to language models or other AI systems.

---

## 📦 Installation

This package is not yet available on the Python Package Index (PyPI) and must be installed from the source code.

### Option 1: Editable Install (for Development)

If you are actively developing the package, an "editable" install is recommended. This allows your changes to be reflected immediately without needing to reinstall.

1. Clone the repository.
2. Run the following command from the project's root directory:

```
pip install -e .
```

### Option 2: Standard Install (from Source)

This method builds the package into a wheel file and then installs it, which is closer to how a user would install it from PyPI.

#### Step 1: Build the Package
First, ensure you have the build tool installed (pip install build). Then, run the build command from the project root:
```
python -m build
```

This will create a dist/ directory containing the installable wheel file (e.g., l8e_beam-0.6.0-py3-none-any.whl).

#### Step 2: Install the Wheel File
Install the package using the wheel file from the dist/ directory:
```
pip install dist/l8e_beam-*.whl
```



---

## 🚀 Two Ways to Sanitize PII

This library offers two powerful methods for handling PII, catering to different needs:

* **1. The Decorator (`@redact_pii`)**
  The easiest way to protect data. Simply add it to your functions for automatic, "set-and-forget" PII protection on all inputs and outputs.
  ✅ Best for **simple, comprehensive coverage**.

* **2. The Direct API (`sanitize_pii`)**
  A flexible function for advanced use cases. It gives you granular control to process specific data blobs, add custom rules, or disable default ones on the fly.
  ✅ Best for **complex, dynamic, or non-decorator workflows**.

---

## ✅ Simple Usage: The `@redact_pii` Decorator

The decorator is the quickest way to secure a function.

### PII Protection Actions

You can control the behavior by setting the `action` parameter.

#### 1. Redaction (Default)

**Redaction** replaces detected PII with a placeholder label.

```python
from l8e_beam import redact_pii, PiiAction

@redact_pii(action=PiiAction.REDACT) 
def process_incident_report(report: dict):
    return report

incident_report = {"details": "Client Susan Miller reported an outage in Berlin."}
redacted_report = process_incident_report(incident_report)
# {'details': 'Client [PERSON] reported an outage in [GPE].'}
```

---

#### 2. Anonymization

**Anonymization** replaces detected PII with realistic-looking **fake data**.

```python
from l8e_beam import redact_pii, PiiAction

@redact_pii(action=PiiAction.ANONYMIZE)
def create_test_user(profile: dict):
    return profile

user_profile = {"name": "John Doe", "email": "john.doe@example.com"}
anonymized_profile = create_test_user(user_profile)
# {'name': 'Mary Smith', 'email': 'robertholmes@example.org'}
```

---

## 🛠️ Advanced Usage: The `sanitize_pii` API

For full control, use the `sanitize_pii` function directly. This is ideal when you need to process a piece of data dynamically or apply custom rules.

```python
from l8e_beam import sanitize_pii, PiiAction

data = "Send the report to jane.doe@example.com"
processed_data = sanitize_pii(data, action=PiiAction.ANONYMIZE)
# 'Send the report to sarahjones@example.com'
```

### Disabling Default Recognizers

You can easily disable default recognizers by passing a list of `DEFAULT_RECOGNIZERS` enums.
This is useful for preventing certain PII types from being processed.

```python
from l8e_beam import sanitize_pii, PiiAction, DEFAULT_RECOGNIZERS

report = "Contact support at help@example.com about the issue with John Smith."

# Redact the person's name, but leave the email address untouched
processed_report = sanitize_pii(
    report,
    action=PiiAction.REDACT,
    disabled_recognizers=[DEFAULT_RECOGNIZERS.EMAIL]
)
# 'Contact support at help@example.com about the issue with [PERSON].'
```

### Adding a Custom Recognizer

The most powerful feature of the API is the ability to add your own recognizers on the fly.

```python
import re
import uuid
from l8e_beam import sanitize_pii, RegexRecognizer, PiiAction

# 1. Define your custom recognizer class
class UuidRecognizer(RegexRecognizer):
    name = "UUID"
    regex = re.compile(r"[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}", re.I)

# 2. Create an instance of it
my_uuid_recognizer = UuidRecognizer()

log_entry = f"Request failed for user_id: {uuid.uuid4()}"

# 3. Pass it to the API
processed_log = sanitize_pii(
    log_entry,
    action=PiiAction.REDACT,
    custom_recognizers=[my_uuid_recognizer]
)
# 'Request failed for user_id: [UUID]'
```

---

## 🕵️ What Information is Handled?

The system uses a **hybrid approach** of machine learning models and regular expressions.

### Controllable Default Recognizers

You can disable any of the following recognizers using the `disabled_recognizers` parameter and the `DEFAULT_RECOGNIZERS` enum:

* `EMAIL`, `PHONE`, `CREDIT_CARD` (from Regex)
* `PERSON`, `ORG`, `GPE`, `LOC`, `DATE` (from spaCy NER)

### Validation for Precision

For certain PII types like credit cards, a validation step (e.g., the **Luhn algorithm**) is performed after detection.
This reduces false positives and increases accuracy.

---

## ⚡ Model Selection

For NER-based detection, you can choose a model that best fits your use case.

| Model           | ModelType Member | Accuracy | Size     | Speed | Best For                    |
| --------------- | ---------------- | -------- | -------- | ----- | --------------------------- |
| **Small**       | `ModelType.SM`   | \~0.86   | \~12 MB  | Fast  | General-purpose tasks       |
| **Transformer** | `ModelType.TRF`  | >0.90    | \~400 MB | Slow  | High-accuracy, complex text |

```python
# The model can be specified in both the decorator and the direct API
from l8e_beam import sanitize_pii, ModelType
processed_text = sanitize_pii(text, model=ModelType.TRF)
```

---
## 🔄 Working with Data Structures

The l8e-beam processor can recursively traverse and sanitize nested data structures.

### Supported Types

- Primitives: str
- Collections: dict, list, tuple

#### Automatic Pydantic & Custom Object Support

The processor will automatically handle any object that has a .dict() method, such as a Pydantic model.
It converts the object to a dictionary, sanitizes its values, and then reconstructs the original object, preserving its type.
```
from pydantic import BaseModel
from l8e_beam import redact_pii, PiiAction

class UserContext(BaseModel):
    user_id: str
    full_name: str

@redact_pii(action=PiiAction.REDACT)
def process_context(context: UserContext):
    # The 'context' object is sanitized before this code runs,
    # but it remains a UserContext instance.
    return context

user_data = UserContext(user_id="abc-123", full_name="Jane Doe")
processed_context = process_context(user_data)

# The returned object is still a UserContext, with sanitized data:
# UserContext(user_id='abc-123', full_name='[PERSON]')
```
---

## 🧪 Running Tests

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:

   ```bash
   pytest
   ```

---

## 📌 Roadmap

* [x] **PII Redaction & Anonymization**
* [x] **Hybrid Detection** (NER + Regex) with Validation
* [x] **Decorator & Advanced API** Interfaces
* [ ] **Audit Logging**: Add a `@log_audit` decorator.
* [ ] **Granular Control**: Allow specifying which PII types to *enable*, not just disable.

---

## 🤝 Contributing

Contributions are welcome! To set up a development environment, use the `build.sh` script:

```bash
chmod +x build.sh
./build.sh
```

---

## 📄 License

MIT License © 2025 **l8e**
