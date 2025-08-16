# l8e-beam 빔

**l8e-beam** is a Python SDK that provides simple, powerful decorators for preparing data for AI agent contexts.  
Its primary features are robust **PII (Personally Identifiable Information) redaction** and **structured audit logging**.

It is designed to be a simple, *drop-in* solution for developers who need to ensure **data privacy** and **maintain traceability** before passing data to language models or other AI systems.

---

## 📦 Installation

Installation
Option 1: Install from PyPI

You can install l8e-beam directly from the Python Package Index (PyPI) once it has been published.
```
pip install l8e-beam
```

Option 2: Build and Install Locally

If you are developing the package or want to install it directly from the source code, you can build it locally.

1. Install Build Tools:
First, ensure you have the necessary build tools installed.
```
pip install build
```

2. Build the Package:
Run the build command from the root of the project directory (l8e-beam/).
```
python -m build
```
This command will create a dist/ directory containing the installable package files (a .whl wheel file and a .tar.gz source archive).

3. Install the Local Package:
You can now install the package using pip.
```
pip install dist/*.whl
```

---

## 🚀 Usage

The SDK provides decorators to easily add functionality to your data processing functions.

### 🔒 PII Redaction

The core feature is the `@redact_pii` decorator, which can be configured to use different models depending on your needs for **speed vs accuracy**.

---

#### ✅ Basic Usage (Fast Model)

By default, the decorator uses a small, fast model (`ModelType.SM`) suitable for **general-purpose redaction**.

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
# {'user': '[REDACTED]', 'query': 'Book a flight from [REDACTED] to [REDACTED] for me.'}
```

---

#### 🎯 High-Accuracy Usage (Transformer Model)

For **complex text** or when **higher accuracy** is required, you can specify the transformer model (`ModelType.TRF`).

```python
from pii_redactor import redact_pii, ModelType

@redact_pii(model=ModelType.TRF)
def process_complex_document(document: dict):
    return document

document = {
    "author": "Paris Hilton",
    "destination": "Paris, France",
    "company": "Hilton Hotels"
}

redacted_document = process_complex_document(document)
# {'author': '[REDACTED]', 'destination': '[REDACTED], [REDACTED]', 'company': '[REDACTED]'}
```

---

### 📜 Audit Logging (WIP)

The `@log_audit` decorator creates a structured audit trail for any function.
It logs **inputs**, **outputs**, and a **timestamp** as a JSON object—ideal for monitoring and debugging AI agent interactions.

---

## 🕵️ What Information is Redacted?

PII redaction is powered by **spaCy’s Named Entity Recognition (NER)** models.
The following entity types are currently targeted:

* **PERSON** → Names of people (e.g., `John Smith`)
* **ORG** → Companies, agencies, institutions (e.g., `Google`, `Acme Corp`)
* **GPE** → Countries, cities, states (e.g., `Germany`, `London`)
* **LOC** → Non-GPE locations, mountains, water bodies (e.g., `Mount Everest`)
* **DATE** → Dates, relative periods (e.g., `June 2024`, `yesterday`)

⚠️ **Note:** The decorator does **not** currently redact other PII types such as **emails, phone numbers, or credit card numbers**.

---

## ⚡ Model Selection

Choose the model that best fits your use case by passing a `ModelType` enum member to the decorator.

| Model           | ModelType Member | Accuracy (F-Score) | Size     | Speed | Best For                                             |
| --------------- | ---------------- | ------------------ | -------- | ----- | ---------------------------------------------------- |
| **Small**       | `ModelType.SM`   | \~0.86             | \~12 MB  | Fast  | General-purpose, high-throughput tasks               |
| **Transformer** | `ModelType.TRF`  | >0.90              | \~400 MB | Slow  | High-accuracy tasks, complex sentences, critical PII |

🔹 The **F-score** balances **precision** (correct entities) and **recall** (entities found). A higher score is better.

---

## 🛠️ Design Decisions

### ❓ Why Dictionary Keys Are Not Redacted

The `@redact_pii` decorator redacts **string values** inside nested data structures (lists, dicts, etc.), but **does not redact dictionary keys**.

* Keys (e.g., `"user"`, `"location"`, `"id"`) are essential for **program logic**.
* Redacting them could **break downstream applications**.

👉 This design ensures **sensitive values** are protected while keeping the data **usable**.

---

## 🧪 Running Tests

To run the test suite:

1. Clone the repository

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

* [ ] Expand redaction to cover emails, phone numbers, and financial identifiers
* [ ] Extend audit logging with external storage backends (e.g., S3, BigQuery)
* [ ] Add more granular control over entity types to redact

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements.

---

## 📄 License

MIT License © 2025 l8e
