<template>
  <div class="flex flex-col h-full bg-white rounded-lg border border-gray-200">
    <!-- Activity Header -->
    <div class="px-4 py-3 border-b border-gray-200 bg-gray-50">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center space-x-2">
        <Activity class="w-5 h-5" />
        <span>Recent Activity</span>
      </h3>
    </div>

    <!-- Activity Feed -->
    <div class="flex-1 overflow-y-auto p-4" style="max-height: 400px;">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <Loader2 class="w-6 h-6 animate-spin text-primary-600" />
      </div>

      <!-- Empty State -->
      <div v-else-if="activities.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
        <Activity class="w-12 h-12 mb-2 text-gray-400" />
        <p>No activity yet</p>
      </div>

      <!-- Activity List -->
      <div v-else class="space-y-4">
        <div
          v-for="activity in activities"
          :key="activity.id"
          class="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <!-- Icon -->
          <div :class="['p-2 rounded-full bg-gray-100 flex-shrink-0', getActivityColor(activity.activity_type)]">
            <component
              :is="getActivityIcon(activity.activity_type)"
              class="w-4 h-4"
            />
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-900">{{ activity.description }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ formatTime(activity.created_at) }}</p>
          </div>
        </div>

        <!-- Load More -->
        <div v-if="hasMore" class="text-center pt-2">
          <button
            @click="loadMore"
            :disabled="loadingMore"
            class="text-sm text-primary-600 hover:text-primary-700 font-medium disabled:opacity-50"
          >
            {{ loadingMore ? 'Loading...' : 'Load more' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { 
  Activity, Loader2, Plus, UserPlus, UserMinus, UserX, 
  Upload, Trash2, MessageCircle
} from 'lucide-vue-next'
import activityService from '../services/activityService.js'

const props = defineProps({
  workspaceId: {
    type: Number,
    required: true
  }
})

const activities = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const hasMore = ref(false)

onMounted(async () => {
  await loadActivities()
})

const loadActivities = async () => {
  loading.value = true
  try {
    const data = await activityService.getActivities(props.workspaceId, 20)
    activities.value = data.activities
    hasMore.value = data.has_more
  } catch (error) {
    console.error('Failed to load activities:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  if (!hasMore.value || loadingMore.value) return
  
  loadingMore.value = true
  try {
    const lastId = activities.value[activities.value.length - 1]?.id
    const data = await activityService.getActivities(props.workspaceId, 20, lastId)
    activities.value.push(...data.activities)
    hasMore.value = data.has_more
  } catch (error) {
    console.error('Failed to load more activities:', error)
  } finally {
    loadingMore.value = false
  }
}

const getActivityIcon = (activityType) => {
  const iconMap = {
    'workspace_created': Plus,
    'member_joined': UserPlus,
    'member_left': UserMinus,
    'member_removed': UserX,
    'file_uploaded': Upload,
    'file_deleted': Trash2,
    'message_sent': MessageCircle
  }
  return iconMap[activityType] || Activity
}

const getActivityColor = (activityType) => {
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

const formatTime = (dateString) => {
  const date = new Date(dateString + 'Z')
  const now = new Date()
  const diff = now - date
  
  // Less than 1 minute
  if (diff < 60000) {
    return 'Just now'
  }
  
  // Less than 1 hour
  if (diff < 3600000) {
    const mins = Math.floor(diff / 60000)
    return `${mins}m ago`
  }
  
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}h ago`
  }
  
  // Less than 7 days
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}d ago`
  }
  
  // This year
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString('en-MY', { month: 'short', day: 'numeric' })
  }
  
  // Different year
  return date.toLocaleDateString('en-MY', { year: 'numeric', month: 'short', day: 'numeric' })
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
