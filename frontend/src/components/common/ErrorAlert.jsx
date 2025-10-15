// frontend/src/components/common/ErrorAlert.jsx
import React from 'react';
import { Alert, AlertTitle, Button, Box } from '@mui/material';
import { Refresh } from '@mui/icons-material';

const ErrorAlert = ({ error, onRetry, retryable = true }) => {
  return (
    <Alert
      severity="error"
      action={
        retryable && onRetry && (
          <Button color="inherit" size="small" onClick={onRetry} startIcon={<Refresh />}>
            Retry
          </Button>
        )
      }
    >
      <AlertTitle>Error</AlertTitle>
      {error?.message || 'An unexpected error occurred'}
    </Alert>
  );
};

export default ErrorAlert;