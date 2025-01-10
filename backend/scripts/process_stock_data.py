# backend/scripts/process_stock_data.py

import pandas as pd
import talib
import json
import os
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

def load_historical_data(symbol, input_dir='../data/stocks/historical'):
    """
    Loads historical stock data from a JSON file.
    """
    try:
        safe_symbol = sanitize_filename(symbol)
        filename = f"{safe_symbol}.json"
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
        logging.info(f"Loaded historical data for {symbol} from {file_path}")
        return data['Historical_Data']
    except Exception as e:
        logging.error(f"Error loading historical data for {symbol}: {e}")
        return None

def calculate_indicators(symbol, historical_data, output_dir='../data/stocks/processed'):
    """
    Calculates technical indicators using TA-Lib and saves the processed data as a separate JSON file.
    """
    try:
        df = pd.DataFrame(historical_data)
        # Ensure necessary columns are present
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
        if not all(col in df.columns for col in required_columns):
            logging.error(f"Missing required columns for {symbol}. Skipping.")
            return

        # Convert data types
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')

        # Drop rows with NaN values in critical columns
        df.dropna(subset=['Close', 'High', 'Low'], inplace=True)

        if df.empty:
            logging.warning(f"No valid data available for {symbol} after cleaning.")
            return

        # Calculate Williams %R (21)
        df['Williams_%R_21'] = talib.WILLR(df['High'], df['Low'], df['Close'], timeperiod=21)

        # Calculate EMA(13) of Williams %R (21)
        df['EMA_13_Williams_%R'] = talib.EMA(df['Williams_%R_21'], timeperiod=13)

        # Calculate RSI 14
        df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)

        # Calculate RSI 21
        df['RSI_21'] = talib.RSI(df['Close'], timeperiod=21)

        # Keep only the latest day's data
        latest = df.iloc[-1].to_dict()

        processed_data = {
            'Symbol': symbol,
            'Date': latest['Date'],
            'Close': latest['Close'],
            'Williams_R_21': latest['Williams_%R_21'],
            'EMA_13_Williams_R': latest['EMA_13_Williams_%R'],
            'RSI_14': latest['RSI_14'],
            'RSI_21': latest['RSI_21']
        }

        # Save processed data
        os.makedirs(output_dir, exist_ok=True)
        safe_symbol = sanitize_filename(symbol)
        filename = f"{safe_symbol}.json"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w') as f:
            json.dump(processed_data, f, indent=4)

        logging.info(f"Processed data for {symbol} has been saved to {file_path}")

    except Exception as e:
        logging.error(f"Error processing data for {symbol}: {e}")

def process_symbol(symbol, input_dir='../data/stocks/historical', output_dir='../data/stocks/processed'):
    """
    Processes a single stock symbol: loads historical data, calculates indicators, and saves processed data.
    """
    historical_data = load_historical_data(symbol, input_dir)
    if historical_data:
        calculate_indicators(symbol, historical_data, output_dir)

def process_all_symbols(symbols, input_dir='../data/stocks/historical', output_dir='../data/stocks/processed'):
    """
    Processes all stock symbols concurrently.
    """
    try:
        logging.info("Starting to process stock data...")
        os.makedirs(output_dir, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_symbol, symbol, input_dir, output_dir): symbol for symbol in symbols}
            for future in concurrent.futures.as_completed(futures):
                symbol = futures[future]
                try:
                    future.result()
                    # Optional: Add a short sleep to manage resource usage
                    time.sleep(0.05)
                except Exception as e:
                    logging.error(f"Unhandled exception during processing of {symbol}: {e}")

        logging.info("Completed processing all stock data.")

    except Exception as e:
        logging.error(f"Error during processing all symbols: {e}")

def main():
    symbols = get_sp500_symbols()
    if symbols:
        process_all_symbols(symbols)
    else:
        logging.error("No symbols to process.")

if __name__ == "__main__":
    main()
