/**
 * Global error handling composable
 * Provides consistent error handling and user-friendly error messages
 */

import { ref } from 'vue'

export function useErrorHandler() {
  const error = ref(null)
  const isError = ref(false)

  /**
   * Extract user-friendly error message from error object
   * @param {Error|Object} err - Error object
   * @returns {string} User-friendly error message
   */
  const getErrorMessage = (err) => {
    // Axios error response
    if (err.response) {
      // Check for specific error messages from backend
      if (err.response.data?.message) {
        return err.response.data.message
      }
      if (err.response.data?.msg) {
        return err.response.data.msg
      }
      
      // HTTP status code based messages
      switch (err.response.status) {
        case 400:
          return 'Invalid request. Please check your input and try again.'
        case 401:
          return 'Authentication required. Please log in and try again.'
        case 403:
          return 'You don\'t have permission to perform this action.'
        case 404:
          return 'The requested resource was not found.'
        case 422:
          return 'Validation error. Please check your input.'
        case 500:
          return 'Server error. Please try again later.'
        default:
          return `Error: ${err.response.status} - ${err.response.statusText}`
      }
    }

    // Network error
    if (err.request) {
      return 'Network error. Please check your internet connection and try again.'
    }

    // Error with message
    if (err.message) {
      return err.message
    }

    // Fallback
    return 'An unexpected error occurred. Please try again.'
  }

  /**
   * Handle error and set error state
   * @param {Error|Object} err - Error object
   * @param {string} fallbackMessage - Optional fallback message
   */
  const handleError = (err, fallbackMessage = null) => {
    const message = fallbackMessage || getErrorMessage(err)
    error.value = message
    isError.value = true
    console.error('Error handled:', err)
  }

  /**
   * Clear error state
   */
  const clearError = () => {
    error.value = null
    isError.value = false
  }

  /**
   * Wrap async function with error handling
   * @param {Function} fn - Async function to wrap
   * @param {string} fallbackMessage - Optional fallback message
   * @returns {Function} Wrapped function
   */
  const withErrorHandling = (fn, fallbackMessage = null) => {
    return async (...args) => {
      try {
        clearError()
        return await fn(...args)
      } catch (err) {
        handleError(err, fallbackMessage)
        throw err
      }
    }
  }

  return {
    error,
    isError,
    handleError,
    clearError,
    getErrorMessage,
    withErrorHandling
  }
}
