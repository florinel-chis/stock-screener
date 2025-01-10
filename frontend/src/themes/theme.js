// src/themes/theme.js

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Customize primary color
    },
    secondary: {
      main: '#dc004e', // Customize secondary color
    },
  },
  typography: {
    h6: {
      fontWeight: 600,
    },
    // Add more typography customizations as needed
  },
  // Customize other theme aspects like spacing, components, etc.
});

export default theme;
