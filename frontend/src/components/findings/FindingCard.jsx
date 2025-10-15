// frontend/src/components/findings/FindingCard.jsx
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Collapse,
  IconButton,
  Alert,
  Button,
} from '@mui/material';
import {
  ExpandMore,
  Code,
  Security,
  OpenInNew,
} from '@mui/icons-material';

const FindingCard = ({ finding, onAnalyze }) => {
  const [expanded, setExpanded] = useState(false);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Chip
                label={finding.severity}
                color={getSeverityColor(finding.severity)}
                size="small"
              />
              <Typography variant="h6" component="div">
                {finding.title}
              </Typography>
            </Box>
            
            <Typography variant="body2" color="textSecondary" paragraph>
              {finding.description}
            </Typography>

            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1 }}>
              {finding.owasp_category && (
                <Chip
                  label={finding.owasp_category}
                  variant="outlined"
                  size="small"
                />
              )}
              {finding.cve_id && (
                <Chip
                  label={finding.cve_id}
                  variant="outlined"
                  size="small"
                  color="error"
                />
              )}
              {finding.location && (
                <Chip
                  label={finding.location}
                  variant="outlined"
                  size="small"
                />
              )}
            </Box>
          </Box>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <IconButton
              onClick={handleExpandClick}
              sx={{
                transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.3s ease',
              }}
            >
              <ExpandMore />
            </IconButton>
            
            <Button
              size="small"
              startIcon={<Code />}
              onClick={() => onAnalyze(finding)}
            >
              AI Analyze
            </Button>
          </Box>
        </Box>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Box sx={{ mt: 2, pt: 2, borderTop: 1, borderColor: 'divider' }}>
            {finding.evidence && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Evidence:
                </Typography>
                <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap', fontSize: '0.75rem' }}>
                  {JSON.stringify(finding.evidence, null, 2)}
                </Typography>
              </Alert>
            )}

            {finding.remediation && (
              <Box>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  Recommended Remediation:
                </Typography>
                <Typography variant="body2">
                  {finding.remediation}
                </Typography>
              </Box>
            )}
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default FindingCard;