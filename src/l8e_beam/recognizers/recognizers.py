import importlib
import inspect
import pathlib
from typing import List

# Import the base classes, as we need them for type checking
from l8e_beam.recognizers.base import Recognizer, RegexRecognizer, SpacyRecognizer

def load_recognizers() -> List[Recognizer]:
    """
    Dynamically discovers and instantiates all Recognizer classes
    in this directory.
    """
    recognizer_instances = []
    package_dir = pathlib.Path(__file__).resolve().parent

    # Iterate over all python files in the current directory
    for file_path in package_dir.glob("*.py"):
        # Skip special files
        if file_path.name in ("__init__.py", "base.py"):
            continue

        # Convert file path to module path for import
        # e.g., /path/to/credit_card.py -> .credit_card
        module_name = f".{file_path.stem}"
        
        # Dynamically import the module
        module = importlib.import_module(module_name, package=__package__)

        # Inspect the module for classes that are subclasses of Recognizer
        for name, member in inspect.getmembers(module, inspect.isclass):
            # Check if it's a concrete subclass of Recognizer
            if (issubclass(member, Recognizer) and member not in 
                    [Recognizer, RegexRecognizer, SpacyRecognizer]):
                recognizer_instances.append(member())
                
    return recognizer_instances

# --- Pre-populated Lists for Easy Import ---

# A single list containing all discovered recognizer instances
ALL_RECOGNIZERS = load_recognizers()

# Filtered lists for convenience in the PiiProcessor
REGEX_RECOGNIZERS = [
    rec for rec in ALL_RECOGNIZERS if isinstance(rec, RegexRecognizer)
]

SPACY_RECOGNIZERS = [
    rec for rec in ALL_RECOGNIZERS if isinstance(rec, SpacyRecognizer)
]

# Defines the public API of this package
__all__ = [
    "ALL_RECOGNIZERS",
    "REGEX_RECOGNIZERS",
    "SPACY_RECOGNIZERS",
    "Recognizer",       # It's good practice to export the base classes too
    "RegexRecognizer",
    "SpacyRecognizer"
]