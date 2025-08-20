#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Install pdoc
pip install pdoc

# Generate the documentation from your source code
pdoc ../src/l8e_beam -o docs/