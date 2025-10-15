// frontend/src/components/ai/AIAnalysisCard.jsx
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Alert,
  LinearProgress,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  SmartToy,
  ExpandMore,
  Code,
  PriorityHigh,
} from '@mui/icons-material';

const AIAnalysisCard = ({ analysis, loading }) => {
  const [expanded, setExpanded] = React.useState(false);

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <SmartToy color="primary" />
            <Typography variant="h6">AI Analysis</Typography>
            <LinearProgress sx={{ flex: 1 }} />
          </Box>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            Analyzing findings and generating remediation suggestions...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (!analysis) {
    return null;
  }

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <SmartToy color="primary" />
          <Typography variant="h6">AI-Powered Analysis</Typography>
          <Chip label={analysis.provider} size="small" variant="outlined" />
          <Box sx={{ flex: 1 }} />
          <IconButton
            onClick={() => setExpanded(!expanded)}
            sx={{
              transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
              transition: 'transform 0.3s ease',
            }}
          >
            <ExpandMore />
          </IconButton>
        </Box>

        {analysis.error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {analysis.error}
          </Alert>
        )}

        <Typography variant="body1" paragraph>
          {analysis.analysis?.summary || 'No summary available.'}
        </Typography>

        <Collapse in={expanded}>
          {analysis.analysis?.prioritized_remediation?.map((item, index) => (
            <Alert
              key={index}
              severity={
                item.priority === 'critical' ? 'error' :
                item.priority === 'high' ? 'warning' :
                item.priority === 'medium' ? 'info' : 'success'
              }
              sx={{ mb: 1 }}
              icon={<PriorityHigh />}
            >
              <Typography variant="subtitle2" gutterBottom>
                {item.action}
              </Typography>
              
              {item.sample_code && (
                <Box sx={{ mt: 1, p: 1, backgroundColor: 'background.paper', borderRadius: 1 }}>
                  <Typography variant="caption" color="textSecondary">
                    {item.sample_code.language}:
                  </Typography>
                  <Typography
                    component="pre"
                    sx={{
                      fontSize: '0.75rem',
                      whiteSpace: 'pre-wrap',
                      mt: 0.5,
                      fontFamily: 'monospace',
                    }}
                  >
                    {item.sample_code.code}
                  </Typography>
                </Box>
              )}
            </Alert>
          ))}

          {analysis.analysis?.additional_recommendations?.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Additional Recommendations:
              </Typography>
              {analysis.analysis.additional_recommendations.map((rec, index) => (
                <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
                  • {rec}
                </Typography>
              ))}
            </Box>
          )}
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default AIAnalysisCard;