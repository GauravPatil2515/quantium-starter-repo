#!/bin/bash

# Script to automate running tests for the Pink Morsel Sales Dashboard
# This script will run pytest on the test_visualize_sales.py file and report success or failure

# Exit immediately if a command exits with a non-zero status
set -e

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
source venv/bin/activate

# Install required packages if they don't exist
echo "🔄 Checking and installing required packages..."
if [ -f "test_requirements.txt" ]; then
  pip install -r test_requirements.txt
else
  echo "⚠️ test_requirements.txt not found. Installing basic test requirements..."
  pip install pytest dash dash[testing] plotly pandas selenium
fi

# Display Python and package versions for debugging purposes
echo "🔍 Python version:"
python --version
echo "🔍 Installed packages:"
pip list | grep -E "dash|pytest|plotly|pandas|selenium"

# Run the test suite using pytest with verbose output
print_divider
echo "🧪 Running tests with pytest..."
pytest test_visualize_sales.py -v

# Capture the exit code of pytest
TEST_RESULT=$?

print_divider
# Evaluate test result and exit accordingly
if [ $TEST_RESULT -eq 0 ]; then
  echo "✅ All tests passed successfully!"
  echo "🎉 The Pink Morsel Sales Dashboard is working as expected."
  exit 0
else
  echo "❌ Some tests failed."
  echo "Please check the test output above for details on what went wrong."
  exit 1
fi
