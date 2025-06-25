#!/bin/bash

# Run Tests Script for Python Dash App Project
# This script automates running the test suite for the Pink Morsel Sales Dashboard
# It activates the virtual environment, runs pytest, and reports success or failure

# Exit immediately if a command exits with a non-zero status
set -e

# Exit if any command in a pipeline fails
set -o pipefail

# Treat unset variables as an error
set -u

# Print a divider line for better readability
print_divider() {
  echo "============================================================="
}

print_divider
echo "🧪 Running test suite for Pink Morsel Sales Dashboard"
print_divider

# Check if venv directory exists
if [ ! -d "venv" ]; then
  echo "❗ Virtual environment not found in venv directory."
  echo "Creating new virtual environment..."
  python -m venv venv
  echo "✅ Virtual environment created successfully."
fi

# Activate the virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || {
  echo "❌ Failed to activate virtual environment."
  exit 1
}

# Install required packages if they don't exist
echo "🔄 Checking and installing required packages..."
if [ -f "test_requirements.txt" ]; then
  pip install -q -r test_requirements.txt
else
  echo "⚠️ test_requirements.txt not found. Installing basic test requirements..."
  pip install -q pytest dash plotly pandas
fi

# Display Python version for verification
echo "🔍 Using Python: $(which python) ($(python --version))"

# Run the test suite using pytest
print_divider
echo "🧪 Running tests with pytest..."
pytest

# Capture the exit code of pytest
TEST_RESULT=$?

print_divider
# Evaluate test result and exit accordingly
if [ $TEST_RESULT -eq 0 ]; then
  echo "✅ All tests passed successfully!"
  exit 0
else
  echo "❌ Some tests failed."
  exit 1
fi
