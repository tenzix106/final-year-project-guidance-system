/**
 * Loading state management composable
 * Provides consistent loading state handling across components
 */

import { ref } from 'vue'

export function useLoading() {
  const isLoading = ref(false)
  const loadingMessage = ref('')

  /**
   * Start loading state
   * @param {string} message - Optional loading message
   */
  const startLoading = (message = 'Loading...') => {
    isLoading.value = true
    loadingMessage.value = message
  }

  /**
   * Stop loading state
   */
  const stopLoading = () => {
    isLoading.value = false
    loadingMessage.value = ''
  }

  /**
   * Wrap async function with automatic loading state management
   * @param {Function} fn - Async function to wrap
   * @param {string} message - Optional loading message
   * @returns {Function} Wrapped function
   */
  const withLoading = (fn, message = 'Loading...') => {
    return async (...args) => {
      startLoading(message)
      try {
        return await fn(...args)
      } finally {
        stopLoading()
      }
    }
  }

  return {
    isLoading,
    loadingMessage,
    startLoading,
    stopLoading,
    withLoading
  }
}
