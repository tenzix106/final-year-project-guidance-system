import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Reactive user state
const currentUser = ref(null)
const authToken = ref(localStorage.getItem('auth_token'))

// Computed properties
const isAuthenticated = computed(() => !!authToken.value && !!currentUser.value)
const isLoading = ref(false)

class AuthService {
  constructor() {
    // Try to restore user on service initialization
    this.initializeAuth()
  }

  async initializeAuth() {
    // Check for OAuth callback token in URL
    const urlParams = new URLSearchParams(window.location.search)
    const oauthToken = urlParams.get('token')
    const oauthError = urlParams.get('error')
    
    if (oauthToken) {
      // Store OAuth token and fetch user
      authToken.value = oauthToken
      localStorage.setItem('auth_token', oauthToken)
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname)
      await this.fetchCurrentUser()
      return
    }
    
    if (oauthError) {
      // Clean URL and show error
      window.history.replaceState({}, document.title, window.location.pathname)
      console.error('OAuth error:', oauthError)
      return
    }
    
    // Regular token restoration
    const token = localStorage.getItem('auth_token')
    if (token) {
      authToken.value = token
      try {
        await this.fetchCurrentUser()
      } catch (error) {
        // Token might be expired, clear it
        this.logout()
      }
    }
  }

  getAuthHeaders() {
    const headers = { 'Content-Type': 'application/json' }
    if (authToken.value) {
      headers['Authorization'] = `Bearer ${authToken.value}`
    }
    return headers
  }

  async register(email, password) {
    isLoading.value = true
    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      
      if (!resp.ok) {
        const err = await this.safeJson(resp)
        throw new Error(err?.message || 'Registration failed')
      }
      
      const data = await resp.json()
      return data
    } finally {
      isLoading.value = false
    }
  }

  async login(email, password) {
    isLoading.value = true
    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      
      if (!resp.ok) {
        const err = await this.safeJson(resp)
        throw new Error(err?.message || 'Invalid credentials')
      }
      
      const data = await resp.json()
      if (data?.access_token) {
        authToken.value = data.access_token
        localStorage.setItem('auth_token', data.access_token)
        await this.fetchCurrentUser()
      }
      
      return data
    } finally {
      isLoading.value = false
    }
  }

  async fetchCurrentUser() {
    if (!authToken.value) return null
    
    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/me`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      })
      
      if (!resp.ok) {
        const err = await this.safeJson(resp)
        throw new Error(err?.message || 'Failed to fetch user')
      }
      
      const userData = await resp.json()
      currentUser.value = userData
      return userData
    } catch (error) {
      // If fetching user fails, clear auth state
      this.logout()
      throw error
    }
  }

  logout() {
    authToken.value = null
    currentUser.value = null
    localStorage.removeItem('auth_token')
  }

  async completeOnboarding() {
    if (!authToken.value) {
      throw new Error('Not authenticated')
    }
    
    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/complete-onboarding`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })
      
      if (!resp.ok) {
        const err = await this.safeJson(resp)
        throw new Error(err?.message || 'Failed to complete onboarding')
      }
      
      // Update local user state
      if (currentUser.value) {
        currentUser.value.onboarding_completed = true
      }
      
      return await resp.json()
    } catch (error) {
      console.error('Complete onboarding error:', error)
      throw error
    }
  }

  async updateProfile(profileData) {
    if (!authToken.value) {
      throw new Error('Not authenticated')
    }
    
    try {
      console.log('Updating profile with token:', authToken.value ? 'Token present' : 'No token')
      console.log('Profile data:', profileData)
      
      const resp = await fetch(`${API_BASE_URL}/api/auth/profile`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(profileData)
      })
      
      console.log('Response status:', resp.status, resp.statusText)
      
      if (!resp.ok) {
        const err = await this.safeJson(resp)
        console.error('Backend error response:', err)
        throw new Error(err?.message || `Failed to update profile (${resp.status})`)
      }
      
      const data = await resp.json()
      
      // Update local user state with new data
      if (data.user) {
        currentUser.value = data.user
      }
      
      return data
    } catch (error) {
      console.error('Update profile error:', error)
      throw error
    }
  }

  async safeJson(resp) {
    try { 
      return await resp.json() 
    } catch { 
      return null 
    }
  }

  // Getters for reactive state
  get user() {
    return currentUser.value
  }

  get token() {
    return authToken.value
  }

  get authenticated() {
    return isAuthenticated.value
  }

  get loading() {
    return isLoading.value
  }
}

// Export singleton instance
const authService = new AuthService()
export default authService

// Export reactive refs for use in components
export { currentUser, authToken, isAuthenticated, isLoading }


