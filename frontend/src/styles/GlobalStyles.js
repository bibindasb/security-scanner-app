// frontend/src/styles/GlobalStyles.js
import { GlobalStyles as MUIGlobalStyles } from '@mui/material';

export const GlobalStyles = () => (
  <MUIGlobalStyles
    styles={{
      '*': {
        boxSizing: 'border-box',
        margin: 0,
        padding: 0,
      },
      html: {
        WebkitFontSmoothing: 'antialiased',
        MozOsxFontSmoothing: 'grayscale',
        height: '100%',
      },
      body: {
        height: '100%',
        backgroundColor: '#f5f5f5',
      },
      '#root': {
        height: '100%',
      },
      '.MuiCard-root:hover': {
        transition: 'all 0.3s ease-in-out',
      },
    }}
  />
);