// frontend/src/services/authService.js
import api from './api';

export const authService = {
  // Login user
  login: (credentials) => 
    api.post('/api/v1/auth/login', credentials),
  
  // Logout user
  logout: () => 
    api.post('/api/v1/auth/logout'),
  
  // Refresh token
  refresh: () => 
    api.post('/api/v1/auth/refresh'),
  
  // Get current user
  getCurrentUser: () => 
    api.get('/api/v1/auth/me'),
  
  // Update user profile
  updateProfile: (data) => 
    api.put('/api/v1/auth/profile', data),
  
  // Change password
  changePassword: (data) => 
    api.post('/api/v1/auth/change-password', data),
};

export default authService;