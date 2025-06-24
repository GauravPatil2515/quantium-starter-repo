# Quantium Sales Data Analysis

This repository contains scripts for processing and visualizing sales data, focusing on the "pink morsel" product.

## Scripts

### 1. Process Sales Data (`process_sales.py`)

This script reads all CSV files in the `data/` folder, filters for rows with product == 'pink morsel', calculates sales (quantity * price), and outputs a single CSV file with sales, date, and region columns.

To run:

```bash
python process_sales.py
```

Output: `pink_morsel_sales.csv`

### 2. Visualize Sales Data (`visualize_sales.py`)

This script creates a Dash web application that visualizes the processed sales data for the "pink morsel" product. It shows total daily sales over time with a vertical line indicating a price increase on January 15, 2021.

To run:

```bash
python visualize_sales.py
```

Then open your web browser and navigate to: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

## Requirements

The required packages are listed in `requirements.txt`. You can install them using:

```bash
pip install -r requirements.txt
```

Or install the specific packages needed for visualization:

```bash
pip install dash plotly pandas
```
