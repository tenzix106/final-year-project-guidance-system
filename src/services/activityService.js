const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

class ActivityService {
  getAuthHeaders() {
    const token = localStorage.getItem('auth_token')
    const headers = { 'Content-Type': 'application/json' }
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    return headers
  }

  async getActivities(workspaceId, limit = 50, beforeId = null) {
    let url = `${API_BASE_URL}/api/activity/${workspaceId}/activity?limit=${limit}`
    if (beforeId) {
      url += `&before=${beforeId}`
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to fetch activities')
    }

    const data = await response.json()
    return data
  }

  getActivityIcon(activityType) {
    const iconMap = {
      'workspace_created': 'Plus',
      'member_joined': 'UserPlus',
      'member_left': 'UserMinus',
      'member_removed': 'UserX',
      'file_uploaded': 'Upload',
      'file_deleted': 'Trash2',
      'message_sent': 'MessageCircle'
    }
    return iconMap[activityType] || 'Activity'
  }

  getActivityColor(activityType) {
    const colorMap = {
      'workspace_created': 'text-purple-600',
      'member_joined': 'text-green-600',
      'member_left': 'text-orange-600',
      'member_removed': 'text-red-600',
      'file_uploaded': 'text-blue-600',
      'file_deleted': 'text-red-600',
      'message_sent': 'text-primary-600'
    }
    return colorMap[activityType] || 'text-gray-600'
  }
}

const activityService = new ActivityService()
export default activityService
