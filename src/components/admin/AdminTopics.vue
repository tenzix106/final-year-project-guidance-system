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
    <div v-if="pagination.pages > 1" class="flex items-center justify-between bg-white px-6 py-4 rounded-xl border border-gray-200">
      <div class="text-sm text-gray-700">
        Page {{ pagination.page }} of {{ pagination.pages }}
      </div>
      <div class="flex space-x-2">
        <button
          @click="loadPage(pagination.page - 1)"
          :disabled="!pagination.has_prev"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Previous
        </button>
        <button
          @click="loadPage(pagination.page + 1)"
          :disabled="!pagination.has_next"
          class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Next
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
const pagination = ref({
  page: 1,
  per_page: 20,
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
        per_page: 20,
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

const deleteTopic = async (topic) => {
  if (!confirm(`Are you sure you want to delete "${topic.title}"?`)) {
    return
  }
  
  try {
    const token = localStorage.getItem('auth_token')
    await axios.delete(
      `http://127.0.0.1:5000/api/admin/topics/${topic.id}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    await fetchTopics(pagination.value.page)
  } catch (error) {
    console.error('Error deleting topic:', error)
    alert(error.response?.data?.message || 'Failed to delete topic')
  }
}

watch([searchQuery, sourceFilter], () => {
  fetchTopics(1)
})

onMounted(() => {
  fetchTopics()
})
</script>
