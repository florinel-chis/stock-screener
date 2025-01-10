import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from io import StringIO

def fetch_sp500_companies():
    """
    Fetches the list of S&P 500 companies from Wikipedia and saves it to a CSV file.
    """
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        print(f"Fetching S&P 500 companies from {url}...")
        
        # Send a GET request to the Wikipedia page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with id 'constituents'
        table = soup.find('table', {'id': 'constituents'})
        
        if table is None:
            print("Error: Could not find the 'constituents' table on the Wikipedia page.")
            return
        
        # Read the table into a DataFrame using StringIO to avoid FutureWarning
        table_html = str(table)
        df = pd.read_html(StringIO(table_html))[0]
        
        # Display the first few rows for verification
        print("First 5 entries of the fetched S&P 500 companies:")
        print(df.head())
        
        # Define the expected columns
        expected_columns = ['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 
                            'Headquarters Location', 'Date first added', 'CIK', 'Founded']
        
        # Check for missing columns
        available_columns = df.columns.tolist()
        missing_columns = [col for col in expected_columns if col not in available_columns]
        if missing_columns:
            print(f"Warning: The following expected columns are missing and will be excluded: {missing_columns}")
            selected_columns = [col for col in expected_columns if col in available_columns]
        else:
            selected_columns = expected_columns
        
        # Select the relevant columns
        df_selected = df[selected_columns]
        
        # Clean the 'Symbol' column to match yfinance format
        if 'Symbol' in df_selected.columns:
            df_selected['Symbol'] = df_selected['Symbol'].astype(str).str.replace('.', '-', regex=False)  # Replace '.' with '-' for ticker symbols like BRK.B to BRK-B
        else:
            print("Error: 'Symbol' column not found in the DataFrame.")
            return
        
        # Save the DataFrame to a CSV file
        output_dir = 'data'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'sp500_companies.csv')
        df_selected.to_csv(output_file, index=False)
        
        print(f"S&P 500 companies list has been saved to {output_file}")
    
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching S&P 500 companies: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    fetch_sp500_companies()

if __name__ == "__main__":
    main()
