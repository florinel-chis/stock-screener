# backend/api/app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(
    filename='../logs/backend.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

DATA_DIR = '../data'
PROCESSED_DIR = os.path.join(DATA_DIR, 'stocks', 'processed')
SP500_CSV = os.path.join(DATA_DIR, 'sp500_companies.csv')

def load_sp500_companies():
    try:
        df = pd.read_csv(SP500_CSV)
        symbols = df['Symbol'].tolist()
        companies = df.to_dict(orient='records')
        logging.info("Loaded S&P 500 companies.")
        return companies
    except Exception as e:
        logging.error(f"Error loading S&P 500 companies: {e}")
        return []

def load_stock_data(symbol=None):
    """
    Load stock data. If symbol is provided, load data for that symbol.
    Otherwise, load all stock data.
    """
    if symbol:
        file_path = os.path.join(PROCESSED_DIR, f"{symbol}.json")
        if not os.path.exists(file_path):
            logging.warning(f"Data file for symbol {symbol} not found.")
            return None
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logging.error(f"Error loading data for symbol {symbol}: {e}")
            return None
    else:
        # Load all stock data
        stock_data = []
        for filename in os.listdir(PROCESSED_DIR):
            if filename.endswith('.json'):
                symbol = filename.replace('.json', '')
                data = load_stock_data(symbol)
                if data:
                    stock_data.append(data)
        return stock_data


@app.route('/api/sp500', methods=['GET'])
def get_sp500():
    companies = load_sp500_companies()
    return jsonify(companies), 200
#http://localhost:5001/api/stock-all-data?williamsR_from=-100&williamsR_to=-80&rsi14_from=100

@app.route('/api/stock-all-data', methods=['GET'])
def get_all_stock_data():
    try:
        # Retrieve interval filter parameters from query string
        williams_r_from = request.args.get('williamsR_from', type=float)
        williams_r_to = request.args.get('williamsR_to', type=float)
        ema_williams_r_from = request.args.get('emaWilliamsR_from', type=float)
        ema_williams_r_to = request.args.get('emaWilliamsR_to', type=float)
        rsi14_from = request.args.get('rsi14_from', type=float)
        rsi14_to = request.args.get('rsi14_to', type=float)
        rsi21_from = request.args.get('rsi21_from', type=float)
        rsi21_to = request.args.get('rsi21_to', type=float)
        
        # Initialize list to hold filtered stock data
        filtered_data = []
        
        # Load all stock data
        stock_data = load_stock_data()
        
        if not stock_data:
            logging.warning("No stock data available to filter.")
            return jsonify({"error": "No stock data available"}), 404
        
        # Iterate through each stock data entry
        for data in stock_data:
            # Flag to determine if the current entry should be included
            include = True
            
            # Apply Williams %R filter
            if williams_r_from is not None:
                if data.get('Williams_R_21') is None or data['Williams_R_21'] < williams_r_from:
                    include = False
            if williams_r_to is not None:
                if data.get('Williams_R_21') is None or data['Williams_R_21'] > williams_r_to:
                    include = False
            
            # Apply EMA(13) of Williams %R filter
            if ema_williams_r_from is not None:
                if data.get('EMA_13_Williams_R') is None or data['EMA_13_Williams_R'] < ema_williams_r_from:
                    include = False
            if ema_williams_r_to is not None:
                if data.get('EMA_13_Williams_R') is None or data['EMA_13_Williams_R'] > ema_williams_r_to:
                    include = False
            
            # Apply RSI 14 filter
            if rsi14_from is not None:
                if data.get('RSI_14') is None or data['RSI_14'] < rsi14_from:
                    include = False
            if rsi14_to is not None:
                if data.get('RSI_14') is None or data['RSI_14'] > rsi14_to:
                    include = False
            
            # Apply RSI 21 filter
            if rsi21_from is not None:
                if data.get('RSI_21') is None or data['RSI_21'] < rsi21_from:
                    include = False
            if rsi21_to is not None:
                if data.get('RSI_21') is None or data['RSI_21'] > rsi21_to:
                    include = False
            
            # If all filters pass, include the data entry
            if include:
                filtered_data.append(data)
        
        logging.info(f"Served {len(filtered_data)} filtered stock data entries.")
        return jsonify(filtered_data), 200

    except Exception as e:
        logging.error(f"Error fetching all stock data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/stock-data/<string:symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        data = load_stock_data(symbol.upper())
        if data:
            return jsonify(data), 200
        else:
            return jsonify({"error": "Symbol not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
