<template>
  <transition name="modal">
    <div v-if="isOpen && workspace" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4" @click.self="handleClose">
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 p-6 rounded-t-2xl sticky top-0 z-10">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-white">{{ workspace.name }}</h2>
              <p class="text-primary-100 mt-1">{{ workspace.description || 'No description' }}</p>
            </div>
            <button @click="handleClose" class="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
              <X class="w-6 h-6 text-white" />
            </button>
          </div>
          
          <!-- Tabs -->
          <div class="flex space-x-6 mt-4">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex items-center space-x-2 pb-2 border-b-2 transition-colors',
                activeTab === tab.id
                  ? 'border-white text-white'
                  : 'border-transparent text-primary-100 hover:text-white hover:border-primary-200'
              ]"
            >
              <component :is="tab.icon" class="w-4 h-4" />
              <span class="text-sm font-medium">{{ tab.label }}</span>
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'" class="space-y-6">
            <!-- Linked Project -->
            <div v-if="workspace.saved_project" class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 mb-2">Linked Project</h3>
                  <p class="text-gray-700 font-medium">{{ workspace.saved_project.custom_title || workspace.saved_project.project_topic?.title || 'Untitled Project' }}</p>
                  <p class="text-sm text-gray-600 mt-1">{{ workspace.saved_project.project_topic?.description }}</p>
                </div>
                <FileText class="w-8 h-8 text-blue-600" />
              </div>
              
              <!-- Research Papers Section -->
              <div class="border-t border-blue-200 pt-4 mt-4">
                <div v-if="loadingPapers" class="flex items-center justify-center py-4">
                  <Loader2 class="w-5 h-5 text-blue-600 animate-spin mr-2" />
                  <span class="text-sm text-gray-600">Fetching research papers...</span>
                </div>
                
                <div v-else-if="researchPapers.length > 0" class="space-y-3">
                  <div class="flex items-center justify-between mb-2">
                    <h4 class="text-sm font-semibold text-gray-900 flex items-center">
                      <BookOpen class="w-4 h-4 mr-2 text-blue-600" />
                      Research Papers ({{ researchPapers.length }})
                    </h4>
                    <button
                      @click="togglePapersExpanded"
                      class="text-xs text-blue-600 hover:text-blue-700 font-medium"
                    >
                      {{ showAllPapers ? 'Show Less' : 'Show All' }}
                    </button>
                  </div>
                  
                  <div class="space-y-2 max-h-60 overflow-y-auto">
                    <div
                      v-for="(paper, idx) in displayedPapers"
                      :key="idx"
                      class="bg-white rounded-lg p-3 border border-blue-100 hover:border-blue-300 transition-colors"
                    >
                      <a
                        :href="paper.url"
                        target="_blank"
                        class="text-sm font-medium text-blue-600 hover:text-blue-700 line-clamp-2"
                      >
                        {{ paper.title }}
                      </a>
                      <div class="flex items-center space-x-3 mt-1 text-xs text-gray-500">
                        <span v-if="paper.authors">{{ paper.authors }}</span>
                        <span v-if="paper.year">{{ paper.year }}</span>
                        <span v-if="paper.citations > 0" class="flex items-center">
                          <Quote class="w-3 h-3 mr-1" />
                          {{ paper.citations }} citations
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div v-else class="text-center py-3">
                  <button
                    @click="fetchResearchPapers"
                    class="inline-flex items-center px-4 py-2 text-sm bg-white border border-blue-300 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors"
                  >
                    <BookOpen class="w-4 h-4 mr-2" />
                    Find Research Papers
                  </button>
                  <p class="text-xs text-gray-500 mt-2">Discover relevant academic papers for this project</p>
                </div>
              </div>
            </div>
            
            <!-- Quick Stats -->
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center space-x-2 text-gray-600 mb-1">
                  <Users class="w-4 h-4" />
                  <span class="text-sm">Members</span>
                </div>
                <p class="text-2xl font-bold text-gray-900">{{ workspace.member_count }}</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center space-x-2 text-gray-600 mb-1">
                  <Globe class="w-4 h-4" />
                  <span class="text-sm">Visibility</span>
                </div>
                <p class="text-lg font-semibold text-gray-900">{{ workspace.is_public ? 'Public' : 'Private' }}</p>
              </div>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center space-x-2 text-gray-600 mb-1">
                  <Clock class="w-4 h-4" />
                  <span class="text-sm">Created</span>
                </div>
                <p class="text-sm font-medium text-gray-900">{{ formatDate(workspace.created_at) }}</p>
              </div>
            </div>
          </div>

          <!-- Activity Tab -->
          <div v-if="activeTab === 'activity'" class="h-[500px]">
            <WorkspaceActivity :workspace-id="workspace.id" />
          </div>

          <!-- Chat Tab -->
          <div v-if="activeTab === 'chat'" class="h-[500px]">
            <WorkspaceChat 
              :workspace-id="workspace.id" 
              :is-owner="workspace.user_role === 'owner'"
            />
          </div>

          <!-- Files Tab -->
          <div v-if="activeTab === 'files'" class="h-[500px]">
            <WorkspaceFiles :workspace="workspace" />
          </div>

          <!-- Members Tab -->
          <div v-if="activeTab === 'members'" class="space-y-6">
            <div class="mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Members ({{ workspace.member_count }})</h3>
            </div>

            <!-- Members List -->
            <div class="space-y-2">
              <div
                v-for="member in workspace.members"
                :key="member.id"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center">
                    <User class="w-5 h-5" />
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ member.user_name || member.user_email }}</p>
                    <p class="text-sm text-gray-500">{{ member.user_email }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <span :class="getRoleBadgeClass(member.role)" class="px-2.5 py-1 rounded-full text-xs font-medium">
                    {{ getRoleLabel(member.role) }}
                  </span>
                  <button
                    v-if="canRemoveMember(member)"
                    @click="confirmRemoveMember(member)"
                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Settings Tab -->
          <div v-if="activeTab === 'settings'" class="space-y-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Workspace Settings</h3>
            
            <!-- Owner/Admin Settings -->
            <div v-if="isOwnerOrAdmin" class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900">Public Workspace</p>
                  <p class="text-sm text-gray-600">Allow others to discover this workspace</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    :checked="workspace.is_public"
                    @change="togglePublic"
                    class="sr-only peer"
                  />
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            </div>
            
            <!-- Member Settings -->
            <div v-if="!isOwnerOrAdmin" class="space-y-4">
              <div class="bg-amber-50 border border-amber-200 rounded-lg p-4">
                <h4 class="font-medium text-gray-900 mb-2">Leave Workspace</h4>
                <p class="text-sm text-gray-600 mb-4">If you no longer want to be part of this workspace, you can leave at any time.</p>
                <button
                  @click="confirmLeave"
                  class="flex items-center space-x-2 px-4 py-2 bg-amber-100 text-amber-700 rounded-lg hover:bg-amber-200 transition-colors font-medium"
                >
                  <LogOut class="w-4 h-4" />
                  <span>Leave Workspace</span>
                </button>
              </div>
            </div>

            <!-- Danger Zone (Owner only) -->
            <div v-if="workspace.user_role === 'owner'" class="pt-6 border-t border-red-200">
              <h3 class="text-lg font-semibold text-red-600 mb-4">Danger Zone</h3>
              <button
                @click="confirmDelete"
                class="flex items-center space-x-2 px-4 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors font-medium"
              >
                <Trash2 class="w-4 h-4" />
                <span>Delete Workspace</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { X, User, Trash2, Users, Globe, FileText, Clock, LayoutGrid, Settings, MessageCircle, FolderOpen, Activity, LogOut, BookOpen, Loader2, Quote } from 'lucide-vue-next'
import workspaceService from '../services/workspaceService.js'
import scholarService from '../services/scholarService.js'
import WorkspaceChat from './WorkspaceChat.vue'
import WorkspaceFiles from './WorkspaceFiles.vue'
import WorkspaceActivity from './WorkspaceActivity.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  workspace: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'updated'])

const activeTab = ref('overview')
const tabs = [
  { id: 'overview', label: 'Overview', icon: LayoutGrid },
  { id: 'activity', label: 'Activity', icon: Activity },
  { id: 'chat', label: 'Chat', icon: MessageCircle },
  { id: 'files', label: 'Files', icon: FolderOpen },
  { id: 'members', label: 'Members', icon: Users },
  { id: 'settings', label: 'Settings', icon: Settings }
]

const isOwnerOrAdmin = computed(() => {
  return props.workspace && ['owner', 'admin'].includes(props.workspace.user_role)
})

const canRemoveMember = (member) => {
  if (!props.workspace) return false
  if (member.role === 'owner') return false
  return props.workspace.user_role === 'owner' || (props.workspace.user_role === 'admin' && member.role !== 'admin')
}

const handleClose = () => {
  emit('close')
}

const confirmRemoveMember = async (member) => {
  if (confirm(`Remove ${member.user_name || member.user_email} from this workspace?`)) {
    try {
      await workspaceService.removeMember(props.workspace.id, member.id)
      emit('updated')
    } catch (err) {
      alert(`Failed to remove member: ${err.message}`)
    }
  }
}

const togglePublic = async () => {
  try {
    await workspaceService.updateWorkspace(props.workspace.id, {
      is_public: !props.workspace.is_public
    })
    emit('updated')
  } catch (err) {
    alert(`Failed to update workspace: ${err.message}`)
  }
}

const confirmDelete = async () => {
  if (confirm(`Are you sure you want to delete "${props.workspace.name}"? This action cannot be undone.`)) {
    try {
      await workspaceService.deleteWorkspace(props.workspace.id)
      emit('updated')
      handleClose()
    } catch (err) {
      alert(`Failed to delete workspace: ${err.message}`)
    }
  }
}

const confirmLeave = async () => {
  if (confirm(`Are you sure you want to leave "${props.workspace.name}"?`)) {
    try {
      // Find current user's member ID
      const currentMember = props.workspace.members?.find(m => m.is_current_user)
      if (!currentMember) {
        throw new Error('Could not find your membership')
      }
      
      await workspaceService.removeMember(props.workspace.id, currentMember.id)
      emit('updated')
      handleClose()
    } catch (err) {
      alert(`Failed to leave workspace: ${err.message}`)
    }
  }
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
  return date.toLocaleDateString('en-MY', { day: 'numeric', month: 'short', year: 'numeric' })
}

// Research papers functionality
const researchPapers = ref([])
const loadingPapers = ref(false)
const showAllPapers = ref(false)

const displayedPapers = computed(() => {
  if (showAllPapers.value) {
    return researchPapers.value
  }
  return researchPapers.value.slice(0, 3)
})

const togglePapersExpanded = () => {
  showAllPapers.value = !showAllPapers.value
}

const fetchResearchPapers = async () => {
  if (!props.workspace?.saved_project) return
  
  loadingPapers.value = true
  try {
    const project = props.workspace.saved_project
    const projectTitle = project.custom_title || project.project_topic?.title || 'Untitled'
    const projectDescription = project.project_topic?.description || ''
    
    const papers = await scholarService.searchPapers(projectTitle, projectDescription, 10)
    researchPapers.value = papers
    
    // Save to localStorage for persistence
    savePapersToStorage()
  } catch (error) {
    console.error('Error fetching research papers:', error)
    alert('Failed to fetch research papers. Please try again.')
  } finally {
    loadingPapers.value = false
  }
}

const savePapersToStorage = () => {
  if (!props.workspace?.id) return
  
  const storageKey = `workspace_papers_${props.workspace.id}`
  localStorage.setItem(storageKey, JSON.stringify(researchPapers.value))
}

const loadPapersFromStorage = () => {
  if (!props.workspace?.id) return
  
  const storageKey = `workspace_papers_${props.workspace.id}`
  const stored = localStorage.getItem(storageKey)
  
  if (stored) {
    try {
      researchPapers.value = JSON.parse(stored)
    } catch (error) {
      console.error('Error loading papers from storage:', error)
    }
  }
}

// Load papers when workspace changes
watch(() => props.workspace?.id, (newId) => {
  if (newId) {
    researchPapers.value = []
    showAllPapers.value = false
    loadPapersFromStorage()
  }
}, { immediate: true })

</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
