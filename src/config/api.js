/**
 * Centralized API configuration
 * Provides consistent API base URL across the application
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

/**
 * API endpoints configuration
 */
export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me',
    GOOGLE_LOGIN: '/api/auth/google/login',
    COMPLETE_ONBOARDING: '/api/auth/complete-onboarding',
    UPDATE_PROFILE: '/api/auth/profile'
  },
  
  // Admin endpoints
  ADMIN: {
    STATS_OVERVIEW: '/api/admin/stats/overview',
    STATS_USAGE: '/api/admin/stats/usage',
    USERS: '/api/admin/users',
    USER_ROLE: (userId) => `/api/admin/users/${userId}/role`,
    TOPICS: '/api/admin/topics',
    TOPIC: (topicId) => `/api/admin/topics/${topicId}`,
    AI_SETTINGS: '/api/admin/settings/ai'
  }
}

/**
 * Helper function to build full API URL
 * @param {string} endpoint - The API endpoint path
 * @returns {string} Full API URL
 */
export const buildApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`
}
