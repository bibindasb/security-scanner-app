// frontend/src/components/scans/ScanForm.jsx
import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Box,
  Stepper,
  Step,
  StepLabel,
  Alert,
} from '@mui/material';

const scanTypes = [
  { value: 'full', label: 'Full Scan' },
  { value: 'quick', label: 'Quick Scan' },
  { value: 'headers', label: 'Headers Only' },
  { value: 'ssl', label: 'SSL/TLS Only' },
  { value: 'ports', label: 'Port Scan Only' },
];

const ScanForm = ({ open, onClose, onSubmit, loading }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    target_url: '',
    scan_type: 'quick',
    options: {
      check_headers: true,
      check_ssl: true,
      check_ports: true,
      check_vulnerabilities: true,
      depth: 'medium',
    },
  });

  const steps = ['Target', 'Scan Type', 'Options'];

  const handleNext = () => {
    setActiveStep((prev) => prev + 1);
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const handleSubmit = () => {
    onSubmit(formData);
  };

  const updateFormData = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const updateOptions = (field, value) => {
    setFormData(prev => ({
      ...prev,
      options: {
        ...prev.options,
        [field]: value,
      },
    }));
  };

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <TextField
            fullWidth
            label="Target URL"
            value={formData.target_url}
            onChange={(e) => updateFormData('target_url', e.target.value)}
            placeholder="https://example.com"
            required
            helperText="Enter the full URL including protocol (http:// or https://)"
          />
        );
      case 1:
        return (
          <FormControl fullWidth>
            <InputLabel>Scan Type</InputLabel>
            <Select
              value={formData.scan_type}
              label="Scan Type"
              onChange={(e) => updateFormData('scan_type', e.target.value)}
            >
              {scanTypes.map((type) => (
                <MenuItem key={type.value} value={type.value}>
                  {type.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      case 2:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.options.check_headers}
                    onChange={(e) => updateOptions('check_headers', e.target.checked)}
                  />
                }
                label="Check Security Headers"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.options.check_ssl}
                    onChange={(e) => updateOptions('check_ssl', e.target.checked)}
                  />
                }
                label="Check SSL/TLS Configuration"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.options.check_ports}
                    onChange={(e) => updateOptions('check_ports', e.target.checked)}
                  />
                }
                label="Scan Common Ports"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.options.check_vulnerabilities}
                    onChange={(e) => updateOptions('check_vulnerabilities', e.target.checked)}
                  />
                }
                label="Check for Common Vulnerabilities"
              />
            </FormGroup>
            
            <FormControl fullWidth>
              <InputLabel>Scan Depth</InputLabel>
              <Select
                value={formData.options.depth}
                label="Scan Depth"
                onChange={(e) => updateOptions('depth', e.target.value)}
              >
                <MenuItem value="quick">Quick</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="deep">Deep</MenuItem>
              </Select>
            </FormControl>
          </Box>
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        New Security Scan
      </DialogTitle>
      
      <DialogContent>
        <Stepper activeStep={activeStep} sx={{ mb: 3 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {getStepContent(activeStep)}
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        
        <Box sx={{ flex: 1 }} />
        
        {activeStep > 0 && (
          <Button onClick={handleBack} disabled={loading}>
            Back
          </Button>
        )}
        
        {activeStep < steps.length - 1 ? (
          <Button 
            onClick={handleNext} 
            variant="contained"
            disabled={!formData.target_url}
          >
            Next
          </Button>
        ) : (
          <Button 
            onClick={handleSubmit} 
            variant="contained"
            disabled={!formData.target_url || loading}
          >
            Start Scan
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default ScanForm;