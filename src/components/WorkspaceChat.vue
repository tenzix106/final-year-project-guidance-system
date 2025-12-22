<template>
  <div class="flex flex-col h-full bg-white rounded-lg border border-gray-200">
    <!-- Chat Header -->
    <div class="px-4 py-3 border-b border-gray-200 bg-gray-50">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center space-x-2">
        <MessageCircle class="w-5 h-5" />
        <span>Workspace Chat</span>
      </h3>
    </div>

    <!-- Messages Area -->
    <div 
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-4"
      style="max-height: 400px;"
    >
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <Loader2 class="w-6 h-6 animate-spin text-primary-600" />
      </div>

      <!-- Empty State -->
      <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
        <MessageCircle class="w-12 h-12 mb-2 text-gray-400" />
        <p>No messages yet. Start the conversation!</p>
      </div>

      <!-- Messages -->
      <div v-else class="space-y-4">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="[
            'flex',
            message.user_id === currentUserId ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            :class="[
              'max-w-[70%] rounded-lg px-4 py-2',
              message.user_id === currentUserId
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-gray-900'
            ]"
          >
            <!-- Sender name for others' messages -->
            <div
              v-if="message.user_id !== currentUserId"
              class="text-xs font-medium text-gray-600 mb-1"
            >
              {{ message.user_name || message.user_email }}
            </div>
            
            <!-- Message text -->
            <p class="text-sm whitespace-pre-wrap break-words">{{ message.message }}</p>
            
            <!-- Timestamp -->
            <div
              :class="[
                'text-xs mt-1 flex items-center justify-between space-x-2',
                message.user_id === currentUserId ? 'text-primary-100' : 'text-gray-500'
              ]"
            >
              <span>{{ formatTime(message.created_at) }}</span>
              
              <!-- Delete button for own messages -->
              <button
                v-if="message.user_id === currentUserId || isOwner"
                @click="handleDeleteMessage(message.id)"
                :class="[
                  'hover:opacity-70 transition-opacity',
                  message.user_id === currentUserId ? 'text-primary-100' : 'text-gray-500'
                ]"
              >
                <Trash2 class="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="px-4 py-3 border-t border-gray-200">
      <form @submit.prevent="handleSendMessage" class="flex space-x-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type a message..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          :disabled="sending"
        />
        <button
          type="submit"
          :disabled="!newMessage.trim() || sending"
          class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <Send class="w-4 h-4" />
          <span v-if="sending">Sending...</span>
          <span v-else>Send</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { MessageCircle, Send, Trash2, Loader2 } from 'lucide-vue-next'
import chatService from '../services/chatService.js'
import { currentUser } from '../services/authService.js'

const props = defineProps({
  workspaceId: {
    type: Number,
    required: true
  },
  isOwner: {
    type: Boolean,
    default: false
  }
})

const messages = ref([])
const newMessage = ref('')
const loading = ref(false)
const sending = ref(false)
const messagesContainer = ref(null)

const currentUserId = computed(() => currentUser.value?.id)

onMounted(async () => {
  await loadMessages()
  // Start polling for new messages every 3 seconds
  chatService.startPolling(props.workspaceId, 3000)
  
  // Watch for new messages from the service
  watch(() => chatService.messages.value, (newMessages) => {
    messages.value = newMessages
    scrollToBottom()
  }, { deep: true })
})

onUnmounted(() => {
  chatService.stopPolling()
  chatService.clearMessages()
})

const loadMessages = async () => {
  loading.value = true
  try {
    const data = await chatService.getMessages(props.workspaceId)
    messages.value = data.messages
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to load messages:', error)
  } finally {
    loading.value = false
  }
}

const handleSendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  const messageText = newMessage.value
  newMessage.value = '' // Clear input immediately
  sending.value = true
  
  try {
    await chatService.sendMessage(props.workspaceId, messageText)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
    newMessage.value = messageText // Restore message on error
    alert('Failed to send message. Please try again.')
  } finally {
    sending.value = false
  }
}

const handleDeleteMessage = async (messageId) => {
  if (!confirm('Delete this message?')) return
  
  try {
    await chatService.deleteMessage(messageId)
  } catch (error) {
    console.error('Failed to delete message:', error)
    alert('Failed to delete message.')
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (dateString) => {
  // Parse as UTC and convert to local time
  const date = new Date(dateString + 'Z') // Add 'Z' to indicate UTC if not present
  const now = new Date()
  const diff = now - date
  
  // Check if message is from today first
  const isToday = date.toDateString() === now.toDateString()
  
  if (isToday) {
    // Less than 1 minute
    if (diff < 60000) {
      return 'Just now'
    }
    
    // Less than 1 hour
    if (diff < 3600000) {
      const mins = Math.floor(diff / 60000)
      return `${mins}m ago`
    }
    
    // Show actual time for messages sent today in 12-hour format
    return date.toLocaleTimeString('en-MY', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true
    })
  }
  
  // Yesterday
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday at ' + date.toLocaleTimeString('en-MY', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true
    })
  }
  
  // Same year
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString('en-MY', { 
      month: 'short', 
      day: 'numeric'
    }) + ' at ' + 
    date.toLocaleTimeString('en-MY', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true
    })
  }
  
  // Different year
  return date.toLocaleDateString('en-MY', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric'
  })
}
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
