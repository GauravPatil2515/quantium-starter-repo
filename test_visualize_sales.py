import pytest
import sys
import time

# Import our app
try:
    from visualize_sales_app import create_app
except ImportError:
    print("Failed to import visualize_sales_app. Make sure the file exists.")
    sys.exit(1)

@pytest.fixture
def dash_app():
    """Create a dash app for testing."""
    # Create the app using our function
    app = create_app()
    
    if app is None:
        pytest.skip("Could not create app, likely due to missing data file.")
    
    # Modify the app to make testing easier
    # This ensures we're not running server processes during testing
    app.config.suppress_callback_exceptions = True
    return app

@pytest.mark.parametrize("component_id, component_type", [
    ("#region-selector", "RadioItems"),  # Region selector radio buttons
    ("#sales-time-series", "Graph"),     # Sales time series graph
])
def test_components_exist(dash_duo, dash_app, component_id, component_type):
    """
    Test that the components exist in the application.
    
    Parameters:
    -----------
    dash_duo : dash.testing.DashDuo
        Dash testing fixture
    dash_app : dash.Dash
        The dash application being tested
    component_id : str
        CSS selector for the component
    component_type : str
        Expected component type name
    """
    # Start the dash app
    dash_duo.start_server(dash_app)
    
    # Wait for the app to load
    dash_duo.wait_for_page_to_load()
    
    # Check if the component exists
    dash_duo.wait_for_element(component_id)
    
    # Print out confirmation
    print(f"Found {component_type} with ID: {component_id}")
    
    # Additional check to ensure the component is visible
    assert dash_duo.get_element(component_id).is_displayed()

def test_header_exists(dash_duo, dash_app):
    """Test that the header with the correct title exists."""
    # Start the dash app
    dash_duo.start_server(dash_app)
    
    # Wait for the app to load
    dash_duo.wait_for_page_to_load()
    
    # Check if the header exists (using H1 element)
    dash_duo.wait_for_element("h1")
    
    # Get the H1 element(s)
    h1_elements = dash_duo.find_elements("h1")
    
    # Check that we found at least one H1 element
    assert len(h1_elements) > 0
    
    # Check the title text (case-insensitive)
    header_found = False
    for h1 in h1_elements:
        if "Pink Morsel Sales" in h1.text:
            header_found = True
            break
    
    # Assert that we found the header with the expected title
    assert header_found, "Header with 'Pink Morsel Sales' title not found"
    
    # Print confirmation
    print("Found header with title containing 'Pink Morsel Sales'")

def test_region_selection_functionality(dash_duo, dash_app):
    """Test that selecting a region updates the graph."""
    # Start the dash app
    dash_duo.start_server(dash_app)
    
    # Wait for the app to load
    dash_duo.wait_for_page_to_load()
    
    # Wait for radio buttons to be available
    dash_duo.wait_for_element("#region-selector")
    
    # Find all radio options
    radio_options = dash_duo.find_elements('input[type="radio"]')
    
    # Check that we have the expected number of radio options (5: north, east, south, west, all)
    assert len(radio_options) == 5, f"Expected 5 radio options, found {len(radio_options)}"
    
    # Click on the 'North' region
    # Find the specific radio option for "north"
    for radio in radio_options:
        if radio.get_attribute("value") == "north":
            north_radio = radio
            break
    
    # Click on the 'North' region option
    north_radio.click()
    
    # Wait a moment for the callback to execute
    time.sleep(1)
    
    # Check that the graph title has been updated to include "North"
    dash_duo.wait_for_contains_text(".gtitle", "North", timeout=2)
    
    print("Region selection functionality confirmed")
