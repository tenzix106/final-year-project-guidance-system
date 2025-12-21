<template>
  <div class="min-h-screen bg-accent-50">
    <!-- Student/Guest Header -->
    <header v-if="!isAuthenticated || currentUser?.role === 'student'" class="bg-white backdrop-blur-md border-b border-secondary-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center shadow-md">
              <GraduationCap class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-primary-600">fip.</h1>
            </div>
          </div>
          
          <div class="flex items-center space-x-6">
            <!-- Navigation -->
            <nav class="hidden md:flex space-x-8">
              <button @click="setActiveView('home')" :class="activeView === 'home' ? 'text-primary-600 font-semibold' : 'text-gray-600 hover:text-primary-600 transition-colors'">
                Home
              </button>
              <button v-if="isAuthenticated" @click="setActiveView('favourites')" :class="activeView === 'favourites' ? 'text-primary-600 font-semibold' : 'text-gray-600 hover:text-primary-600 transition-colors'" class="flex items-center space-x-1">
                <Heart class="w-4 h-4" />
                <span>My Favourites</span>
              </button>
              <a v-if="activeView === 'home'" href="#resources" class="text-gray-600 hover:text-primary-600 transition-colors">Resources</a>
              <a v-if="activeView === 'home'" href="#setup" class="text-gray-600 hover:text-primary-600 transition-colors">AI Setup</a>
            </nav>

            <!-- Auth Section -->
            <div class="flex items-center space-x-3">
              <!-- Authenticated User -->
              <div v-if="isAuthenticated" class="relative">
                <button 
                  @click="toggleUserDropdown"
                  class="flex items-center space-x-2 text-sm hover:bg-gray-50 px-3 py-2 rounded-lg transition-colors"
                >
                  <div class="w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center">
                    <User class="w-4 h-4" />
                  </div>
                  <span class="text-gray-700 font-medium">{{ currentUser?.email }}</span>
                  <ChevronDown class="w-4 h-4 text-gray-400" :class="{ 'rotate-180': userDropdownOpen }" />
                </button>

                <!-- Dropdown Menu -->
                <transition name="dropdown">
                  <div v-if="userDropdownOpen" class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50">
                    <div class="px-4 py-3 border-b border-gray-100">
                      <p class="text-xs text-gray-500">Signed in as</p>
                      <p class="text-sm font-medium text-gray-900 truncate">{{ currentUser?.email }}</p>
                      <p class="text-xs text-gray-500 mt-1">
                        {{ currentUser?.auth_provider === 'google' ? 'Google Account' : 'Email Account' }}
                      </p>
                    </div>
                    
                    <button 
                      @click="openProfileModalFromDropdown"
                      class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2 transition-colors"
                    >
                      <Settings class="w-4 h-4" />
                      <span>Edit Profile</span>
                    </button>
                    
                    <button 
                      @click="handleLogoutFromDropdown"
                      class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2 transition-colors"
                    >
                      <LogOut class="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </transition>
              </div>

              <!-- Not Authenticated -->
              <div v-else class="flex items-center space-x-3">
                <button 
                  @click="openAuthModal('login')"
                  class="text-gray-600 hover:text-primary-600 transition-colors font-medium"
                >
                  Sign In
                </button>
                <button 
                  @click="openAuthModal('register')"
                  class="bg-primary-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-600 transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  Sign Up
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Admin Header -->
    <header v-if="isAuthenticated && currentUser?.role === 'admin'" class="bg-white backdrop-blur-md border-b border-secondary-200 sticky top-0 z-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center shadow-md">
              <GraduationCap class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-primary-600">fip.</h1>
            </div>
          </div>
          
          <div class="flex items-center space-x-6">
            <!-- Admin Navigation -->
            <nav class="hidden md:flex space-x-8">
              <button @click="setActiveView('home')" :class="activeView === 'home' ? 'text-primary-600 font-semibold' : 'text-gray-600 hover:text-primary-600 transition-colors'">
                Dashboard
              </button>
              <button @click="setActiveView('admin')" :class="activeView === 'admin' ? 'text-primary-600 font-semibold' : 'text-gray-600 hover:text-primary-600 transition-colors'" class="flex items-center space-x-1">
                <Shield class="w-4 h-4" />
                <span>Admin Panel</span>
              </button>
            </nav>

            <!-- Admin User Section -->
            <div class="flex items-center space-x-3">
              <div class="relative">
                <button 
                  @click="toggleUserDropdown"
                  class="flex items-center space-x-2 text-sm hover:bg-gray-50 px-3 py-2 rounded-lg transition-colors"
                >
                  <div class="w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center">
                    <User class="w-4 h-4" />
                  </div>
                  <span class="text-gray-700 font-medium">{{ currentUser?.email }}</span>
                  <ChevronDown class="w-4 h-4 text-gray-400" :class="{ 'rotate-180': userDropdownOpen }" />
                </button>

                <!-- Admin Dropdown Menu -->
                <transition name="dropdown">
                  <div v-if="userDropdownOpen" class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50">
                    <div class="px-4 py-3 border-b border-gray-100">
                      <p class="text-xs text-gray-500">Signed in as</p>
                      <p class="text-sm font-medium text-gray-900 truncate">{{ currentUser?.email }}</p>
                      <p class="text-xs text-purple-600 mt-1 flex items-center">
                        <Shield class="w-3 h-3 mr-1" />
                        Administrator
                      </p>
                    </div>
                    
                    <button 
                      @click="openProfileModalFromDropdown"
                      class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2 transition-colors"
                    >
                      <Settings class="w-4 h-4" />
                      <span>Edit Profile</span>
                    </button>
                    
                    <button 
                      @click="handleLogoutFromDropdown"
                      class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2 transition-colors"
                    >
                      <LogOut class="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section v-if="!isAuthenticated || currentUser?.role === 'student'" class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-5xl font-bold text-gray-900 mb-6 animate-fade-in">
          Find Your Perfect
          <span class="text-primary-600">Final Year Project</span>
        </h2>
        <p class="text-xl text-gray-600 mb-8 animate-slide-up">
          Get AI-powered project suggestions tailored to your interests, skills, and academic requirements.
          Discover relevant resources and guidance for your research journey.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up">
          <button @click="scrollToForm" class="btn-primary">
            <Sparkles class="w-5 h-5 inline mr-2" />
            Generate Topics
          </button>
          <button @click="scrollToResults" class="btn-secondary">
            <BookOpen class="w-5 h-5 inline mr-2" />
            View Examples
          </button>
        </div>
      </div>
    </section>

    <!-- Admin Hero Section -->
    <section v-if="isAuthenticated && currentUser?.role === 'admin' && activeView === 'home'" class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-purple-50 to-blue-50">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <div class="flex items-center justify-center space-x-3 mb-4">
            <Shield class="w-16 h-16 text-purple-600" />
          </div>
          <h2 class="text-5xl font-bold text-gray-900 mb-4 animate-fade-in">
            Admin Dashboard
          </h2>
          <p class="text-xl text-gray-600 animate-slide-up">
            Manage the FYP Guidance System - Monitor users, topics, AI settings, and system analytics
          </p>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 font-medium">Total Users</p>
                <p class="text-3xl font-bold text-gray-900 mt-1">{{ adminQuickStats.users }}</p>
              </div>
              <Users class="w-10 h-10 text-blue-500 opacity-80" />
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 font-medium">Project Topics</p>
                <p class="text-3xl font-bold text-gray-900 mt-1">{{ adminQuickStats.topics }}</p>
              </div>
              <BookOpen class="w-10 h-10 text-green-500 opacity-80" />
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 font-medium">AI Generated</p>
                <p class="text-3xl font-bold text-gray-900 mt-1">{{ adminQuickStats.generated }}</p>
              </div>
              <Sparkles class="w-10 h-10 text-purple-500 opacity-80" />
            </div>
          </div>
          <div class="bg-white rounded-xl shadow-md p-6 border-l-4 border-orange-500">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 font-medium">Active (30d)</p>
                <p class="text-3xl font-bold text-gray-900 mt-1">{{ adminQuickStats.active }}</p>
              </div>
              <Activity class="w-10 h-10 text-orange-500 opacity-80" />
            </div>
          </div>
        </div>

        <!-- Admin Features Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-purple-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <LayoutDashboard class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">System Overview</h3>
            </div>
            <p class="text-gray-600 text-sm">View comprehensive system statistics, user metrics, and activity trends at a glance</p>
          </button>

          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-blue-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <Users class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">User Management</h3>
            </div>
            <p class="text-gray-600 text-sm">Manage user accounts, assign roles, view user details, and monitor registrations</p>
          </button>

          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-green-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <BookOpen class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">Topic Database</h3>
            </div>
            <p class="text-gray-600 text-sm">Browse, search, filter and manage all project topics in the database</p>
          </button>

          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-indigo-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <Settings class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">AI Settings</h3>
            </div>
            <p class="text-gray-600 text-sm">Configure AI providers, manage API keys, and set default models for topic generation</p>
          </button>

          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-orange-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <BarChart3 class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">Analytics & Reports</h3>
            </div>
            <p class="text-gray-600 text-sm">View usage statistics, generation trends, and detailed analytics reports</p>
          </button>

          <button
            @click="setActiveView('admin')"
            class="bg-white rounded-xl shadow-md p-8 text-left hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-2 border-transparent hover:border-red-500 group"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-red-500 to-red-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <Database class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-xl font-bold text-gray-900">System Health</h3>
            </div>
            <p class="text-gray-600 text-sm">Monitor system performance, database status, and API health metrics</p>
          </button>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main v-if="activeView === 'home' && (!isAuthenticated || currentUser?.role === 'student')" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <!-- AI Status Banner -->
      <!-- <div v-if="aiStatus.provider" class="mb-8">
        <div class="card max-w-4xl mx-auto">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center"
                   :class="useAI ? 'bg-green-100' : 'bg-yellow-100'">
                <Sparkles class="w-4 h-4" :class="useAI ? 'text-green-600' : 'text-yellow-600'" />
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">
                  {{ useAI ? 'AI-Powered Topic Generation' : 'Mock Data Mode' }}
                </h4>
                <p class="text-sm text-gray-600">
                  {{ useAI ? `Using ${aiStatus.provider.toUpperCase()} AI for personalized topic generation` : 'AI not configured - using sample topics' }}
                </p>
              </div>
            </div>
            <div v-if="!useAI" class="text-right">
              <p class="text-xs text-gray-500 mb-1">To enable AI features:</p>
              <a href="#setup" class="text-sm text-primary-600 hover:text-primary-700 underline">
                Setup Guide
              </a>
            </div>
          </div>
        </div>
      </div> -->

      <!-- Form Section -->
      <section id="form" class="mb-20">
        <FYPForm @generate-topics="handleGenerateTopics" />
      </section>

      <!-- Results Section -->
      <section id="results" class="mb-20">
        <!-- AI Error Display -->
        <div v-if="aiError" class="mb-6">
          <div class="card max-w-4xl mx-auto bg-red-50 border-red-200">
            <div class="flex items-center space-x-3">
              <AlertCircle class="w-5 h-5 text-red-600" />
              <div>
                <h4 class="font-semibold text-red-800">AI Generation Error</h4>
                <p class="text-sm text-red-700">{{ aiError }}</p>
                <p class="text-xs text-red-600 mt-1">Showing sample topics instead.</p>
              </div>
            </div>
          </div>
        </div>
        
        <FYPResults :topics="generatedTopics" :loading="isLoading" />
      </section>

      <!-- Resources Section -->
      <section id="resources" class="mb-20">
        <FYPResources />
      </section>

      <!-- AI Setup Section -->
      <!-- <section id="setup" class="mb-20">
        <AISetupGuide />
      </section> -->
    </main>

    <!-- Favourites Page View -->
    <main v-if="activeView === 'favourites'" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <FavouritesPage @navigate-home="setActiveView('home')" />
    </main>

    <!-- Admin Dashboard View -->
    <AdminDashboard v-if="activeView === 'admin'" @exit-admin="setActiveView('home')" />

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center shadow-md">
                <GraduationCap class="w-5 h-5 text-white" />
              </div>
              <span class="text-xl font-bold text-primary-600">FYP Guidance</span>
            </div>
            <p class="text-secondary-600">
              Empowering students with AI-driven project suggestions and comprehensive research guidance.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Links</h3>
            <ul class="space-y-2">
              <li><a href="#form" class="text-gray-600 hover:text-primary-600 transition-colors">Generate Topics</a></li>
              <li><a href="#results" class="text-gray-600 hover:text-primary-600 transition-colors">View Results</a></li>
              <li><a href="#resources" class="text-gray-600 hover:text-primary-600 transition-colors">Resources</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Support</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Help Center</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Contact Us</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Documentation</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-200 mt-8 pt-8 text-center">
          <p class="text-gray-600">&copy; 2024 FYP Guidance System. All rights reserved.</p>
        </div>
      </div>
    </footer>

    <!-- Auth Modal -->
    <AuthModal 
      :is-open="authModalOpen"
      :initial-mode="authModalMode"
      @close="closeAuthModal"
      @success="handleAuthSuccess"
    />

    <!-- Profile Completion Modal -->
    <ProfileCompletionModal
      :is-open="profileCompletionModalOpen"
      @completed="handleProfileCompletion"
    />

    <!-- Profile Modal -->
    <ProfileModal
      :is-open="profileModalOpen"
      @close="closeProfileModal"
      @updated="handleProfileUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { GraduationCap, Sparkles, BookOpen, AlertCircle, User, LogOut, Heart, Settings, ChevronDown, Shield, LayoutDashboard, BarChart3, Database, Activity, Users } from 'lucide-vue-next'
import FYPForm from './components/FYPForm.vue'
import FYPResults from './components/FYPResults.vue'
import FYPResources from './components/FYPResources.vue'
import AISetupGuide from './components/AISetupGuide.vue'
import AuthModal from './components/AuthModal.vue'
import ProfileCompletionModal from './components/ProfileCompletionModal.vue'
import ProfileModal from './components/ProfileModal.vue'
import FavouritesPage from './components/FavouritesPage.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import aiService from './services/aiService.js'
import authService, { isAuthenticated, currentUser } from './services/authService.js'
import axios from 'axios'

const generatedTopics = ref([])
const isLoading = ref(false)
const aiError = ref('')
const aiStatus = ref({})
const useAI = ref(false)

// Auth state
const authModalOpen = ref(false)
const authModalMode = ref('login')

// Profile completion state
const profileCompletionModalOpen = ref(false)

// Profile state
const profileModalOpen = ref(false)

// User dropdown state
const userDropdownOpen = ref(false)

// View state
const activeView = ref('home')

// Admin stats
const adminQuickStats = ref({
  users: 0,
  topics: 0,
  generated: 0,
  active: 0
})

const setActiveView = (view) => {
  activeView.value = view
  if (view === 'home') {
    // Optionally scroll to top when going home
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Fetch admin stats when user is admin
const fetchAdminStats = async () => {
  if (!isAuthenticated.value || currentUser.value?.role !== 'admin') return
  
  try {
    const token = localStorage.getItem('auth_token')
    const response = await axios.get('http://localhost:5000/api/admin/stats/overview', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    adminQuickStats.value = {
      users: response.data.total_users || 0,
      topics: response.data.total_topics || 0,
      generated: response.data.total_generated_projects || 0,
      active: response.data.active_users_30d || 0
    }
  } catch (error) {
    console.error('Error fetching admin stats:', error)
  }
}

const scrollToForm = () => {
  document.getElementById('form')?.scrollIntoView({ behavior: 'smooth' })
}

const scrollToResults = () => {
  document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
}

const handleGenerateTopics = async (formData) => {
  isLoading.value = true
  aiError.value = ''
  
  try {
    if (useAI.value && aiService.isConfigured()) {
      // Use AI service for topic generation
      generatedTopics.value = await aiService.generateTopics(formData)
    } else {
      // Fallback to mock data
      generatedTopics.value = generateMockTopics(formData)
    }
  } catch (error) {
    console.error('Topic generation error:', error)
    aiError.value = error.message
    // Fallback to mock data on error
    generatedTopics.value = generateMockTopics(formData)
  } finally {
    isLoading.value = false
    scrollToResults()
  }
}

// Check AI service status on component mount
onMounted(() => {
  aiStatus.value = aiService.getStatus()
  useAI.value = aiService.isConfigured()
  
  // Fetch admin stats if user is admin
  if (isAuthenticated.value && currentUser.value?.role === 'admin') {
    fetchAdminStats()
  }
  
  // Check if OAuth user needs to complete profile
  if (isAuthenticated.value && currentUser.value && !currentUser.value.onboarding_completed) {
    // Show profile completion modal for OAuth users who just signed in
    setTimeout(() => {
      profileCompletionModalOpen.value = true
    }, 500)
  }
  
  // Close dropdown when clicking outside
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Watch for authentication changes to fetch admin stats and check onboarding
watch([isAuthenticated, currentUser], ([newAuth, newUser]) => {
  if (newAuth && newUser?.role === 'admin') {
    fetchAdminStats()
  }
  
  // Check if newly authenticated user needs to complete profile
  if (newAuth && newUser && !newUser.onboarding_completed && !profileCompletionModalOpen.value) {
    profileCompletionModalOpen.value = true
  }
}, { deep: true })

const generateMockTopics = (formData) => {
  // Parse skills and interests from text input
  const skills = formData.skillsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
  const interests = formData.interestsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
  
  // Generate topics based on program and interests
  const topics = []
  
  // Technology/Computing topics
  if (formData.program.includes('computer') || formData.program.includes('software') || 
      formData.program.includes('information') || formData.program.includes('data') ||
      formData.program.includes('cybersecurity') || interests.some(i => 
        i.toLowerCase().includes('ai') || i.toLowerCase().includes('machine learning') ||
        i.toLowerCase().includes('software') || i.toLowerCase().includes('programming'))) {
    
    topics.push({
      id: 1,
      title: "AI-Powered Learning Management System",
      description: "Develop an intelligent LMS that adapts to individual learning patterns and provides personalized content recommendations using machine learning algorithms.",
      difficulty: "Advanced",
      duration: "6-8 months",
      skills: ["Machine Learning", "Web Development", "Database Design", "Python"],
      resources: [
        { type: "Paper", title: "Personalized Learning Systems: A Survey", url: "#" },
        { type: "Tutorial", title: "Building ML Models with TensorFlow", url: "#" },
        { type: "Tool", title: "React.js Documentation", url: "#" }
      ],
      tags: ["AI/ML", "Education", "Web Development"],
      objectives: [
        "Design and implement machine learning algorithms for personalized content recommendation",
        "Create an adaptive user interface that responds to individual learning patterns",
        "Develop a comprehensive analytics dashboard for educators and administrators",
        "Implement secure user authentication and data privacy measures"
      ],
      methodology: "This project will follow an agile development methodology, starting with user research and requirements gathering, followed by iterative design and development cycles. The machine learning component will be developed using TensorFlow and scikit-learn, while the web application will be built using React.js and Node.js. User testing will be conducted throughout the development process to ensure the system meets educational needs.",
      expectedOutcomes: "Upon completion, this project will deliver a fully functional AI-powered LMS that can adapt to individual learning styles, improve student engagement, and provide valuable insights to educators. The system will demonstrate measurable improvements in learning outcomes and user satisfaction compared to traditional LMS platforms."
    })
  }
  
  // Business/Marketing topics
  if (formData.program.includes('business') || formData.program.includes('marketing') || 
      formData.program.includes('finance') || formData.program.includes('management') ||
      interests.some(i => i.toLowerCase().includes('business') || i.toLowerCase().includes('marketing') ||
        i.toLowerCase().includes('finance') || i.toLowerCase().includes('e-commerce'))) {
    
    topics.push({
      id: 2,
      title: "Digital Marketing Analytics Dashboard",
      description: "Create a comprehensive analytics platform for tracking and analyzing digital marketing campaigns across multiple channels with real-time insights.",
      difficulty: "Intermediate",
      duration: "4-6 months",
      skills: ["Data Analytics", "Web Development", "Marketing", "Statistics"],
      resources: [
        { type: "Paper", title: "Digital Marketing Analytics: Current Trends", url: "#" },
        { type: "Tutorial", title: "Building Analytics Dashboards", url: "#" },
        { type: "Tool", title: "Google Analytics API Documentation", url: "#" }
      ],
      tags: ["Marketing", "Analytics", "Business Intelligence"],
      objectives: [
        "Develop a unified dashboard integrating multiple marketing channels (social media, email, PPC, SEO)",
        "Implement real-time data visualization and reporting capabilities",
        "Create automated alert systems for campaign performance monitoring",
        "Design user-friendly interfaces for different stakeholder roles"
      ],
      methodology: "The project will utilize a data-driven approach, starting with comprehensive market research and stakeholder interviews. The dashboard will be built using modern web technologies including React.js for the frontend and Node.js for the backend. Data integration will be achieved through APIs from various marketing platforms, with data processing handled by Python scripts and visualization powered by D3.js or Chart.js.",
      expectedOutcomes: "The final product will be a comprehensive analytics dashboard that provides marketers with actionable insights, reduces manual reporting time by 70%, and improves campaign ROI through better data-driven decision making. The system will support multiple user roles and provide customizable reporting features."
    })
  }
  
  // Engineering topics
  if (formData.program.includes('engineering') || formData.program.includes('mechanical') ||
      formData.program.includes('electrical') || formData.program.includes('civil') ||
      interests.some(i => i.toLowerCase().includes('engineering') || i.toLowerCase().includes('automation') ||
        i.toLowerCase().includes('sustainability') || i.toLowerCase().includes('renewable'))) {
    
    topics.push({
      id: 3,
      title: "Smart Energy Management System for Buildings",
      description: "Design and implement an IoT-based system for monitoring and optimizing energy consumption in commercial buildings with predictive analytics.",
      difficulty: "Advanced",
      duration: "6-8 months",
      skills: ["IoT", "Embedded Systems", "Energy Systems", "Data Analytics"],
      resources: [
        { type: "Paper", title: "Smart Building Energy Management Systems", url: "#" },
        { type: "Tutorial", title: "IoT Sensor Networks for Energy Monitoring", url: "#" },
        { type: "Tool", title: "Arduino and Raspberry Pi Integration", url: "#" }
      ],
      tags: ["IoT", "Energy", "Sustainability", "Automation"],
      objectives: [
        "Design and deploy a network of IoT sensors for real-time energy monitoring",
        "Develop predictive algorithms for energy consumption optimization",
        "Create a centralized management system for building operators",
        "Implement automated control systems for HVAC and lighting optimization"
      ],
      methodology: "This project follows a systems engineering approach, beginning with energy audit and requirements analysis. Hardware components will include Arduino/Raspberry Pi-based sensors, wireless communication modules, and actuators. The software stack will comprise embedded C/C++ for sensors, Python for data processing and machine learning, and a web-based dashboard using React.js. Machine learning models will be trained using TensorFlow to predict energy patterns and optimize consumption.",
      expectedOutcomes: "The completed system will demonstrate 15-25% reduction in energy consumption, provide real-time monitoring capabilities, and offer predictive maintenance features. The solution will be scalable to different building types and sizes, with potential for commercial deployment and positive environmental impact."
    })
  }
  
  // Health/Medical topics
  if (formData.program.includes('medicine') || formData.program.includes('nursing') ||
      formData.program.includes('pharmacy') || formData.program.includes('biology') ||
      interests.some(i => i.toLowerCase().includes('health') || i.toLowerCase().includes('medical') ||
        i.toLowerCase().includes('healthcare') || i.toLowerCase().includes('biotechnology'))) {
    
    topics.push({
      id: 4,
      title: "Telemedicine Platform for Remote Patient Monitoring",
      description: "Develop a comprehensive telemedicine platform that enables remote patient monitoring, virtual consultations, and health data tracking.",
      difficulty: "Advanced",
      duration: "7-9 months",
      skills: ["Web Development", "Mobile Development", "Healthcare Systems", "Data Security"],
      resources: [
        { type: "Paper", title: "Telemedicine: Current Applications and Future Prospects", url: "#" },
        { type: "Tutorial", title: "Healthcare App Development", url: "#" },
        { type: "Tool", title: "HIPAA Compliance Guidelines", url: "#" }
      ],
      tags: ["Healthcare", "Telemedicine", "Mobile Health", "Patient Care"]
    })
  }
  
  // Social Sciences/Psychology topics
  if (formData.program.includes('psychology') || formData.program.includes('sociology') ||
      formData.program.includes('education') || formData.program.includes('social') ||
      interests.some(i => i.toLowerCase().includes('psychology') || i.toLowerCase().includes('social') ||
        i.toLowerCase().includes('education') || i.toLowerCase().includes('behavior'))) {
    
    topics.push({
      id: 5,
      title: "Social Media Impact on Mental Health Study",
      description: "Conduct a comprehensive research study analyzing the relationship between social media usage patterns and mental health outcomes among university students.",
      difficulty: "Intermediate",
      duration: "5-7 months",
      skills: ["Research Methods", "Statistics", "Data Analysis", "Survey Design"],
      resources: [
        { type: "Paper", title: "Social Media and Mental Health: A Systematic Review", url: "#" },
        { type: "Tutorial", title: "Statistical Analysis with SPSS", url: "#" },
        { type: "Tool", title: "Survey Design Best Practices", url: "#" }
      ],
      tags: ["Psychology", "Social Media", "Mental Health", "Research"]
    })
  }
  
  // Environmental/Sustainability topics
  if (formData.program.includes('environmental') || formData.program.includes('biology') ||
      interests.some(i => i.toLowerCase().includes('environment') || i.toLowerCase().includes('climate') ||
        i.toLowerCase().includes('sustainability') || i.toLowerCase().includes('renewable'))) {
    
    topics.push({
      id: 6,
      title: "Climate Change Impact Assessment Tool",
      description: "Develop a web-based tool for assessing and visualizing the potential impacts of climate change on local communities and ecosystems.",
      difficulty: "Intermediate",
      duration: "6-8 months",
      skills: ["Web Development", "Data Visualization", "Environmental Science", "GIS"],
      resources: [
        { type: "Paper", title: "Climate Change Impact Assessment Methodologies", url: "#" },
        { type: "Tutorial", title: "Environmental Data Visualization", url: "#" },
        { type: "Tool", title: "GIS Software Documentation", url: "#" }
      ],
      tags: ["Climate Change", "Environmental Science", "Data Visualization", "Sustainability"]
    })
  }
  
  // If no specific topics match, generate generic ones based on skills
  if (topics.length === 0) {
    topics.push({
      id: 1,
      title: "Comprehensive Research Study in Your Field",
      description: `Conduct an in-depth research study focusing on ${interests[0] || 'your area of interest'} using ${skills[0] || 'your skills'} to contribute new knowledge to the field.`,
      difficulty: formData.difficulty === 'beginner' ? 'Beginner' : formData.difficulty === 'advanced' ? 'Advanced' : 'Intermediate',
      duration: formData.duration === '3-4' ? '3-4 months' : formData.duration === '4-6' ? '4-6 months' : formData.duration === '6-8' ? '6-8 months' : '8-12 months',
      skills: skills.slice(0, 4),
      resources: [
        { type: "Paper", title: "Research Methods in Your Field", url: "#" },
        { type: "Tutorial", title: "Academic Writing and Research", url: "#" },
        { type: "Tool", title: "Research Tools and Databases", url: "#" }
      ],
      tags: ["Research", "Academic Study", "Field Analysis"]
    })
  }
  
  return topics.slice(0, 3) // Return up to 3 topics
}

// Authentication methods
const openAuthModal = (mode = 'login') => {
  authModalMode.value = mode
  authModalOpen.value = true
}

const closeAuthModal = () => {
  authModalOpen.value = false
}

const handleAuthSuccess = async (type) => {
  console.log('Authentication successful:', type)
  closeAuthModal()
  
  // Wait a moment for user data to be fetched
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Check if user needs to complete profile (anyone who hasn't completed onboarding)
  if (currentUser.value && !currentUser.value.onboarding_completed) {
    // Show profile completion modal
    profileCompletionModalOpen.value = true
  } else {
    // Redirect to home view if profile already completed
    setActiveView('home')
  }
}

const handleProfileCompletion = async (skipped) => {
  profileCompletionModalOpen.value = false
  
  console.log(skipped ? 'Profile completion skipped' : 'Profile completed')
  
  // Redirect to home view after profile completion
  setActiveView('home')
  
  // If the user completed their profile, show onboarding tutorial
  if (!skipped && currentUser.value) {
    // Optional: Show a success message
    setTimeout(() => {
      console.log('Profile setup complete! You can now explore the system.')
    }, 500)
  }
}

const handleLogout = async () => {
  try {
    await authService.logout()
    console.log('User logged out successfully')
    // Redirect to home view after logout
    setActiveView('home')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

const openProfileModal = () => {
  profileModalOpen.value = true
}

const closeProfileModal = () => {
  profileModalOpen.value = false
}

const handleProfileUpdated = () => {
  console.log('Profile updated successfully')
}

const toggleUserDropdown = (event) => {
  event.stopPropagation()
  userDropdownOpen.value = !userDropdownOpen.value
}

const handleClickOutside = () => {
  userDropdownOpen.value = false
}

const openProfileModalFromDropdown = () => {
  userDropdownOpen.value = false
  profileModalOpen.value = true
}

const openAdminPanelFromDropdown = () => {
  userDropdownOpen.value = false
  setActiveView('admin')
}

const handleLogoutFromDropdown = async () => {
  userDropdownOpen.value = false
  await handleLogout()
}
</script>
