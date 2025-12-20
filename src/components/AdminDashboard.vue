<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Admin Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <Shield class="w-8 h-8 text-primary-600" />
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
              <p class="text-sm text-gray-600">System Management & Analytics</p>
            </div>
          </div>
          <button 
            @click="$emit('exit-admin')"
            class="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <LogOut class="w-4 h-4" />
            <span>Exit Admin</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav class="flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'flex items-center space-x-2 py-4 px-2 border-b-2 font-medium text-sm transition-colors',
              activeTab === tab.id
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            <span>{{ tab.label }}</span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'" class="space-y-6">
        <AdminOverview />
      </div>

      <!-- Users Tab -->
      <div v-if="activeTab === 'users'" class="space-y-6">
        <AdminUsers />
      </div>

      <!-- Topics Tab -->
      <div v-if="activeTab === 'topics'" class="space-y-6">
        <AdminTopics />
      </div>

      <!-- AI Settings Tab -->
      <div v-if="activeTab === 'ai'" class="space-y-6">
        <AdminAISettings />
      </div>

      <!-- Analytics Tab -->
      <div v-if="activeTab === 'analytics'" class="space-y-6">
        <AdminAnalytics />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Shield, LogOut, LayoutDashboard, Users, BookOpen, Settings, BarChart3 } from 'lucide-vue-next'
import AdminOverview from './admin/AdminOverview.vue'
import AdminUsers from './admin/AdminUsers.vue'
import AdminTopics from './admin/AdminTopics.vue'
import AdminAISettings from './admin/AdminAISettings.vue'
import AdminAnalytics from './admin/AdminAnalytics.vue'

defineEmits(['exit-admin'])

const activeTab = ref('overview')

const tabs = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'users', label: 'Users', icon: Users },
  { id: 'topics', label: 'Topics', icon: BookOpen },
  { id: 'ai', label: 'AI Settings', icon: Settings },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 }
]
</script>
