import { ref } from 'vue'
import authService from './authService.js'

class WorkspaceService {
  constructor() {
    this.baseUrl = 'http://localhost:5000'
    this.workspaces = ref([])
    this.currentWorkspace = ref(null)
    this.isLoading = ref(false)
  }

  getAuthHeaders() {
    return authService.getAuthHeaders()
  }

  async getWorkspaces() {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Failed to fetch workspaces')
      }

      const data = await response.json()
      this.workspaces.value = data.workspaces
      return this.workspaces.value
    } catch (error) {
      console.error('Error fetching workspaces:', error)
      this.workspaces.value = []
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async getWorkspace(workspaceId) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Failed to fetch workspace')
      }

      const data = await response.json()
      this.currentWorkspace.value = data
      return data
    } catch (error) {
      console.error('Error fetching workspace:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async createWorkspace(workspaceData) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(workspaceData)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to create workspace')
      }

      const data = await response.json()
      
      // Refresh workspaces list
      await this.getWorkspaces()
      
      return data
    } catch (error) {
      console.error('Error creating workspace:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async updateWorkspace(workspaceId, updates) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(updates)
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to update workspace')
      }

      const data = await response.json()
      
      // Update local state
      const index = this.workspaces.value.findIndex(w => w.id === workspaceId)
      if (index !== -1) {
        this.workspaces.value[index] = data
      }
      
      return data
    } catch (error) {
      console.error('Error updating workspace:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async deleteWorkspace(workspaceId) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to delete workspace')
      }

      // Remove from local state
      this.workspaces.value = this.workspaces.value.filter(w => w.id !== workspaceId)
      
      return await response.json()
    } catch (error) {
      console.error('Error deleting workspace:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async inviteMember(workspaceId, email, role = 'member') {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}/invite`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ email, role })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to send invitation')
      }

      return await response.json()
    } catch (error) {
      console.error('Error inviting member:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async acceptInvite(inviteToken) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/invites/${inviteToken}/accept`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to accept invitation')
      }

      const data = await response.json()
      
      // Refresh workspaces list
      await this.getWorkspaces()
      
      return data
    } catch (error) {
      console.error('Error accepting invite:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async removeMember(workspaceId, memberId) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}/members/${memberId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to remove member')
      }

      return await response.json()
    } catch (error) {
      console.error('Error removing member:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async discoverWorkspaces() {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/discover`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Failed to discover workspaces')
      }

      const data = await response.json()
      return data.workspaces
    } catch (error) {
      console.error('Error discovering workspaces:', error)
      return []
    } finally {
      this.isLoading.value = false
    }
  }

  async joinWorkspace(workspaceId) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/workspaces/${workspaceId}/join`, {
        method: 'POST',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to join workspace')
      }

      const data = await response.json()
      
      // Refresh workspaces list
      await this.getWorkspaces()
      
      return data
    } catch (error) {
      console.error('Error joining workspace:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }
}

// Export singleton instance
export default new WorkspaceService()
