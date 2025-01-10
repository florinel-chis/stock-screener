// src/components/Header.js

import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';
import ShowChartIcon from '@mui/icons-material/ShowChart';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <ShowChartIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          S&P 500 Stock Screener
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header; // Ensure default export
