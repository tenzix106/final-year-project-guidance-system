<template>
  <transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4" @click.self="handleClose">
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 p-6 rounded-t-2xl">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-white">Create New Workspace</h2>
              <p class="text-primary-100 mt-1">Set up a collaborative space for your team</p>
            </div>
            <button @click="handleClose" class="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
              <X class="w-6 h-6 text-white" />
            </button>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
          <!-- Workspace Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
              Workspace Name <span class="text-red-500">*</span>
            </label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              required
              placeholder="e.g., AI Project Team"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              v-model="formData.description"
              rows="3"
              placeholder="Brief description of the workspace purpose..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
            ></textarea>
          </div>

          <!-- Link to Saved Project -->
          <div>
            <label for="project" class="block text-sm font-medium text-gray-700 mb-1">
              Link to Saved Project (Optional)
            </label>
            <select
              id="project"
              v-model="formData.saved_project_id"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            >
              <option value="">No linked project</option>
              <option v-for="fav in favourites" :key="fav.id" :value="fav.id">
                {{ fav.custom_title || fav.project_topic?.title || 'Untitled Project' }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Link this workspace to one of your saved projects</p>
          </div>

          <!-- Settings -->
          <div class="space-y-4">
            <h3 class="text-sm font-semibold text-gray-900">Workspace Settings</h3>
            
            <!-- Public/Private -->
            <div class="flex items-start space-x-3">
              <input
                id="is_public"
                v-model="formData.is_public"
                type="checkbox"
                class="mt-1 w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <div class="flex-1">
                <label for="is_public" class="text-sm font-medium text-gray-700 cursor-pointer">
                  Make this workspace public
                </label>
                <p class="text-xs text-gray-500 mt-0.5">
                  Public workspaces can be discovered and viewed by other users
                </p>
              </div>
            </div>

            <!-- Max Members -->
            <div>
              <label for="max_members" class="block text-sm font-medium text-gray-700 mb-1">
                Maximum Members
              </label>
              <input
                id="max_members"
                v-model.number="formData.max_members"
                type="number"
                min="2"
                max="50"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
              <p class="text-xs text-gray-500 mt-1">Maximum number of members allowed (2-50)</p>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-2">
            <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              @click="handleClose"
              class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="creating"
              class="px-6 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Loader2 v-if="creating" class="w-4 h-4 animate-spin" />
              <Plus v-else class="w-4 h-4" />
              <span>{{ creating ? 'Creating...' : 'Create Workspace' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { X, Plus, Loader2, AlertCircle } from 'lucide-vue-next'
import workspaceService from '../services/workspaceService.js'
import favouriteService from '../services/favouriteService.js'
import { authReady } from '../services/authService.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'created'])

const formData = ref({
  name: '',
  description: '',
  saved_project_id: '',
  is_public: false,
  max_members: 10
})

const favourites = ref([])
const creating = ref(false)
const error = ref('')
const favouritesLoaded = ref(false)

onMounted(async () => {
  // Wait for auth to be ready before loading favourites
  if (authReady.value) {
    await loadFavourites()
  } else {
    // Watch for authReady to become true
    const unwatch = watch(authReady, async (ready) => {
      if (ready) {
        await loadFavourites()
        unwatch() // Stop watching once loaded
      }
    })
  }
})

const loadFavourites = async () => {
  if (favouritesLoaded.value) return
  
  try {
    await favouriteService.getFavourites()
    favourites.value = favouriteService.favourites.value
    favouritesLoaded.value = true
  } catch (err) {
    console.error('Failed to load favourites:', err)
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (!isOpen) {
    resetForm()
  }
})

const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    saved_project_id: '',
    is_public: false,
    max_members: 10
  }
  error.value = ''
}

const handleClose = () => {
  emit('close')
}

const handleSubmit = async () => {
  error.value = ''
  creating.value = true

  try {
    const payload = {
      name: formData.value.name,
      description: formData.value.description,
      is_public: formData.value.is_public,
      max_members: formData.value.max_members
    }

    // Only include saved_project_id if a project is actually selected
    if (formData.value.saved_project_id && formData.value.saved_project_id !== '') {
      payload.saved_project_id = parseInt(formData.value.saved_project_id)
    }

    await workspaceService.createWorkspace(payload)
    emit('created')
  } catch (err) {
    error.value = err.message || 'Failed to create workspace'
  } finally {
    creating.value = false
  }
}
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
