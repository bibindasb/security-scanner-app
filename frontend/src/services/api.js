// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const scanService = {
  getScans: () => api.get('/api/v1/scans/'),
  getScan: (id) => api.get(`/api/v1/scans/${id}`),
  createScan: (data) => api.post('/api/v1/scans/', data),
  deleteScan: (id) => api.delete(`/api/v1/scans/${id}`),
  getScanFindings: (id) => api.get(`/api/v1/scans/${id}/findings`),
};

export const aiService = {
  analyzeScan: (scanId, provider = 'ollama') => 
    api.post('/api/v1/ai/analyze', { scan_id: scanId, provider }),
  getAnalysis: (scanId) => 
    api.get(`/api/v1/ai/analysis/${scanId}`),
};

export const authService = {
  login: (credentials) => api.post('/api/v1/auth/login', credentials),
  logout: () => api.post('/api/v1/auth/logout'),
  refresh: () => api.post('/api/v1/auth/refresh'),
};

export default api;