#!/bin/bash

# This script automates the setup and testing process for the l8e-beam package.
# It robustly handles spaCy model versions by finding the downloaded model
# and renaming it to the fixed path expected by the Python code.
#
# To use it:
# 1. Make sure you are in an activated virtual environment.
# 2. Make the script executable: chmod +x build.sh
# 3. Run the script: ./build.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Define Model Names as Variables ---
SM_MODEL_NAME="en_core_web_sm"
TRF_MODEL_NAME="en_core_web_trf"

# --- 1. Download SpaCy Models ---
echo "--- 📥 Downloading spaCy models... ---"
python -m spacy download "$SM_MODEL_NAME"
python -m spacy download "$TRF_MODEL_NAME"

# --- 2. Copy Models to Source Directory ---
echo "---  copying models to src/pii_redactor/model... ---"

# Find the site-packages directory of the current virtual environment
VENV_PATH=$(python -c "import site; print(site.getsitepackages()[0])")

# Define the destination directory for the models
DEST_DIR="src/l8e_beam/model"

# Ensure the destination directory exists
mkdir -p "$DEST_DIR"

# --- Define the fixed model names that our Python Enum expects ---
SM_MODEL_DEST_NAME="$SM_MODEL_NAME-3.7.1"
TRF_MODEL_DEST_NAME="$TRF_MODEL_NAME-3.7.3"

# --- Find and copy the SM model ---
# Find the actual downloaded directory path using a wildcard
SM_MODEL_SRC_PATH=$(ls -d "$VENV_PATH/$SM_MODEL_NAME/$SM_MODEL_NAME"*)
# Define the final destination path
SM_MODEL_DEST_PATH="$DEST_DIR/$SM_MODEL_DEST_NAME"
echo "Copying $SM_MODEL_SRC_PATH to $SM_MODEL_DEST_PATH"
# Remove the old directory if it exists, then copy the new one
rm -rf "$SM_MODEL_DEST_PATH"
cp -r "$SM_MODEL_SRC_PATH" "$SM_MODEL_DEST_PATH"

# --- Find and copy the TRF model ---
# Find the actual downloaded directory path using a wildcard
TRF_MODEL_SRC_PATH=$(ls -d "$VENV_PATH/$TRF_MODEL_NAME/$TRF_MODEL_NAME"*)
# Define the final destination path
TRF_MODEL_DEST_PATH="$DEST_DIR/$TRF_MODEL_DEST_NAME"
echo "Copying $TRF_MODEL_SRC_PATH to $TRF_MODEL_DEST_PATH"
# Remove the old directory if it exists, then copy the new one
rm -rf "$TRF_MODEL_DEST_PATH"
cp -r "$TRF_MODEL_SRC_PATH" "$TRF_MODEL_DEST_PATH"

echo "--- ✅ Models copied successfully. ---"


# --- 3. Run Pytest ---
echo "--- 🧪 Running unit tests... ---"
python -m pytest

echo "--- 🎉 Build and test process completed successfully! ---"
