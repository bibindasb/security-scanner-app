// frontend/src/pages/Settings.jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Grid,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from '@mui/material';
import { Save, Security, Api, Notifications } from '@mui/icons-material';

const Settings = () => {
  const [settings, setSettings] = useState({
    // AI Settings
    aiProvider: 'ollama',
    ollamaUrl: 'http://localhost:11434',
    openaiApiKey: '',
    openrouteApiKey: '',
    
    // Scan Settings
    maxScanDuration: 300,
    userAgent: 'SecurityScanner/1.0',
    enablePassiveScan: true,
    enableActiveScan: true,
    
    // Notification Settings
    emailNotifications: false,
    slackNotifications: false,
    webhookUrl: '',
  });

  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Load settings from localStorage or API
    const savedSettings = localStorage.getItem('scannerSettings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  const handleSave = () => {
    localStorage.setItem('scannerSettings', JSON.stringify(settings));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1000, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Settings saved successfully!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* AI Settings */}
        <Grid item xs={12}>
          <Card elevation={2}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Security color="primary" />
                <Typography variant="h6">AI Analysis Settings</Typography>
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>AI Provider</InputLabel>
                    <Select
                      value={settings.aiProvider}
                      label="AI Provider"
                      onChange={(e) => handleChange('aiProvider', e.target.value)}
                    >
                      <MenuItem value="ollama">Ollama (Local)</MenuItem>
                      <MenuItem value="openai">OpenAI</MenuItem>
                      <MenuItem value="openroute">OpenRoute</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                {settings.aiProvider === 'ollama' && (
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Ollama Base URL"
                      value={settings.ollamaUrl}
                      onChange={(e) => handleChange('ollamaUrl', e.target.value)}
                      helperText="URL where Ollama is running"
                    />
                  </Grid>
                )}

                {settings.aiProvider === 'openai' && (
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="OpenAI API Key"
                      type="password"
                      value={settings.openaiApiKey}
                      onChange={(e) => handleChange('openaiApiKey', e.target.value)}
                      helperText="Your OpenAI API key for remote analysis"
                    />
                  </Grid>
                )}

                {settings.aiProvider === 'openroute' && (
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="OpenRoute API Key"
                      type="password"
                      value={settings.openrouteApiKey}
                      onChange={(e) => handleChange('openrouteApiKey', e.target.value)}
                      helperText="Your OpenRoute API key for remote analysis"
                    />
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Scan Settings */}
        <Grid item xs={12}>
          <Card elevation={2}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Api color="primary" />
                <Typography variant="h6">Scan Settings</Typography>
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Max Scan Duration (seconds)"
                    type="number"
                    value={settings.maxScanDuration}
                    onChange={(e) => handleChange('maxScanDuration', parseInt(e.target.value))}
                    helperText="Maximum time allowed for a scan to complete"
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="User Agent"
                    value={settings.userAgent}
                    onChange={(e) => handleChange('userAgent', e.target.value)}
                    helperText="User agent string used for scanning"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.enablePassiveScan}
                        onChange={(e) => handleChange('enablePassiveScan', e.target.checked)}
                      />
                    }
                    label="Enable Passive Scanning"
                  />
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.enableActiveScan}
                        onChange={(e) => handleChange('enableActiveScan', e.target.checked)}
                      />
                    }
                    label="Enable Active Scanning"
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Notification Settings */}
        <Grid item xs={12}>
          <Card elevation={2}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Notifications color="primary" />
                <Typography variant="h6">Notification Settings</Typography>
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.emailNotifications}
                        onChange={(e) => handleChange('emailNotifications', e.target.checked)}
                      />
                    }
                    label="Email Notifications"
                  />
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.slackNotifications}
                        onChange={(e) => handleChange('slackNotifications', e.target.checked)}
                      />
                    }
                    label="Slack Notifications"
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Webhook URL"
                    value={settings.webhookUrl}
                    onChange={(e) => handleChange('webhookUrl', e.target.value)}
                    helperText="Webhook URL for scan completion notifications"
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Save Button */}
      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={handleSave}
          size="large"
        >
          Save Settings
        </Button>
      </Box>
    </Box>
  );
};

export default Settings;