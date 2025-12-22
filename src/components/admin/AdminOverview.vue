<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900">System Overview</h2>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
      <p class="text-red-800 font-medium">{{ error }}</p>
      <button @click="fetchStats()" class="mt-4 btn-primary">
        Retry
      </button>
    </div>

    <!-- Stats Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Users -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Total Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_users }}</p>
            <p class="text-sm text-gray-500 mt-1">
              {{ stats.total_students }} students, {{ stats.total_admins }} admins
            </p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Users class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>

      <!-- Total Topics -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Project Topics</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_topics }}</p>
            <p class="text-sm text-gray-500 mt-1">In database</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <BookOpen class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>

      <!-- Generated Projects -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Generated Projects</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_generated_projects }}</p>
            <p class="text-sm text-gray-500 mt-1">AI generations</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <Sparkles class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>

      <!-- Saved Projects -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Saved Projects</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.total_saved_projects }}</p>
            <p class="text-sm text-gray-500 mt-1">User favourites</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <Heart class="w-6 h-6 text-orange-600" />
          </div>
        </div>
      </div>

      <!-- New Users (30 days) -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">New Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.new_users_30d }}</p>
            <p class="text-sm text-gray-500 mt-1">Last 30 days</p>
          </div>
          <div class="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
            <UserPlus class="w-6 h-6 text-teal-600" />
          </div>
        </div>
      </div>

      <!-- Active Users (30 days) -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Active Users</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.active_users_30d }}</p>
            <p class="text-sm text-gray-500 mt-1">Last 30 days</p>
          </div>
          <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
            <Activity class="w-6 h-6 text-indigo-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button class="flex items-center space-x-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all">
          <Users class="w-5 h-5 text-gray-600" />
          <div class="text-left">
            <p class="font-medium text-gray-900">Manage Users</p>
            <p class="text-sm text-gray-500">View and edit user accounts</p>
          </div>
        </button>
        <button class="flex items-center space-x-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all">
          <BookOpen class="w-5 h-5 text-gray-600" />
          <div class="text-left">
            <p class="font-medium text-gray-900">Topic Database</p>
            <p class="text-sm text-gray-500">Manage project topics</p>
          </div>
        </button>
        <button class="flex items-center space-x-3 p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all">
          <Settings class="w-5 h-5 text-gray-600" />
          <div class="text-left">
            <p class="font-medium text-gray-900">AI Settings</p>
            <p class="text-sm text-gray-500">Configure AI providers</p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Users, BookOpen, Sparkles, Heart, TrendingUp, Loader2 } from 'lucide-vue-next'
import axios from 'axios'

const loading = ref(true)
const error = ref(null)
const stats = ref({
  total_users: 0,
  total_students: 0,
  total_admins: 0,
  total_topics: 0,
  total_generated_projects: 0,
  total_saved_projects: 0,
  new_users_30d: 0,
  active_users_30d: 0
})

const fetchStats = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      error.value = 'No authentication token found. Please log in again.'
      setTimeout(() => {
        window.location.href = '/'
      }, 2000)
      return
    }
    
    const response = await axios.get('http://127.0.0.1:5000/api/admin/stats/overview', {
      headers: { Authorization: `Bearer ${token}` }
    })
    stats.value = response.data
  } catch (err) {
    console.error('Error fetching stats:', err)
    if (err.response) {
      console.error('Response data:', err.response.data)
      console.error('Response status:', err.response.status)
      
      // Redirect to home on authentication/authorization errors
      if (err.response.status === 401 || err.response.status === 403 || err.response.status === 422) {
        error.value = err.response.data?.message || 'Session expired. Redirecting to home page...'
        setTimeout(() => {
          window.location.href = '/'
        }, 2000)
        return
      }
      
      error.value = err.response.data?.message || `Error: ${err.response.status} - Failed to load statistics`
    } else {
      error.value = 'Network error. Please check if the backend server is running.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
