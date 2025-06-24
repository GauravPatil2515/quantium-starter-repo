# Testing the Dash Application

This document provides instructions for testing the Pink Morsel Sales Dashboard using pytest and the Dash testing framework.

## Prerequisites

Install the testing dependencies:

```bash
pip install -r test_requirements.txt
```

This will install:
- pytest for running the tests
- dash[testing] for the Dash testing utilities
- selenium for browser automation

## Running the Tests

To run all tests:

```bash
pytest test_visualize_sales.py -v
```

## Test Coverage

The tests check that:

1. The layout contains all essential components:
   - The header with "Pink Morsel Sales" title
   - The sales time series graph (with ID "sales-time-series")
   - The region selector radio buttons (with ID "region-selector")

2. The interactive functionality works correctly:
   - Selecting a region updates the graph title and content

## Troubleshooting

If you encounter errors:

1. Make sure `visualize_sales_app.py` and the data file `pink_morsel_sales.csv` are in the same directory.
2. Verify that all dependencies are correctly installed.
3. WebDriver issues: The tests use Chrome by default; ensure you have Chrome installed, or modify the tests to use a different browser.

## Adding More Tests

To add more tests:
1. Add new test functions to `test_visualize_sales.py`
2. Follow the pattern of existing tests, using the `dash_duo` fixture

Example:
```python
def test_new_feature(dash_duo, dash_app):
    """Description of what you're testing."""
    dash_duo.start_server(dash_app)
    # Test steps here
    assert condition, "Message if test fails"
```
