// frontend/src/components/ai/RemediationSteps.jsx
import React from 'react';
import {
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Box,
  Typography,
  Card,
  CardContent,
  Alert,
} from '@mui/material';
import {
  PriorityHigh as CriticalIcon,
  Warning as HighIcon,
  Info as MediumIcon,
  CheckCircle as LowIcon,
  Code as CodeIcon,
} from '@mui/icons-material';

const RemediationSteps = ({ steps, compact = false }) => {
  if (!steps || steps.length === 0) {
    return (
      <Alert severity="info">
        No remediation steps available for this finding.
      </Alert>
    );
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'critical':
        return <CriticalIcon color="error" />;
      case 'high':
        return <HighIcon color="warning" />;
      case 'medium':
        return <MediumIcon color="info" />;
      case 'low':
        return <LowIcon color="success" />;
      default:
        return <MediumIcon color="info" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  return (
    <List dense={compact}>
      {steps.map((step, index) => (
        <ListItem key={index} alignItems="flex-start" sx={{ mb: 1 }}>
          <ListItemIcon sx={{ minWidth: 40, mt: 0.5 }}>
            {getPriorityIcon(step.priority)}
          </ListItemIcon>
          <ListItemText
            primary={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Typography variant="body1" fontWeight="medium">
                  {step.action}
                </Typography>
                <Chip
                  label={step.priority}
                  size="small"
                  color={getPriorityColor(step.priority)}
                  variant="outlined"
                />
              </Box>
            }
            secondary={
              <Box sx={{ mt: 1 }}>
                {step.description && (
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {step.description}
                  </Typography>
                )}
                
                {step.sample_code && (
                  <Card variant="outlined" sx={{ mt: 1, backgroundColor: 'grey.50' }}>
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <CodeIcon fontSize="small" color="action" />
                        <Typography variant="caption" fontWeight="bold" color="text.secondary">
                          {step.sample_code.language}
                        </Typography>
                      </Box>
                      <Typography
                        component="pre"
                        variant="caption"
                        sx={{
                          fontFamily: 'monospace',
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-all',
                          m: 0,
                          lineHeight: 1.4,
                        }}
                      >
                        {step.sample_code.code}
                      </Typography>
                    </CardContent>
                  </Card>
                )}
                
                {step.references && step.references.length > 0 && (
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="caption" fontWeight="bold" color="text.secondary">
                      References:
                    </Typography>
                    <List dense sx={{ listStyleType: 'disc', pl: 2 }}>
                      {step.references.map((ref, refIndex) => (
                        <ListItem key={refIndex} sx={{ display: 'list-item', p: 0, pl: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            {ref}
                          </Typography>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </Box>
            }
          />
        </ListItem>
      ))}
    </List>
  );
};

export default RemediationSteps;