// frontend/src/components/findings/SeverityChip.jsx
import React from 'react';
import { Chip, Tooltip } from '@mui/material';
import {
  Error as CriticalIcon,
  Warning as HighIcon,
  Info as MediumIcon,
  CheckCircle as LowIcon,
  Help as InfoIcon,
} from '@mui/icons-material';

const SeverityChip = ({ severity, count, size = 'small' }) => {
  const getSeverityConfig = (severity) => {
    const configs = {
      critical: {
        icon: <CriticalIcon />,
        color: 'error',
        label: 'Critical',
        description: 'Immediate action required - severe security risk',
      },
      high: {
        icon: <HighIcon />,
        color: 'warning',
        label: 'High',
        description: 'High priority - significant security risk',
      },
      medium: {
        icon: <MediumIcon />,
        color: 'info',
        label: 'Medium',
        description: 'Medium priority - moderate security risk',
      },
      low: {
        icon: <LowIcon />,
        color: 'success',
        label: 'Low',
        description: 'Low priority - minor security risk',
      },
      info: {
        icon: <InfoIcon />,
        color: 'default',
        label: 'Info',
        description: 'Informational finding - no immediate risk',
      },
    };

    return configs[severity] || configs.info;
  };

  const config = getSeverityConfig(severity);
  const label = count !== undefined ? `${config.label} (${count})` : config.label;

  return (
    <Tooltip title={config.description}>
      <Chip
        icon={config.icon}
        label={label}
        size={size}
        color={config.color}
        variant="filled"
        sx={{
          fontWeight: 'bold',
          '& .MuiChip-icon': {
            color: 'inherit !important',
          },
        }}
      />
    </Tooltip>
  );
};

export default SeverityChip;