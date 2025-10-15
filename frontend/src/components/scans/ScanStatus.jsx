// frontend/src/components/scans/ScanStatus.jsx
import React from 'react';
import { Chip, LinearProgress, Box, Tooltip } from '@mui/material';
import {
  CheckCircle,
  Error,
  Schedule,
  PlayArrow,
} from '@mui/icons-material';

const ScanStatus = ({ status, progress, size = 'medium' }) => {
  const getStatusConfig = (status) => {
    switch (status) {
      case 'completed':
        return {
          icon: <CheckCircle />,
          color: 'success',
          label: 'Completed',
        };
      case 'running':
        return {
          icon: <PlayArrow />,
          color: 'primary',
          label: 'Running',
        };
      case 'failed':
        return {
          icon: <Error />,
          color: 'error',
          label: 'Failed',
        };
      case 'pending':
        return {
          icon: <Schedule />,
          color: 'default',
          label: 'Pending',
        };
      default:
        return {
          icon: <Schedule />,
          color: 'default',
          label: status,
        };
    }
  };

  const config = getStatusConfig(status);

  if (status === 'running' && progress !== undefined) {
    return (
      <Tooltip title={`${progress}% complete`}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 120 }}>
          <LinearProgress 
            variant="determinate" 
            value={progress} 
            sx={{ flexGrow: 1 }}
          />
          <Chip
            icon={config.icon}
            label={`${progress}%`}
            size={size}
            color={config.color}
            variant="outlined"
          />
        </Box>
      </Tooltip>
    );
  }

  return (
    <Chip
      icon={config.icon}
      label={config.label}
      size={size}
      color={config.color}
      variant={status === 'running' ? 'outlined' : 'filled'}
    />
  );
};

export default ScanStatus;