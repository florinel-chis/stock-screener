// src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client'; // Correct import path for React 18
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './themes/theme';
import App from './App';

// Select the root DOM node
const container = document.getElementById('root');

// Create a root
const root = ReactDOM.createRoot(container);

// Initial render
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
