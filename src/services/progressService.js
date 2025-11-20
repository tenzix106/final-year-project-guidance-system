import { ref } from 'vue'
import authService from './authService'

class ProgressService {
  constructor() {
    this.baseURL = 'http://localhost:5000'
    this.currentProgress = ref(null)
    this.isLoading = ref(false)
  }

  async initializeProgress(savedProjectId, startDate = null) {
    return this.initializeTracking(savedProjectId, startDate)
  }

  async initializeTracking(savedProjectId, startDate = null) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/initialize/${savedProjectId}`,
        {
          method: 'POST',
          headers: authService.getAuthHeaders(),
          body: JSON.stringify({
            start_date: startDate || new Date().toISOString()
          })
        }
      )

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'Failed to initialize progress tracking')
      }

      const data = await response.json()
      this.currentProgress.value = data
      return data

    } catch (error) {
      console.error('Initialize tracking error:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async getProgress(savedProjectId) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/${savedProjectId}`,
        {
          headers: authService.getAuthHeaders()
        }
      )

      if (!response.ok) throw new Error('Failed to fetch progress')

      const data = await response.json()
      this.currentProgress.value = data
      return data

    } catch (error) {
      console.error('Get progress error:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async updatePhaseStatus(savedProjectId, phaseId, newStatus) {
    return this.updatePhase(phaseId, { status: newStatus })
  }

  async updatePhase(phaseId, updates) {
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/phase/${phaseId}`,
        {
          method: 'PUT',
          headers: authService.getAuthHeaders(),
          body: JSON.stringify(updates)
        }
      )

      if (!response.ok) throw new Error('Failed to update phase')

      const data = await response.json()
      
      // Refresh current progress
      if (this.currentProgress.value && this.currentProgress.value.phases) {
        const phaseIndex = this.currentProgress.value.phases.findIndex(p => p.id === phaseId)
        if (phaseIndex !== -1) {
          this.currentProgress.value.phases[phaseIndex] = data.phase
        }
      }
      
      return data

    } catch (error) {
      console.error('Update phase error:', error)
      throw error
    }
  }

  async toggleTask(savedProjectId, phaseId, taskId) {
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/task/${taskId}/toggle`,
        {
          method: 'PUT',
          headers: authService.getAuthHeaders()
        }
      )

      if (!response.ok) throw new Error('Failed to toggle task')

      return await response.json()

    } catch (error) {
      console.error('Toggle task error:', error)
      throw error
    }
  }

  async addTask(savedProjectId, phaseId, taskTitle) {
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/task`,
        {
          method: 'POST',
          headers: authService.getAuthHeaders(),
          body: JSON.stringify({ 
            phase_id: phaseId, 
            task_title: taskTitle 
          })
        }
      )

      if (!response.ok) throw new Error('Failed to add task')

      return await response.json()

    } catch (error) {
      console.error('Add task error:', error)
      throw error
    }
  }

  async deleteTask(savedProjectId, phaseId, taskId) {
    try {
      if (!authService.authenticated) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${this.baseURL}/api/progress/task/${taskId}`,
        {
          method: 'DELETE',
          headers: authService.getAuthHeaders()
        }
      )

      if (!response.ok) throw new Error('Failed to delete task')

      return await response.json()

    } catch (error) {
      console.error('Delete task error:', error)
      throw error
    }
  }

  getPhaseStatusColor(status) {
    const colors = {
      'not_started': 'gray',
      'in_progress': 'blue',
      'completed': 'green',
      'blocked': 'red'
    }
    return colors[status] || 'gray'
  }

  getProjectStatusColor(status) {
    const colors = {
      'saved': 'gray',
      'not_started': 'gray',
      'in_progress': 'blue',
      'completed': 'green',
      'abandoned': 'red'
    }
    return colors[status] || 'gray'
  }

  formatDate(dateString) {
    if (!dateString) return 'Not set'
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  calculateTimeRemaining(endDate) {
    if (!endDate) return null
    
    const end = new Date(endDate)
    const now = new Date()
    const diffTime = end - now
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays < 0) return `${Math.abs(diffDays)} days overdue`
    if (diffDays === 0) return 'Due today'
    if (diffDays === 1) return '1 day remaining'
    if (diffDays < 7) return `${diffDays} days remaining`
    
    const weeks = Math.floor(diffDays / 7)
    return `${weeks} week${weeks > 1 ? 's' : ''} remaining`
  }
}

export default new ProgressService()
