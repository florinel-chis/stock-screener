// src/components/StockDetailDialog.js

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Typography,
  Grid,
} from '@mui/material';

const StockDetailDialog = ({ open, handleClose, stock }) => {
  if (!stock) return null;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>{stock.Symbol} Details</DialogTitle>
      <DialogContent dividers>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography variant="subtitle1">Date:</Typography>
            <Typography variant="body1">{stock.Date}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">Close Price:</Typography>
            <Typography variant="body1">${stock.Close.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">Williams %R (21):</Typography>
            <Typography variant="body1">{stock.Williams_R_21.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">EMA(13) of Williams %R:</Typography>
            <Typography variant="body1">{stock.EMA_13_Williams_R.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">RSI 14:</Typography>
            <Typography variant="body1">{stock.RSI_14.toFixed(2)}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle1">RSI 21:</Typography>
            <Typography variant="body1">{stock.RSI_21.toFixed(2)}</Typography>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} variant="contained" color="primary">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default StockDetailDialog;
