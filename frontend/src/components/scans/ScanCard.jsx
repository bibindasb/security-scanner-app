// frontend/src/components/scans/ScanCard.jsx
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Delete,
  Visibility,
  Warning,
  CheckCircle,
  Error,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const ScanCard = ({ scan, onDelete, onStop }) => {
  const navigate = useNavigate();

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle color="success" />;
      case 'running':
        return <LinearProgress size={20} />;
      case 'failed':
        return <Error color="error" />;
      default:
        return <Warning color="warning" />;
    }
  };

  const getSeverityCounts = () => {
    const counts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
    scan.findings?.forEach(finding => {
      counts[finding.severity] = (counts[finding.severity] || 0) + 1;
    });
    return counts;
  };

  const severityCounts = getSeverityCounts();

  return (
    <Card
      sx={{
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6" component="div" noWrap sx={{ maxWidth: '70%' }}>
            {scan.target_url}
          </Typography>
          <Chip
            label={scan.status}
            size="small"
            color={
              scan.status === 'completed' ? 'success' :
              scan.status === 'running' ? 'primary' :
              scan.status === 'failed' ? 'error' : 'default'
            }
          />
        </Box>

        <Typography color="textSecondary" variant="body2" gutterBottom>
          {new Date(scan.created_at).toLocaleString()}
        </Typography>

        {scan.findings && (
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {Object.entries(severityCounts).map(([severity, count]) => (
              count > 0 && (
                <Chip
                  key={severity}
                  label={`${count} ${severity}`}
                  size="small"
                  color={
                    severity === 'critical' ? 'error' :
                    severity === 'high' ? 'warning' :
                    severity === 'medium' ? 'info' :
                    'default'
                  }
                  variant="outlined"
                />
              )
            ))}
          </Box>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2, gap: 1 }}>
          <IconButton
            size="small"
            onClick={() => navigate(`/scans/${scan.id}`)}
            color="primary"
          >
            <Visibility />
          </IconButton>
          
          {scan.status === 'running' && (
            <IconButton size="small" onClick={() => onStop(scan.id)} color="warning">
              <Stop />
            </IconButton>
          )}
          
          <IconButton size="small" onClick={() => onDelete(scan.id)} color="error">
            <Delete />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ScanCard;