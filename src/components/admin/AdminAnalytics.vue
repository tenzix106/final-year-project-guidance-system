<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900">Usage Analytics</h2>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
    </div>

    <!-- Analytics Content -->
    <div v-else class="space-y-6">
      <!-- Daily Generations Chart -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Project Generations (Last 30 Days)</h3>
        <div v-if="usage.daily_generations && usage.daily_generations.length > 0" class="space-y-2">
          <div v-for="day in usage.daily_generations" :key="day.date" class="flex items-center">
            <span class="text-sm text-gray-600 w-32">{{ new Date(day.date).toLocaleDateString() }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-6 relative overflow-hidden">
              <div
                class="bg-primary-500 h-full transition-all duration-500"
                :style="{ width: `${(day.count / maxDailyGenerations) * 100}%` }"
              ></div>
              <span class="absolute inset-0 flex items-center justify-end pr-2 text-xs font-medium text-gray-700">
                {{ day.count }}
              </span>
            </div>
          </div>
        </div>
        <p v-else class="text-sm text-gray-500">No generation data available</p>
      </div>

      <!-- Top Programs -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Top Programs by User Count</h3>
        <div v-if="usage.top_programs && usage.top_programs.length > 0" class="space-y-3">
          <div v-for="(prog, index) in usage.top_programs" :key="prog.program" class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <span class="flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-600 font-semibold text-sm">
                {{ index + 1 }}
              </span>
              <span class="text-sm font-medium text-gray-900">{{ prog.program }}</span>
            </div>
            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
              {{ prog.count }} users
            </span>
          </div>
        </div>
        <p v-else class="text-sm text-gray-500">No program data available</p>
      </div>

      <!-- AI Provider Usage -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">AI Provider Usage</h3>
        <div v-if="usage.ai_provider_usage && usage.ai_provider_usage.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            v-for="provider in usage.ai_provider_usage"
            :key="provider.provider"
            class="bg-gray-50 rounded-lg p-4 text-center"
          >
            <p class="text-2xl font-bold text-gray-900">{{ provider.count }}</p>
            <p class="text-sm text-gray-600 uppercase mt-1">{{ provider.provider }}</p>
          </div>
        </div>
        <p v-else class="text-sm text-gray-500">No AI provider usage data available</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import axios from 'axios'

const loading = ref(true)
const usage = ref({
  daily_generations: [],
  top_programs: [],
  ai_provider_usage: []
})

const maxDailyGenerations = computed(() => {
  if (!usage.value.daily_generations || usage.value.daily_generations.length === 0) return 1
  return Math.max(...usage.value.daily_generations.map(d => d.count))
})

const fetchUsageStats = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get(buildApiUrl(API_ENDPOINTS.ADMIN.STATS_USAGE), {
      headers: { Authorization: `Bearer ${token}` }
    })
    usage.value = response.data
  } catch (error) {
    console.error('Error fetching usage stats:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsageStats()
})
</script>
