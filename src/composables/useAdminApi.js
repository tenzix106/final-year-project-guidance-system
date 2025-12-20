/**
 * Composable for admin API calls
 * Provides reusable functions for admin operations with consistent error handling
 */

import axios from 'axios'
import { ref } from 'vue'
import { API_ENDPOINTS, buildApiUrl } from '../config/api.js'

export function useAdminApi() {
  const loading = ref(false)
  const error = ref(null)

  /**
   * Get authorization headers with token
   * @returns {Object} Headers object with Authorization
   */
  const getAuthHeaders = () => {
    const token = localStorage.getItem('auth_token')
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }

  /**
   * Fetch overview statistics
   * @returns {Promise<Object>} Statistics data
   */
  const fetchOverviewStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(
        buildApiUrl(API_ENDPOINTS.ADMIN.STATS_OVERVIEW),
        { headers: getAuthHeaders() }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch statistics'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch usage statistics
   * @returns {Promise<Object>} Usage data
   */
  const fetchUsageStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(
        buildApiUrl(API_ENDPOINTS.ADMIN.STATS_USAGE),
        { headers: getAuthHeaders() }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch usage statistics'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch users with pagination and filters
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} Users data with pagination
   */
  const fetchUsers = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(
        buildApiUrl(API_ENDPOINTS.ADMIN.USERS),
        { 
          headers: getAuthHeaders(),
          params
        }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch users'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Update user role
   * @param {number} userId - User ID
   * @param {string} role - New role
   * @returns {Promise<Object>} Updated user data
   */
  const updateUserRole = async (userId, role) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch(
        buildApiUrl(API_ENDPOINTS.ADMIN.USER_ROLE(userId)),
        { role },
        { headers: getAuthHeaders() }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to update user role'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch topics with pagination and filters
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} Topics data with pagination
   */
  const fetchTopics = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(
        buildApiUrl(API_ENDPOINTS.ADMIN.TOPICS),
        {
          headers: getAuthHeaders(),
          params
        }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch topics'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Delete a topic
   * @param {number} topicId - Topic ID
   * @returns {Promise<Object>} Response data
   */
  const deleteTopic = async (topicId) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.delete(
        buildApiUrl(API_ENDPOINTS.ADMIN.TOPIC(topicId)),
        { headers: getAuthHeaders() }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to delete topic'
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch AI settings
   * @returns {Promise<Object>} AI settings data
   */
  const fetchAISettings = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(
        buildApiUrl(API_ENDPOINTS.ADMIN.AI_SETTINGS),
        { headers: getAuthHeaders() }
      )
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to fetch AI settings'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    fetchOverviewStats,
    fetchUsageStats,
    fetchUsers,
    updateUserRole,
    fetchTopics,
    deleteTopic,
    fetchAISettings
  }
}
