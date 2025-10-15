// frontend/src/services/aiService.js
import api from './api';

export const aiService = {
  // Analyze scan findings
  analyzeScan: (scanId, provider = 'ollama') => 
    api.post('/api/v1/ai/analyze', { 
      scan_id: scanId, 
      provider 
    }),
  
  // Get existing analysis
  getAnalysis: (scanId) => 
    api.get(`/api/v1/ai/analysis/${scanId}`),
  
  // Analyze single finding
  analyzeFinding: (findingId, provider = 'ollama') =>
    api.post('/api/v1/ai/analyze/finding', {
      finding_id: findingId,
      provider
    }),
  
  // Get available AI models
  getModels: () => api.get('/api/v1/ai/models'),
};

export default aiService;