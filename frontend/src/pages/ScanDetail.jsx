// frontend/src/pages/ScanDetail.jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  Tabs,
  Tab,
  Alert,
  LinearProgress,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowBack,
  SmartToy,
  Download,
  Refresh,
} from '@mui/icons-material';
import { scanService, aiService } from '../services/api';
import FindingList from '../components/findings/FindingList';
import AIAnalysisCard from '../components/ai/AIAnalysisCard';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/ErrorAlert';

const ScanDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [scan, setScan] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    loadScan();
  }, [id]);

  const loadScan = async () => {
    try {
      setLoading(true);
      const [scanResponse, analysisResponse] = await Promise.all([
        scanService.getScan(id),
        aiService.getAnalysis(id).catch(() => null), // Optional
      ]);
      
      setScan(scanResponse.data);
      setAiAnalysis(analysisResponse?.data || null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeFindings = async () => {
    try {
      setAnalyzing(true);
      const response = await aiService.analyzeScan(id);
      setAiAnalysis(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleAnalyzeFinding = async (finding) => {
    // Implement single finding analysis
    console.log('Analyze single finding:', finding);
  };

  const handleDownloadReport = () => {
    // Implement report download
    console.log('Download report for scan:', id);
  };

  if (loading) {
    return <LoadingSpinner message="Loading scan details..." />;
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <ErrorAlert error={error} onRetry={loadScan} />
      </Box>
    );
  }

  if (!scan) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="warning">Scan not found</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/scans')}
          sx={{ mr: 1 }}
        >
          Back
        </Button>
        
        <Box sx={{ flex: 1 }}>
          <Typography variant="h4" gutterBottom>
            {scan.target_url}
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Chip
              label={scan.status}
              color={
                scan.status === 'completed' ? 'success' :
                scan.status === 'running' ? 'primary' :
                scan.status === 'failed' ? 'error' : 'default'
              }
            />
            <Typography variant="body2" color="textSecondary">
              Started: {new Date(scan.created_at).toLocaleString()}
            </Typography>
            {scan.completed_at && (
              <Typography variant="body2" color="textSecondary">
                Completed: {new Date(scan.completed_at).toLocaleString()}
              </Typography>
            )}
          </Box>
        </Box>

        <Button
          startIcon={<Download />}
          onClick={handleDownloadReport}
          variant="outlined"
        >
          Export
        </Button>
        
        <Button
          startIcon={<Refresh />}
          onClick={loadScan}
          variant="outlined"
        >
          Refresh
        </Button>
      </Box>

      {/* Stats Overview */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Findings
              </Typography>
              <Typography variant="h4">
                {scan.findings?.length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical
              </Typography>
              <Typography variant="h4" color="error.main">
                {scan.findings?.filter(f => f.severity === 'critical').length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                High
              </Typography>
              <Typography variant="h4" color="warning.main">
                {scan.findings?.filter(f => f.severity === 'high').length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                AI Analysis
              </Typography>
              <Typography variant="h4" color="primary.main">
                {aiAnalysis ? 'Ready' : 'Pending'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Card>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Findings" />
          <Tab label="AI Analysis" />
          <Tab label="Scan Details" />
        </Tabs>

        <CardContent>
          {activeTab === 0 && (
            <FindingList
              findings={scan.findings || []}
              onAnalyzeFinding={handleAnalyzeFinding}
            />
          )}

          {activeTab === 1 && (
            <Box>
              {!aiAnalysis && (
                <Alert 
                  severity="info" 
                  action={
                    <Button
                      color="inherit"
                      size="small"
                      onClick={handleAnalyzeFindings}
                      disabled={analyzing}
                      startIcon={<SmartToy />}
                    >
                      {analyzing ? 'Analyzing...' : 'Analyze'}
                    </Button>
                  }
                  sx={{ mb: 3 }}
                >
                  No AI analysis available. Click to analyze findings.
                </Alert>
              )}
              
              <AIAnalysisCard
                analysis={aiAnalysis}
                loading={analyzing}
              />
            </Box>
          )}

          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Scan Configuration
              </Typography>
              <Typography variant="body2" component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                {JSON.stringify(scan.scan_config, null, 2)}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default ScanDetail;