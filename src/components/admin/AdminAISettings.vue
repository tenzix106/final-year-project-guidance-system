<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900">AI Model Settings</h2>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
    </div>

    <!-- AI Providers Configuration -->
    <div v-else class="space-y-6">
      <!-- Gemini -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Sparkles class="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Google Gemini</h3>
              <p class="text-sm text-gray-600">Primary AI provider for topic generation</p>
            </div>
          </div>
          <div :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            settings.providers.gemini.configured ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            {{ settings.providers.gemini.configured ? 'Configured' : 'Not Configured' }}
          </div>
        </div>
        <div class="text-sm text-gray-600">
          <p>API Key Status: {{ settings.providers.gemini.configured ? `${settings.providers.gemini.key_length} characters` : 'Not set' }}</p>
          <p class="mt-2 text-xs text-gray-500">Configure via environment variable: GEMINI_API_KEY</p>
        </div>
      </div>

      <!-- OpenAI -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Sparkles class="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">OpenAI</h3>
              <p class="text-sm text-gray-600">Alternative AI provider (GPT models)</p>
            </div>
          </div>
          <div :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            settings.providers.openai.configured ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            {{ settings.providers.openai.configured ? 'Configured' : 'Not Configured' }}
          </div>
        </div>
        <div class="text-sm text-gray-600">
          <p>API Key Status: {{ settings.providers.openai.configured ? `${settings.providers.openai.key_length} characters` : 'Not set' }}</p>
          <p class="mt-2 text-xs text-gray-500">Configure via environment variable: OPENAI_API_KEY</p>
        </div>
      </div>

      <!-- HuggingFace -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Sparkles class="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">HuggingFace</h3>
              <p class="text-sm text-gray-600">Free-tier AI provider option</p>
            </div>
          </div>
          <div :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            settings.providers.huggingface.configured ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            {{ settings.providers.huggingface.configured ? 'Configured' : 'Not Configured' }}
          </div>
        </div>
        <div class="text-sm text-gray-600">
          <p>API Key Status: {{ settings.providers.huggingface.configured ? `${settings.providers.huggingface.key_length} characters` : 'Not set' }}</p>
          <p class="mt-2 text-xs text-gray-500">Configure via environment variable: HUGGINGFACE_API_KEY</p>
        </div>
      </div>

      <!-- Default Provider -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Default Provider</h3>
        <div class="flex items-center space-x-3">
          <span class="text-sm text-gray-600">Currently set to:</span>
          <span class="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm font-medium uppercase">
            {{ settings.default_provider }}
          </span>
        </div>
        <p class="mt-3 text-xs text-gray-500">Configure via environment variable: DEFAULT_AI_PROVIDER</p>
      </div>

      <!-- Information Box -->
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div class="flex items-start space-x-3">
          <Info class="w-5 h-5 text-blue-600 mt-0.5" />
          <div class="flex-1">
            <h4 class="text-sm font-semibold text-blue-900 mb-2">Configuration Instructions</h4>
            <ul class="text-sm text-blue-800 space-y-1 list-disc list-inside">
              <li>AI provider settings are configured via environment variables</li>
              <li>Update the <code class="bg-blue-100 px-1 py-0.5 rounded">.env</code> file in the backend_flask directory</li>
              <li>Restart the Flask server after making changes</li>
              <li>At least one provider must be configured for AI topic generation to work</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loader2, Sparkles, Info } from 'lucide-vue-next'
import axios from 'axios'

const loading = ref(true)
const settings = ref({
  providers: {
    gemini: { configured: false, key_length: 0 },
    openai: { configured: false, key_length: 0 },
    huggingface: { configured: false, key_length: 0 }
  },
  default_provider: 'gemini'
})

const fetchSettings = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get(buildApiUrl(API_ENDPOINTS.ADMIN.AI_SETTINGS), {
      headers: { Authorization: `Bearer ${token}` }
    })
    settings.value = response.data
  } catch (error) {
    console.error('Error fetching AI settings:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSettings()
})
</script>
