// frontend/src/services/scanService.js
import api from './api';

export const scanService = {
  // Get all scans
  getScans: () => api.get('/api/v1/scans/'),
  
  // Get single scan
  getScan: (id) => api.get(`/api/v1/scans/${id}`),
  
  // Create new scan
  createScan: (data) => api.post('/api/v1/scans/', data),
  
  // Delete scan
  deleteScan: (id) => api.delete(`/api/v1/scans/${id}`),
  
  // Get scan findings
  getScanFindings: (id) => api.get(`/api/v1/scans/${id}/findings`),
  
  // Stop running scan
  stopScan: (id) => api.post(`/api/v1/scans/${id}/stop`),
  
  // Export scan report
  exportReport: (id, format = 'json') => 
    api.get(`/api/v1/scans/${id}/export`, { 
      params: { format },
      responseType: 'blob'
    }),
};

export default scanService;