
# PII Redaction and Anonymization Library: l8e-beam Examples

This repository contains examples demonstrating how to use the **l8e-beam** library to detect and handle Personally Identifiable Information (PII) in your Python applications. The examples cover basic decorator usage, advanced API functions, and integration with a web framework like FastAPI.

---

## 🚀 Core Features

- **PII Detection**: Identifies PII such as names, email addresses, phone numbers, and more within various data structures (dictionaries, strings).

- **Multiple Actions**:
  - **Anonymize**: Replaces detected PII with realistic fake data (e.g., `"Jane Doe"` → `"Markus Kramer"`).
  - **Redact**: Replaces PII with a placeholder label (e.g., `"Jane Doe"` → `[REDACTED PERSON]`).

- **Flexible Models**:
  - `ModelType.SM`: A small, fast spaCy-based model for general use.
  - `ModelType.TRF`: A larger, more accurate transformer-based model for nuanced, context-aware detection.

- **Extensible**: Allows adding custom PII recognizers (e.g., for UUIDs) and disabling default ones.

- **Easy Integration**: Provides a simple decorator for quick implementation and a direct API for fine-grained control.

---

## 📚 Examples

### 1. Decorator Usage (`decorator_usage.py`)

This example shows the simplest way to use the library.  
The `@redact_pii` decorator automatically processes the arguments and return value of a function.

**Key Concepts:**
- Use `@redact_pii` on a function to protect its data.
- Set the action to `PiiAction.ANONYMIZE` or `PiiAction.REDACT`.
- Choose a model (`ModelType.SM` or `ModelType.TRF`) based on your accuracy and performance needs.

**How to Run:**
```bash
python examples/decorator_usage.py
````

---

### 2. Advanced API Usage (`api_usage.py`)

This script demonstrates how to use the `sanitize_pii` function directly for more complex scenarios, such as adding custom rules or modifying behavior dynamically.

**Key Concepts:**

* Call `sanitize_pii()` on your data for programmatic control.
* **Custom Recognizers**: Define your own classes inheriting from `RegexRecognizer` to find and process custom patterns (like UUIDs).
* **Disable Recognizers**: Pass a list of recognizers to `disabled_recognizers` to ignore certain types of PII (e.g., emails).

**How to Run:**

```bash
python examples/api_usage.py
```

---

### 3. FastAPI Integration (`integrate_fastapi.py`)

This example illustrates how to protect a web API built with **FastAPI**. It provides two endpoints to show both the decorator and direct API approaches in a real-world context.

**Key Concepts:**

* **Decorator Method**: Apply the `@redact_pii` decorator directly to a FastAPI path operation function to automatically sanitize incoming Pydantic models.
* **API Method**: Call `sanitize_pii` inside an endpoint to implement conditional logic, such as enabling or disabling redaction based on a query parameter.

**How to Run:**

1. Install dependencies:

   ```bash
   pip install "fastapi[all]" uvicorn
   ```
2. Start the server from the project root:

   ```bash
   uvicorn examples.integrate_fastapi:app --reload
   ```
3. Send POST requests to the endpoints:

   * `http://127.0.0.1:8000/process-with-decorator`
   * `http://127.0.0.1:8000/process-with-api`

**Example Request Body:**

```json
{
  "user_id": "user-123",
  "full_name": "Jane Doe",
  "query": "Please book a flight to Paris for me.",
  "metadata": { "source_ip": "192.168.1.1" }
}
```
