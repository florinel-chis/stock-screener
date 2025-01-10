// src/components/Filters.js

import React from 'react';
import { Grid, TextField, Button, Box } from '@mui/material';

const FILTER_RANGES = {
  williamsR: { from: -100, to: 0 },
  emaWilliamsR: { from: -100, to: 100 }, // Example range; adjust as needed
  rsi14: { from: 0, to: 100 },
  rsi21: { from: 0, to: 100 },
};

const Filters = ({ filters, setFilters }) => {
  // Handle changes for from and to inputs
  const handleChange = (e) => {
    const { name, value, dataset } = e.target;
    const [field, bound] = name.split('_'); // e.g., 'williamsR_from' -> ['williamsR', 'from']

    setFilters((prev) => ({
      ...prev,
      [field]: {
        ...prev[field],
        [bound]: value === '' ? '' : Number(value),
      },
    }));
  };

  // Handle reset functionality
  const handleReset = () => {
    setFilters({
      williamsR: { from: '', to: '' },
      emaWilliamsR: { from: '', to: '' },
      rsi14: { from: '', to: '' },
      rsi21: { from: '', to: '' },
    });
  };

  return (
    <Box sx={{ mb: 3 }}>
      <Grid container spacing={2} alignItems="center">
        {/* Williams %R Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="Williams %R From"
            variant="outlined"
            fullWidth
            name="williamsR_from"
            value={filters.williamsR.from}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.williamsR.from,
                max: FILTER_RANGES.williamsR.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.williamsR.from} to ${FILTER_RANGES.williamsR.to}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="Williams %R To"
            variant="outlined"
            fullWidth
            name="williamsR_to"
            value={filters.williamsR.to}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.williamsR.from,
                max: FILTER_RANGES.williamsR.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.williamsR.from} to ${FILTER_RANGES.williamsR.to}`}
          />
        </Grid>

        {/* EMA(13) of Williams %R Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="EMA(13) Williams %R From"
            variant="outlined"
            fullWidth
            name="emaWilliamsR_from"
            value={filters.emaWilliamsR.from}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.emaWilliamsR.from,
                max: FILTER_RANGES.emaWilliamsR.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.emaWilliamsR.from} to ${FILTER_RANGES.emaWilliamsR.to}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="EMA(13) Williams %R To"
            variant="outlined"
            fullWidth
            name="emaWilliamsR_to"
            value={filters.emaWilliamsR.to}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.emaWilliamsR.from,
                max: FILTER_RANGES.emaWilliamsR.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.emaWilliamsR.from} to ${FILTER_RANGES.emaWilliamsR.to}`}
          />
        </Grid>

        {/* RSI 14 Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="RSI 14 From"
            variant="outlined"
            fullWidth
            name="rsi14_from"
            value={filters.rsi14.from}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.rsi14.from,
                max: FILTER_RANGES.rsi14.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.rsi14.from} to ${FILTER_RANGES.rsi14.to}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="RSI 14 To"
            variant="outlined"
            fullWidth
            name="rsi14_to"
            value={filters.rsi14.to}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.rsi14.from,
                max: FILTER_RANGES.rsi14.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.rsi14.from} to ${FILTER_RANGES.rsi14.to}`}
          />
        </Grid>

        {/* RSI 21 Filter */}
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="RSI 21 From"
            variant="outlined"
            fullWidth
            name="rsi21_from"
            value={filters.rsi21.from}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.rsi21.from,
                max: FILTER_RANGES.rsi21.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.rsi21.from} to ${FILTER_RANGES.rsi21.to}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            label="RSI 21 To"
            variant="outlined"
            fullWidth
            name="rsi21_to"
            value={filters.rsi21.to}
            onChange={handleChange}
            type="number"
            InputProps={{
              inputProps: {
                min: FILTER_RANGES.rsi21.from,
                max: FILTER_RANGES.rsi21.to,
                step: 0.01,
              },
            }}
            helperText={`Range: ${FILTER_RANGES.rsi21.from} to ${FILTER_RANGES.rsi21.to}`}
          />
        </Grid>

        {/* Reset Button */}
        <Grid item xs={12} sm={6} md={3}>
          <Button variant="contained" color="primary" onClick={handleReset} fullWidth>
            Reset Filters
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Filters;
