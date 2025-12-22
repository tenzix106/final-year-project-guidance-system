<template>
  <div class="min-h-screen bg-accent-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Collaborative Workspaces</h1>
          <p class="text-gray-600 mt-1">Work together with your team on FYP projects</p>
        </div>
        <button
          @click="openCreateModal"
          class="flex items-center space-x-2 px-4 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium shadow-md hover:shadow-lg"
        >
          <Plus class="w-5 h-5" />
          <span>New Workspace</span>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <Loader2 class="w-8 h-8 animate-spin text-primary-600" />
      </div>

      <!-- My Workspaces Section (only show when user has workspaces) -->
      <div v-if="workspaces.length > 0" class="mb-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">My Workspaces</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="workspace in workspaces"
            :key="workspace.id"
            class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all cursor-pointer"
            @click="viewWorkspace(workspace)"
          >
            <div class="p-6">
              <!-- Header -->
              <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ workspace.name }}</h3>
                  <p class="text-sm text-gray-600 line-clamp-2">{{ workspace.description || 'No description' }}</p>
                </div>
                <div class="ml-3">
                  <span :class="getRoleBadgeClass(workspace.user_role)" class="px-2.5 py-1 rounded-full text-xs font-medium">
                    {{ getRoleLabel(workspace.user_role) }}
                  </span>
                </div>
              </div>

              <!-- Owner -->
              <div class="flex items-center space-x-2 text-sm text-gray-600 mb-4">
                <User class="w-4 h-4" />
                <span>{{ workspace.owner_name || workspace.owner_email }}</span>
              </div>

              <!-- Members -->
              <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                <div class="flex items-center space-x-2">
                  <Users class="w-4 h-4 text-gray-500" />
                  <span class="text-sm text-gray-600">
                    {{ workspace.member_count }} {{ workspace.member_count === 1 ? 'member' : 'members' }}
                  </span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <Globe v-if="workspace.is_public" class="w-4 h-4 text-green-600" title="Public workspace" />
                  <Lock v-else class="w-4 h-4 text-gray-400" title="Private workspace" />
                </div>
              </div>

              <!-- Updated -->
              <div class="mt-3 text-xs text-gray-500">
                Updated {{ formatDate(workspace.updated_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>



      <!-- Discover Public Workspaces -->
      <div v-if="!loading">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">{{ workspaces.length === 0 ? 'Join a Public Workspace' : 'Discover More Workspaces' }}</h2>
            <p v-if="workspaces.length === 0" class="text-gray-600 mt-1">Browse and join public workspaces or create your own</p>
          </div>
          <button
            @click="loadDiscoverWorkspaces"
            class="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center space-x-1"
          >
            <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loadingDiscover }" />
            <span>Refresh</span>
          </button>
        </div>

        <div v-if="loadingDiscover" class="flex items-center justify-center py-12">
          <Loader2 class="w-6 h-6 animate-spin text-primary-600" />
        </div>

        <div v-else-if="discoverWorkspaces.length === 0" class="text-center py-16 bg-white rounded-xl border-2 border-dashed border-gray-300">
          <Globe class="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-semibold text-gray-900 mb-2">No Public Workspaces Available</h3>
          <p class="text-gray-600 mb-6">Be the first to create a public workspace</p>
          <button
            @click="openCreateModal"
            class="inline-flex items-center space-x-2 px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
          >
            <Plus class="w-5 h-5" />
            <span>Create Workspace</span>
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="workspace in discoverWorkspaces"
            :key="workspace.id"
            class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all p-6"
          >
            <div class="flex items-start justify-between mb-4">
              <h4 class="font-semibold text-gray-900 text-lg flex-1">{{ workspace.name }}</h4>
              <Globe class="w-5 h-5 text-green-600 ml-2" />
            </div>
            <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ workspace.description || 'No description' }}</p>
            <div class="flex items-center space-x-2 text-sm text-gray-600 mb-4">
              <User class="w-4 h-4" />
              <span>{{ workspace.owner_name || workspace.owner_email }}</span>
            </div>
            <div class="flex items-center justify-between pt-4 border-t border-gray-100">
              <div class="flex items-center space-x-2 text-sm text-gray-600">
                <Users class="w-4 h-4 text-gray-500" />
                <span>{{ workspace.member_count }} {{ workspace.member_count === 1 ? 'member' : 'members' }}</span>
              </div>
              <button
                @click.stop="joinWorkspace(workspace)"
                :disabled="joiningWorkspace === workspace.id"
                class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors text-sm font-medium disabled:opacity-50"
              >
                {{ joiningWorkspace === workspace.id ? 'Joining...' : 'Join' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Workspace Modal -->
    <CreateWorkspaceModal
      :is-open="createModalOpen"
      @close="createModalOpen = false"
      @created="handleWorkspaceCreated"
    />

    <!-- Workspace Details Modal -->
    <WorkspaceDetailsModal
      :is-open="detailsModalOpen"
      :workspace="selectedWorkspace"
      @close="detailsModalOpen = false"
      @updated="handleWorkspaceUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Plus, Users, User, Globe, Lock, Loader2, RefreshCw } from 'lucide-vue-next'
import workspaceService from '../services/workspaceService.js'
import CreateWorkspaceModal from './CreateWorkspaceModal.vue'
import WorkspaceDetailsModal from './WorkspaceDetailsModal.vue'
import { authReady } from '../services/authService.js'

const workspaces = ref([])
const discoverWorkspaces = ref([])
const selectedWorkspace = ref(null)
const loading = ref(false)
const loadingDiscover = ref(false)
const createModalOpen = ref(false)
const detailsModalOpen = ref(false)
const joiningWorkspace = ref(null)

onMounted(async () => {
  // Wait for auth to be ready before loading workspaces
  if (authReady.value) {
    await loadWorkspaces()
    await loadDiscoverWorkspaces()
  } else {
    // Watch for authReady to become true
    const unwatch = watch(authReady, async (ready) => {
      if (ready) {
        await loadWorkspaces()
        await loadDiscoverWorkspaces()
        unwatch() // Stop watching once loaded
      }
    })
  }
})

const loadWorkspaces = async () => {
  loading.value = true
  try {
    workspaces.value = await workspaceService.getWorkspaces()
  } catch (error) {
    console.error('Failed to load workspaces:', error)
  } finally {
    loading.value = false
  }
}

const loadDiscoverWorkspaces = async () => {
  loadingDiscover.value = true
  try {
    discoverWorkspaces.value = await workspaceService.discoverWorkspaces()
  } catch (error) {
    console.error('Failed to discover workspaces:', error)
  } finally {
    loadingDiscover.value = false
  }
}

const openCreateModal = () => {
  createModalOpen.value = true
}

const viewWorkspace = (workspace) => {
  selectedWorkspace.value = workspace
  detailsModalOpen.value = true
}

const joinWorkspace = async (workspace) => {
  joiningWorkspace.value = workspace.id
  try {
    await workspaceService.joinWorkspace(workspace.id)
    // Refresh both lists
    await loadWorkspaces()
    await loadDiscoverWorkspaces()
  } catch (error) {
    console.error('Failed to join workspace:', error)
    alert(error.message || 'Failed to join workspace')
  } finally {
    joiningWorkspace.value = null
  }
}

const handleWorkspaceCreated = async () => {
  createModalOpen.value = false
  await loadWorkspaces()
}

const handleWorkspaceUpdated = async () => {
  await loadWorkspaces()
}

const getRoleLabel = (role) => {
  const labels = {
    owner: 'Owner',
    admin: 'Admin',
    member: 'Member',
    viewer: 'Viewer'
  }
  return labels[role] || role
}

const getRoleBadgeClass = (role) => {
  const classes = {
    owner: 'bg-purple-100 text-purple-700',
    admin: 'bg-blue-100 text-blue-700',
    member: 'bg-green-100 text-green-700',
    viewer: 'bg-gray-100 text-gray-700'
  }
  return classes[role] || 'bg-gray-100 text-gray-700'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else {
    return date.toLocaleDateString('en-MY', { day: 'numeric', month: 'short', year: 'numeric' })
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
