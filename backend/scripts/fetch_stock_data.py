# backend/scripts/fetch_stock_data.py

import pandas as pd
import yfinance as yf
import os
import json
from datetime import datetime
import logging
import concurrent.futures
import re
import time

# Configure logging
logging.basicConfig(
    filename='../logs/backend.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def sanitize_filename(symbol):
    """
    Sanitizes the stock symbol to create a safe filename.
    Replaces any character that's not alphanumeric or '-' with '_'.
    """
    return re.sub(r'[^\w\-]', '_', symbol)

def get_sp500_symbols(csv_path='../data/sp500_companies.csv'):
    """
    Reads the S&P 500 companies CSV and returns a list of ticker symbols.
    """
    try:
        df = pd.read_csv(csv_path)
        symbols = df['Symbol'].tolist()
        logging.info(f"Retrieved {len(symbols)} symbols from {csv_path}.")
        return symbols
    except Exception as e:
        logging.error(f"Error reading S&P 500 companies CSV: {e}")
        return []

def fetch_and_save_historical(symbol, output_dir='../data/stocks/historical'):
    """
    Fetches the last 6 months of stock data for a given symbol and saves it as a JSON file.
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='6mo', interval='1d')  # Fetch the last 6 months

        if hist.empty:
            logging.warning(f"No historical data found for symbol: {symbol}")
            return

        # Reset index to get 'Date' as a column
        hist.reset_index(inplace=True)

        # Convert Timestamp to string for JSON serialization
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')

        # Convert DataFrame to dictionary
        data = hist.to_dict(orient='records')
        data = {
            'Symbol': symbol,
            'Historical_Data': data
        }

        # Sanitize filename
        safe_symbol = sanitize_filename(symbol)
        filename = f"{safe_symbol}.json"
        file_path = os.path.join(output_dir, filename)

        # Save to JSON
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Fetched and saved historical data for {symbol} to {file_path}")

    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")

def fetch_stock_data(symbols, output_dir='../data/stocks/historical'):
    """
    Fetches historical stock price data for the given symbols using yfinance and saves each as a separate JSON file.
    Utilizes multithreading for faster execution while respecting rate limits.
    """
    try:
        logging.info("Starting to fetch historical stock data...")
        os.makedirs(output_dir, exist_ok=True)

        # To respect rate limits, limit the number of workers and add slight delays if necessary
        max_workers = 10  # Adjust based on system capabilities and rate limits
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(fetch_and_save_historical, symbol, output_dir): symbol for symbol in symbols}
            for future in concurrent.futures.as_completed(futures):
                symbol = futures[future]
                try:
                    future.result()
                    # Optional: Add a short sleep to prevent hitting rate limits
                    time.sleep(0.1)
                except Exception as e:
                    logging.error(f"Unhandled exception for {symbol}: {e}")

        logging.info("Completed fetching historical stock data.")

    except Exception as e:
        logging.error(f"Error during stock data fetching: {e}")

def main():
    symbols = get_sp500_symbols()
    if symbols:
        fetch_stock_data(symbols)
    else:
        logging.error("No symbols to fetch.")

if __name__ == "__main__":
    main()
