// frontend/src/pages/NewScan.jsx
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Alert,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  ArrowBack,
  PlayArrow,
} from '@mui/icons-material';
import { scanService } from '../services/api';
import ScanForm from '../components/scans/ScanForm';
import LoadingSpinner from '../components/common/LoadingSpinner';

const NewScan = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [scanCreated, setScanCreated] = useState(false);
  const [createdScan, setCreatedScan] = useState(null);

  const handleCreateScan = async (scanData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await scanService.createScan(scanData);
      setCreatedScan(response.data);
      setScanCreated(true);
      
      // Redirect to scan detail after a short delay
      setTimeout(() => {
        navigate(`/scans/${response.data.id}`);
      }, 2000);
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create scan');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Creating scan..." />;
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1200, margin: '0 auto' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/scans')}
          sx={{ mr: 1 }}
        >
          Back to Scans
        </Button>
        
        <Box sx={{ flex: 1 }}>
          <Typography variant="h4" gutterBottom>
            New Security Scan
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Configure and launch a new security scan for your target website
          </Typography>
        </Box>
      </Box>

      {/* Success Message */}
      {scanCreated && (
        <Alert 
          severity="success" 
          sx={{ mb: 3 }}
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => navigate(`/scans/${createdScan.id}`)}
            >
              View Scan
            </Button>
          }
        >
          Scan created successfully! Redirecting to scan details...
        </Alert>
      )}

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Main Content */}
      <Card elevation={3}>
        <CardContent sx={{ p: 4 }}>
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <PlayArrow 
              sx={{ 
                fontSize: 64, 
                color: 'primary.main',
                mb: 2,
              }} 
            />
            <Typography variant="h5" gutterBottom>
              Configure Your Scan
            </Typography>
            <Typography variant="body1" color="textSecondary">
              Fill out the form below to configure and launch a comprehensive security scan
            </Typography>
          </Box>

          <ScanForm
            onSubmit={handleCreateScan}
            loading={loading}
          />
        </CardContent>
      </Card>

      {/* Information Cards */}
      <Box sx={{ mt: 4, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom color="primary">
              What gets scanned?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Security headers and configurations<br/>
              • SSL/TLS certificate validity<br/>
              • Open ports and services<br/>
              • Common web vulnerabilities<br/>
              • OWASP Top 10 coverage
            </Typography>
          </CardContent>
        </Card>

        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom color="primary">
              Scan Types
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Quick Scan: Basic security checks (2-5 minutes)<br/>
              • Full Scan: Comprehensive analysis (5-15 minutes)<br/>
              • Custom: Configure specific checks as needed
            </Typography>
          </CardContent>
        </Card>

        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom color="primary">
              Best Practices
            </Typography>
            <Typography variant="body2" color="textSecondary">
              • Scan during off-peak hours<br/>
              • Ensure you have permission to scan<br/>
              • Review findings with AI assistance<br/>
              • Export reports for documentation
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default NewScan;