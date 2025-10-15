// frontend/src/services/aiService.js
import api from './api';

export const aiService = {
  // Analyze scan findings
  analyzeScan: (scanId, provider = 'openrouter', model = null) => 
    api.post('/api/v1/ai/analyze', { 
      scan_id: scanId, 
      provider,
      model
    }),
  
  // Get existing analysis
  getAnalysis: (scanId) => 
    api.get(`/api/v1/ai/analysis/${scanId}`),
  
  // Analyze single finding
  analyzeFinding: (findingId, provider = 'openrouter', model = null) =>
    api.post('/api/v1/ai/analyze/finding', {
      finding_id: findingId,
      provider,
      model
    }),
  
  // Get available AI providers and models
  getProviders: () => api.get('/api/v1/ai/providers'),
  
  // Get available AI models (legacy endpoint)
  getModels: () => api.get('/api/v1/ai/providers'),
};

export default aiService;