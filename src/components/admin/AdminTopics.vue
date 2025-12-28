<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-900">Topic Database</h2>
      <div class="flex items-center space-x-4">
        <select v-model="sourceFilter" class="input-field">
          <option value="">All Sources</option>
          <option value="generated">AI Generated</option>
          <option value="predefined">Predefined</option>
          <option value="template">Template</option>
        </select>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search topics..."
          class="input-field"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
    </div>

    <!-- Topics List -->
    <div v-else class="space-y-4">
      <div
        v-for="topic in topics"
        :key="topic.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ topic.title }}</h3>
            <p class="text-gray-600 text-sm mb-4">{{ topic.description }}</p>
            <div class="flex flex-wrap gap-2">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded">
                {{ topic.difficulty }}
              </span>
              <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
                {{ topic.duration }}
              </span>
              <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded">
                {{ topic.source_type }}
              </span>
              <span v-if="topic.ai_provider" class="px-2 py-1 bg-orange-100 text-orange-800 text-xs font-medium rounded">
                {{ topic.ai_provider }}
              </span>
            </div>
          </div>
          <button
            @click="deleteTopic(topic)"
            class="ml-4 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading" class="flex items-center justify-between bg-white px-6 py-4 rounded-xl border border-gray-200">
      <div class="text-sm text-gray-700">
        Showing {{ topics.length > 0 ? ((pagination.page - 1) * pagination.per_page) + 1 : 0 }} 
        to {{ Math.min(pagination.page * pagination.per_page, pagination.total) }} 
        of {{ pagination.total }} topics
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="loadPage(pagination.page - 1)"
          :disabled="!pagination.has_prev"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Previous
        </button>
        <span class="text-sm text-gray-600">
          Page {{ pagination.page }} of {{ pagination.pages || 1 }}
        </span>
        <button
          @click="loadPage(pagination.page + 1)"
          :disabled="!pagination.has_next"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 p-6">
        <h3 class="text-xl font-bold text-gray-900 mb-2">Delete Topic</h3>
        <p class="text-gray-600 mb-4">
          Are you sure you want to delete <span class="font-semibold">{{ deleteConfirmTitle }}</span>?
        </p>
        <p class="text-sm text-red-600 mb-6">
          ⚠️ This action cannot be undone.
        </p>
        <div class="flex space-x-3">
          <button
            @click="cancelDelete"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium transition-colors"
          >
            Cancel
          </button>
          <button
            @click="confirmDelete"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors"
          >
            Delete Topic
          </button>
        </div>
      </div>
    </div>

    <!-- Error Message Modal -->
    <div v-if="showErrorModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 p-6">
        <h3 class="text-xl font-bold text-red-600 mb-2">Cannot Delete Topic</h3>
        <p class="text-gray-700 mb-2 font-semibold">{{ errorModalTitle }}</p>
        <p class="text-gray-600 mb-6">{{ errorModalMessage }}</p>
        <button
          @click="showErrorModal = false"
          class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors"
        >
          Got it
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Loader2, Trash2 } from 'lucide-vue-next'
import axios from 'axios'

const loading = ref(true)
const topics = ref([])
const searchQuery = ref('')
const sourceFilter = ref('')
const showDeleteConfirm = ref(false)
const showErrorModal = ref(false)
const deleteConfirmTitle = ref('')
const errorModalTitle = ref('')
const errorModalMessage = ref('')
const topicToDelete = ref(null)
const pagination = ref({
  page: 1,
  per_page: 5,
  total: 0,
  pages: 0,
  has_next: false,
  has_prev: false
})

const fetchTopics = async (page = 1) => {
  loading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get('http://127.0.0.1:5000/api/admin/topics', {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        page,
        per_page: 5,
        search: searchQuery.value,
        source_type: sourceFilter.value
      }
    })
    topics.value = response.data.topics
    pagination.value = response.data.pagination
  } catch (error) {
    console.error('Error fetching topics:', error)
  } finally {
    loading.value = false
  }
}

const loadPage = (page) => {
  fetchTopics(page)
}

const deleteTopic = (topic) => {
  topicToDelete.value = topic
  deleteConfirmTitle.value = topic.title
  showDeleteConfirm.value = true
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
  topicToDelete.value = null
  deleteConfirmTitle.value = ''
}

const confirmDelete = async () => {
  const topic = topicToDelete.value
  showDeleteConfirm.value = false
  
  try {
    const token = localStorage.getItem('auth_token')
    await axios.delete(
      `http://127.0.0.1:5000/api/admin/topics/${topic.id}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    await fetchTopics(pagination.value.page)
    topicToDelete.value = null
    deleteConfirmTitle.value = ''
  } catch (error) {
    console.error('Error deleting topic:', error)
    
    // Show detailed error modal for referenced topics
    if (error.response?.status === 400) {
      const message = error.response.data?.message || 'Failed to delete topic'
      errorModalTitle.value = topic.title
      
      // Parse the error message to show user-friendly information
      if (message.includes('referenced by')) {
        const match = message.match(/(\d+) saved projects and (\d+) generated projects/)
        if (match) {
          const savedCount = parseInt(match[1])
          const generatedCount = parseInt(match[2])
          
          if (savedCount > 0) {
            errorModalMessage.value = `This topic is currently saved by ${savedCount} student${savedCount > 1 ? 's' : ''}. It cannot be deleted while students have it in their favourites. Please ask students to remove it from their saved projects first, or archive the topic instead of deleting it.`
          } else {
            errorModalMessage.value = `This topic has been used to generate ${generatedCount} project${generatedCount > 1 ? 's' : ''}. It cannot be deleted to maintain data integrity. Consider archiving it instead.`
          }
        } else {
          errorModalMessage.value = message
        }
      } else {
        errorModalMessage.value = message
      }
      
      showErrorModal.value = true
    } else {
      // Generic error
      errorModalTitle.value = 'Error'
      errorModalMessage.value = error.response?.data?.message || 'Failed to delete topic. Please try again.'
      showErrorModal.value = true
    }
    
    topicToDelete.value = null
    deleteConfirmTitle.value = ''
  }
}

watch([searchQuery, sourceFilter], () => {
  fetchTopics(1)
})

onMounted(() => {
  fetchTopics()
})
</script>
