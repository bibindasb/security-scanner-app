// frontend/src/pages/ScanList.jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
} from '@mui/material';
import { Add, Search } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { scanService } from '../services/api';
import ScanCard from '../components/scans/ScanCard';
import ScanForm from '../components/scans/ScanForm';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/ErrorAlert';

const ScanList = () => {
  const navigate = useNavigate();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showScanForm, setShowScanForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadScans();
  }, []);

  const loadScans = async () => {
    try {
      setLoading(true);
      const response = await scanService.getScans();
      setScans(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateScan = async (scanData) => {
    try {
      await scanService.createScan(scanData);
      setShowScanForm(false);
      loadScans(); // Refresh the list
    } catch (err) {
      setError(err);
    }
  };

  const handleDeleteScan = async (scanId) => {
    if (window.confirm('Are you sure you want to delete this scan?')) {
      try {
        await scanService.deleteScan(scanId);
        loadScans();
      } catch (err) {
        setError(err);
      }
    }
  };

  const filteredScans = scans.filter(scan => {
    const matchesSearch = scan.target_url.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || scan.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return <LoadingSpinner message="Loading scans..." />;
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4">Security Scans</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setShowScanForm(true)}
        >
          New Scan
        </Button>
      </Box>

      {/* Filters */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <TextField
          placeholder="Search scans..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: <Search sx={{ color: 'text.secondary', mr: 1 }} />,
          }}
          sx={{ minWidth: 200 }}
        />
        
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={statusFilter}
            label="Status"
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <MenuItem value="all">All Status</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="running">Running</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="failed">Failed</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Error Alert */}
      {error && (
        <ErrorAlert error={error} onRetry={loadScans} sx={{ mb: 3 }} />
      )}

      {/* Scans Grid */}
      {filteredScans.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="textSecondary" gutterBottom>
            No scans found
          </Typography>
          <Typography color="textSecondary" sx={{ mb: 3 }}>
            {scans.length === 0 
              ? 'Get started by running your first security scan.'
              : 'No scans match your current filters.'
            }
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setShowScanForm(true)}
          >
            Start First Scan
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {filteredScans.map((scan) => (
            <Grid item xs={12} sm={6} md={4} key={scan.id}>
              <ScanCard
                scan={scan}
                onDelete={handleDeleteScan}
                onStop={() => {/* Implement stop functionality */}}
              />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Scan Form Dialog */}
      <ScanForm
        open={showScanForm}
        onClose={() => setShowScanForm(false)}
        onSubmit={handleCreateScan}
        loading={false}
      />
    </Box>
  );
};

export default ScanList;