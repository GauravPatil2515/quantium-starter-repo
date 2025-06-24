# Pink Morsel Sales Visualization Dashboard
# 
# This script creates a Dash app to visualize sales data for the "pink morsel" product.
# Before running, make sure you have the required packages installed:
#
# pip install dash plotly pandas
#
# For testing, you'll also need:
# pip install pytest dash[testing]
#
# The dashboard shows daily sales over time with a vertical line indicating 
# a price increase on January 15, 2021.
# It allows filtering sales data by region using radio buttons.

import pandas as pd
import os
import sys
from datetime import datetime

# Check for required packages
try:
    import dash
    from dash import dcc, html, callback
    from dash.dependencies import Input, Output
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    print("\n" + "="*70)
    print("ERROR: Required packages are not installed.")
    print("Please install them using one of the following commands:")
    print("\npip install dash plotly pandas")
    print("\nOR")
    print("\npip install -r requirements.txt")
    print("="*70 + "\n")
    sys.exit(1)

# Custom CSS styles
external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap',
        'rel': 'stylesheet'
    }
]

# Custom CSS for the app
custom_styles = {
    'app_container': {
        'fontFamily': 'Montserrat, sans-serif',
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': '#F8F9FA'
    },
    'header': {
        'textAlign': 'center',
        'color': '#FB0D9B',
        'backgroundColor': 'white',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    },
    'chart_container': {
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'marginBottom': '20px'
    },
    'radio_container': {
        'backgroundColor': 'white',
        'padding': '15px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'marginBottom': '20px'
    },
    'radio_options': {
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'center',
        'gap': '20px',
        'marginTop': '10px'
    }
}

def create_app():
    """
    Create and return the Dash application instance.
    This function is separate from main() to make the app testable.
    """
    # Read the processed CSV file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pink_morsel_sales.csv')
    
    # Check if file exists and return None if not found (for testing purposes)
    if not os.path.exists(file_path):
        print(f"\nERROR: File not found at {file_path}")
        print("Make sure the pink_morsel_sales.csv file is in the project directory.")
        return None
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    
    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort the data by date
    df = df.sort_values('date')
    
    # Create a Dash application with external stylesheets
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    
    # Define the layout of the app with improved styling
    app.layout = html.Div([
        # Header
        html.Div([
            html.H1("Pink Morsel Sales Over Time"),
            html.P("Daily sales analysis by region")
        ], style=custom_styles['header']),
        
        # Radio button for region selection
        html.Div([
            html.H3("Select Region:", style={'textAlign': 'center'}),
            html.Div([
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                        {'label': 'All Regions', 'value': 'all'}
                    ],
                    value='all',  # Default selection
                    labelStyle={'marginRight': '15px', 'cursor': 'pointer', 'fontWeight': 'bold'},
                    style={'color': '#636EFA'}
                )
            ], style=custom_styles['radio_options'])
        ], style=custom_styles['radio_container']),
        
        # Sales chart
        html.Div([
            dcc.Graph(id='sales-time-series')
        ], style=custom_styles['chart_container'])
        
    ], style=custom_styles['app_container'])
    
    # Register callbacks
    register_callbacks(app, df)
    
    return app

def register_callbacks(app, df):
    """Register all callbacks for the app"""
    @app.callback(
        Output('sales-time-series', 'figure'),
        [Input('region-selector', 'value')]
    )
    def update_chart(selected_region):
        # Filter data based on selected region
        if selected_region == 'all':
            # Aggregate sales by date across all regions
            filtered_df = df.groupby('date')['sales'].sum().reset_index()
            region_title = 'All Regions'
        else:
            # Filter for selected region
            filtered_df = df[df['region'] == selected_region]
            # Aggregate sales by date for the selected region
            filtered_df = filtered_df.groupby('date')['sales'].sum().reset_index()
            region_title = selected_region.capitalize()
        
        # Create figure with updated data
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=filtered_df['date'], 
                y=filtered_df['sales'],
                mode='lines',
                name=f'{region_title} Sales',
                line=dict(color='#FB0D9B', width=2)
            )
        )
        
        # Add price increase vertical line
        fig.add_shape(
            type='line',
            x0='2021-01-15',
            y0=0,
            x1='2021-01-15',
            y1=filtered_df['sales'].max() * 1.1 if not filtered_df.empty else 1000,
            line=dict(color='red', width=2, dash='dash')
        )
        
        # Add annotation for price increase
        fig.add_annotation(
            x='2021-01-15',
            y=filtered_df['sales'].max() * 1.1 if not filtered_df.empty else 1000,
            text='Price Increase',
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-30
        )
        
        # Update layout
        fig.update_layout(
            title=f'Daily Sales of Pink Morsel - {region_title}',
            xaxis=dict(title='Date', gridcolor='#EAEAEA'),
            yaxis=dict(title='Sales (in dollars)', gridcolor='#EAEAEA'),
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            hovermode='x unified',
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        return fig

def main():
    """Main function to run the app"""
    # Create the app
    app = create_app()
    
    if app is None:
        sys.exit(1)
    
    # Run the server
    print("\n" + "="*70)
    print("Starting Dash server. Navigate to http://127.0.0.1:8050/ in your web browser.")
    print("Interactive features:")
    print("- Use the radio buttons to filter sales data by region")
    print("- Hover over the chart to see detailed sales values")
    print("Press Ctrl+C to stop the server.")
    print("="*70 + "\n")
    
    try:
        app.run_server(debug=True)
    except Exception as e:
        print(f"\nError starting the Dash server: {str(e)}")
        sys.exit(1)

# This ensures the app is importable for testing
if __name__ == "__main__":
    main()
