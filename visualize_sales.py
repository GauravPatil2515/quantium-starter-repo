# Pink Morsel Sales Visualization Dashboard
# 
# This script creates a Dash app to visualize sales data for the "pink morsel" product.
# Before running, make sure you have the required packages installed:
#
# pip install dash plotly pandas
#
# The dashboard shows daily sales over time with a vertical line indicating 
# a price increase on January 15, 2021.

import pandas as pd
import os
import sys
from datetime import datetime

# Check for required packages
try:
    import dash
    from dash import dcc, html
    import plotly.express as px
except ImportError:
    print("\n" + "="*70)
    print("ERROR: Required packages are not installed.")
    print("Please install them using one of the following commands:")
    print("\npip install dash plotly pandas")
    print("\nOR")
    print("\npip install -r requirements.txt")
    print("="*70 + "\n")
    sys.exit(1)

def main():
    # Read the processed CSV file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pink_morsel_sales.csv')
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"\nERROR: File not found at {file_path}")
        print("Make sure the pink_morsel_sales.csv file is in the project directory.")
        sys.exit(1)
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    
    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort the data by date
    df = df.sort_values('date')
    
    # Aggregate sales by date (sum across regions)
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    
    # Create a Dash application
    app = dash.Dash(__name__)
    
    # Define the layout of the app
    app.layout = html.Div([
        html.H1("Pink Morsel Sales Over Time", style={'textAlign': 'center', 'color': '#636EFA'}),
        
        dcc.Graph(
            id='sales-time-series',
            figure={
                'data': [
                    {
                        'x': daily_sales['date'],
                        'y': daily_sales['sales'],
                        'type': 'line',
                        'name': 'Daily Sales',
                        'line': {'color': '#FB0D9B', 'width': 2}  # Pink line for Pink Morsel
                    }
                ],
                'layout': {
                    'title': 'Daily Sales of Pink Morsel',
                    'xaxis': {'title': 'Date', 'gridcolor': '#EAEAEA'},
                    'yaxis': {'title': 'Sales (in dollars)', 'gridcolor': '#EAEAEA'},
                    'plot_bgcolor': '#FFFFFF',
                    'paper_bgcolor': '#FFFFFF',
                    'shapes': [{
                        'type': 'line',
                        'x0': '2021-01-15',
                        'y0': 0,
                        'x1': '2021-01-15',
                        'y1': daily_sales['sales'].max() * 1.1,  # Extend a bit above the max value
                        'line': {
                            'color': 'red',
                            'width': 2,
                            'dash': 'dash',
                        }
                    }],
                    'annotations': [{
                        'x': '2021-01-15',
                        'y': daily_sales['sales'].max() * 1.1,
                        'xref': 'x',
                        'yref': 'y',
                        'text': 'Price Increase',
                        'showarrow': True,
                        'arrowhead': 2,
                        'ax': 0,
                        'ay': -30
                    }]
                }
            }
        )
    ], style={'margin': '20px', 'fontFamily': 'Arial'})
    
    # Run the server
    print("\n" + "="*70)
    print("Starting Dash server. Navigate to http://127.0.0.1:8050/ in your web browser.")
    print("Press Ctrl+C to stop the server.")
    print("="*70 + "\n")
    
    try:
        app.run_server(debug=True)
    except Exception as e:
        print(f"\nError starting the Dash server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
