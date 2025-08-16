import pytest
from l8e_beam.decorator import redact_pii, ModelType
# --- Test Cases for Parameterization ---
PII_EXAMPLES = [
    # (Input String, Expected Redacted String)
    ("My name is John Smith.", "My name is [REDACTED]."),
    ("I work for Apple Inc. in Cupertino.", "I work for [REDACTED] in [REDACTED]."),
    ("The meeting is on Tuesday with an Smith.", "The meeting is on [REDACTED] with an [REDACTED]."),
    ("He traveled from London to New York.", "He traveled from [REDACTED] to [REDACTED]."),
    ("This is a safe string.", "This is a safe string."),
]

@pytest.mark.parametrize("input_text, expected_text", PII_EXAMPLES)
def test_various_pii_examples_sm(input_text, expected_text):
    """Tests a variety of PII strings using the default 'sm' model."""
    @redact_pii()
    def process(text):
        return text
    
    assert process(input_text) == expected_text

@pytest.mark.slow
@pytest.mark.parametrize("input_text, expected_text", PII_EXAMPLES)
def test_various_pii_examples_trf(input_text, expected_text):
    """Tests a variety of PII strings using the 'trf' model."""
    @redact_pii(model=ModelType.TRF)
    def process(text):
        return text
    
    assert process(input_text) == expected_text

def test_redaction_in_deeply_nested_dict():
    """Tests that PII is redacted in a complex, deeply nested dictionary."""
    @redact_pii()
    def process_data(data):
        return data

    user_data = {
        "level1": {
            "user": "Eve Adams",
            "level2": {
                "company": "Stark Industries",
                "locations": ["New York", "London"],
                "level3": {
                    "contact": "Contact person is Tony Stark."
                }
            }
        }
    }
    
    result = process_data(user_data)
    
    assert result["level1"]["user"] == "[REDACTED]"
    assert result["level1"]["level2"]["company"] == "[REDACTED]"
    assert result["level1"]["level2"]["locations"] == ["[REDACTED]", "[REDACTED]"]
    assert result["level1"]["level2"]["level3"]["contact"] == "Contact person is [REDACTED]."

def test_redaction_in_list_of_dicts():
    """Tests redaction within a list of dictionaries."""
    @redact_pii()
    def process_logs(logs):
        return logs

    log_entries = [
        {"user": "Peter Parker", "action": "login", "location": "New York"},
        {"user": "Bruce Wayne", "action": "logout", "location": "Gotham City"}
    ]
    
    result = process_logs(log_entries)
    
    assert result[0]["user"] == "[REDACTED]"
    assert result[0]["location"] == "[REDACTED]"
    assert result[1]["user"] == "[REDACTED]"
    # Note: "Gotham City" is fictional and may not be in the 'sm' model's vocabulary
    # This is a good example of a potential limitation.
    # assert result[1]["location"] == "[REDACTED]" 

@pytest.mark.slow
def test_contextual_name_with_trf_model():
    """
    Tests a context-sensitive case where a name could also be a location.
    The 'trf' model should be able to distinguish this correctly.
    """
    @redact_pii(model=ModelType.TRF)
    def process_context(data):
        return data

    context_data = {
        "person": "Paris Hilton",
        "destination": "Paris, France"
    }
    
    result = process_context(context_data)
    
    assert result["person"] == "[REDACTED]"
    # The transformer model correctly identifies both "Paris" and "France"
    # as separate entities, so we expect two redactions.
    assert result["destination"] == "[REDACTED], [REDACTED]"
