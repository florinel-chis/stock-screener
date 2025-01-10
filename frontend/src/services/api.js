// frontend/src/services/api.js

import axios from 'axios';

// Define the base URL for the API
const API_BASE_URL = 'http://localhost:5001/api'; // Ensure this matches your backend port

/**
 * Fetches all processed stock data with optional interval filters.
 * @param {Object} filters - Filtering parameters with 'from' and 'to' for each field.
 */
export const fetchStockData = async (filters = {}) => {
    try {
      const queryParams = new URLSearchParams();
  
      // Iterate over each filter field
      Object.keys(filters).forEach((field) => {
        const { from, to } = filters[field];
        if (from !== '' && from !== null) {
          queryParams.append(`${field}_from`, from);
        }
        if (to !== '' && to !== null) {
          queryParams.append(`${field}_to`, to);
        }
      });
  
      const response = await axios.get(`${API_BASE_URL}/stock-all-data?${queryParams.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  };

/**
 * Fetches the list of S&P 500 companies.
 */
export const fetchSp500Companies = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sp500`);
    return response.data;
  } catch (error) {
    console.error('Error fetching S&P 500 companies:', error);
    throw error;
  }
};

/**
 * Fetches processed stock data for a specific symbol.
 * @param {string} symbol - Stock symbol.
 */
export const fetchStockDataBySymbol = async (symbol) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stock-data/${symbol}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching data for symbol ${symbol}:`, error);
    throw error;
  }
};
