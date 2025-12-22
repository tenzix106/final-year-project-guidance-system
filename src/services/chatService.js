import { ref } from 'vue'
import authService from './authService.js'

class ChatService {
  constructor() {
    this.baseUrl = 'http://localhost:5000'
    this.messages = ref([])
    this.isLoading = ref(false)
    this.pollingInterval = null
  }

  getAuthHeaders() {
    return authService.getAuthHeaders()
  }

  async getMessages(workspaceId, beforeId = null, limit = 50) {
    this.isLoading.value = true
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const params = new URLSearchParams({ limit: limit.toString() })
      if (beforeId) {
        params.append('before', beforeId.toString())
      }

      const response = await fetch(`${this.baseUrl}/api/chat/${workspaceId}/messages?${params}`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Failed to fetch messages')
      }

      const data = await response.json()
      this.messages.value = data.messages
      return data
    } catch (error) {
      console.error('Error fetching messages:', error)
      throw error
    } finally {
      this.isLoading.value = false
    }
  }

  async sendMessage(workspaceId, message, messageType = 'text') {
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/chat/${workspaceId}/messages`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ message, message_type: messageType })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to send message')
      }

      const data = await response.json()
      
      // Add message to local state
      this.messages.value.push(data)
      
      return data
    } catch (error) {
      console.error('Error sending message:', error)
      throw error
    }
  }

  async deleteMessage(messageId) {
    try {
      if (!authService.authenticated) {
        throw new Error('No auth token found')
      }

      const response = await fetch(`${this.baseUrl}/api/chat/messages/${messageId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to delete message')
      }

      // Remove message from local state
      this.messages.value = this.messages.value.filter(msg => msg.id !== messageId)
      
      return await response.json()
    } catch (error) {
      console.error('Error deleting message:', error)
      throw error
    }
  }

  // Start polling for new messages
  startPolling(workspaceId, intervalMs = 3000) {
    this.stopPolling() // Clear any existing interval
    
    this.pollingInterval = setInterval(async () => {
      try {
        const lastMessageId = this.messages.value.length > 0 
          ? this.messages.value[this.messages.value.length - 1].id 
          : null
        
        // Fetch messages after the last one we have
        const response = await fetch(
          `${this.baseUrl}/api/chat/${workspaceId}/messages?limit=20`,
          { headers: this.getAuthHeaders() }
        )
        
        if (response.ok) {
          const data = await response.json()
          
          // Only add new messages
          if (data.messages.length > 0) {
            const newMessages = lastMessageId 
              ? data.messages.filter(msg => msg.id > lastMessageId)
              : data.messages
            
            if (newMessages.length > 0) {
              this.messages.value.push(...newMessages)
            }
          }
        }
      } catch (error) {
        console.error('Polling error:', error)
      }
    }, intervalMs)
  }

  stopPolling() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval)
      this.pollingInterval = null
    }
  }

  clearMessages() {
    this.messages.value = []
  }
}

// Export singleton instance
export default new ChatService()
