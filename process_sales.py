import pandas as pd
import os
import glob

def main():
    # Path to data folder
    data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    # Get all CSV files in the data folder
    csv_files = glob.glob(os.path.join(data_folder, '*.csv'))
    
    # List to store dataframes
    dfs = []
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"Processing file: {os.path.basename(csv_file)}")
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Filter for rows with product == 'pink morsel'
        df = df[df['product'] == 'pink morsel']
        
        # Convert price to numeric (remove '$' and convert to float)
        df['price'] = df['price'].str.replace('$', '').astype(float)
        
        # Calculate sales
        df['sales'] = df['quantity'] * df['price']
        
        # Keep only sales, date, and region columns
        df = df[['sales', 'date', 'region']]
        
        # Add to list of dataframes
        dfs.append(df)
    
    # Combine all dataframes
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Output to a single CSV
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pink_morsel_sales.csv')
        combined_df.to_csv(output_file, index=False)
        print(f"Output saved to: {output_file}")
        print(f"Total rows processed: {len(combined_df)}")
    else:
        print("No data matching the criteria was found.")

if __name__ == "__main__":
    main()
