<template>
  <div class="max-w-6xl mx-auto py-8">
    <!-- Header -->
    <div class="text-center mb-12">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">My Saved Projects</h2>
      <p class="text-gray-600">Manage your favourite project ideas and track your progress</p>
    </div>

    <!-- Loading State -->
    <div v-if="favouriteService.isLoading.value" class="text-center py-20">
      <div class="inline-flex items-center space-x-3">
        <Loader2 class="w-8 h-8 text-primary-600 animate-spin" />
        <span class="text-lg text-gray-600">Loading your favourites...</span>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="favouriteService.favourites.value.length === 0" class="text-center py-20">
      <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <Heart class="w-12 h-12 text-gray-400" />
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No saved projects yet</h3>
      <p class="text-gray-600 mb-6">Start by generating some project ideas and saving your favourites</p>
      <button @click="goToGenerator" class="btn-primary">
        <Plus class="w-4 h-4 mr-2" />
        Generate Projects
      </button>
    </div>

    <!-- Favourites List -->
    <div v-else class="space-y-6">
      <div v-for="(favourite, index) in favouriteService.favourites.value" :key="favourite.id"
           class="card hover:shadow-lg transition-all duration-300 animate-slide-up"
           :style="{ animationDelay: `${index * 0.1}s` }">
        
        <!-- Project Header -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-8 h-8 bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Heart class="w-4 h-4 text-white fill-current" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">
                  {{ favourite.custom_title || favourite.project_topic?.title || 'Untitled Project' }}
                </h3>
                <div class="flex items-center space-x-3 mt-1">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                        :class="getStatusClass(favourite.status)">
                    {{ formatStatus(favourite.status) }}
                  </span>
                  <span class="text-gray-500 text-sm">
                    <Calendar class="w-3 h-3 inline mr-1" />
                    Saved {{ formatDate(favourite.saved_at) }}
                  </span>
                </div>
              </div>
            </div>
            <p v-if="favourite.project_topic?.description" 
               class="text-gray-600 leading-relaxed">
              {{ favourite.project_topic.description }}
            </p>
          </div>
          
          <!-- Actions Menu -->
          <div class="flex items-center space-x-2">
            <button @click="toggleEditMode(favourite.id)" 
                    class="p-2 text-gray-400 hover:text-gray-600 transition-colors">
              <Edit3 class="w-4 h-4" />
            </button>
            <button @click="removeFavourite(favourite.id)" 
                    class="p-2 text-gray-400 hover:text-red-600 transition-colors"
                    :disabled="removingFavourites.has(favourite.id)">
              <component :is="removingFavourites.has(favourite.id) ? Loader2 : Trash2" 
                         :class="['w-4 h-4', removingFavourites.has(favourite.id) ? 'animate-spin' : '']" />
            </button>
          </div>
        </div>

        <!-- Project Details -->
        <div v-if="favourite.project_topic" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <!-- Difficulty & Duration -->
          <div class="space-y-2">
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-700">Difficulty:</span>
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                    :class="getDifficultyClass(favourite.project_topic.difficulty_level)">
                {{ favourite.project_topic.difficulty_level }}
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <Clock class="w-4 h-4 text-gray-500" />
              <span class="text-sm text-gray-600">{{ favourite.project_topic.estimated_duration }}</span>
            </div>
          </div>

          <!-- Progress -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-700">Progress</span>
              <span class="text-sm text-gray-600">{{ favourite.progress_percentage }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-primary-600 h-2 rounded-full transition-all duration-300" 
                   :style="{ width: `${favourite.progress_percentage}%` }"></div>
            </div>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="favourite.project_topic?.tags?.length" class="mb-4">
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in favourite.project_topic.tags" :key="tag"
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- Notes Section -->
        <div class="border-t border-gray-200 pt-4">
          <div v-if="editingNotes !== favourite.id">
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-medium text-gray-700 flex items-center">
                <FileText class="w-4 h-4 mr-2" />
                My Notes
              </h4>
              <button @click="startEditingNotes(favourite)" 
                      class="text-sm text-primary-600 hover:text-primary-800">
                {{ favourite.user_notes ? 'Edit' : 'Add Notes' }}
              </button>
            </div>
            <p v-if="favourite.user_notes" class="text-gray-600 text-sm">
              {{ favourite.user_notes }}
            </p>
            <p v-else class="text-gray-400 text-sm italic">
              No notes added yet. Click "Add Notes" to add your thoughts about this project.
            </p>
          </div>

          <!-- Edit Notes Form -->
          <div v-else>
            <div class="space-y-3">
              <label class="text-sm font-medium text-gray-700">Notes</label>
              <textarea v-model="editingNotesContent" 
                        placeholder="Add your thoughts, progress updates, or ideas about this project..."
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                        rows="3"></textarea>
              
              <!-- Status Update -->
              <div class="flex items-center space-x-4">
                <label class="text-sm font-medium text-gray-700">Status</label>
                <select v-model="editingStatus" 
                        class="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-primary-500 focus:border-primary-500">
                  <option value="saved">Saved</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="abandoned">Abandoned</option>
                </select>
              </div>

              <!-- Action Buttons -->
              <div class="flex items-center space-x-2">
                <button @click="saveNotes(favourite.id)" 
                        :disabled="savingNotes"
                        class="btn-primary text-sm py-1 px-3">
                  <component :is="savingNotes ? Loader2 : Save" 
                             :class="['w-3 h-3 mr-1', savingNotes ? 'animate-spin' : '']" />
                  Save
                </button>
                <button @click="cancelEditingNotes" class="btn-secondary text-sm py-1 px-3">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  Heart, Plus, Calendar, Edit3, Trash2, Clock, FileText, 
  Loader2, Save 
} from 'lucide-vue-next'
import { ref, onMounted } from 'vue'
import favouriteService from '../services/favouriteService.js'

// Component state
const editingNotes = ref(null)
const editingNotesContent = ref('')
const editingStatus = ref('saved')
const savingNotes = ref(false)
const removingFavourites = ref(new Set())

// Load favourites on component mount
onMounted(async () => {
  try {
    await favouriteService.getFavourites()
  } catch (error) {
    console.error('Error loading favourites:', error)
  }
})

// Edit notes functionality
const startEditingNotes = (favourite) => {
  editingNotes.value = favourite.id
  editingNotesContent.value = favourite.user_notes || ''
  editingStatus.value = favourite.status || 'saved'
}

const cancelEditingNotes = () => {
  editingNotes.value = null
  editingNotesContent.value = ''
  editingStatus.value = 'saved'
}

const saveNotes = async (favouriteId) => {
  savingNotes.value = true
  try {
    await favouriteService.updateNotes(favouriteId, editingNotesContent.value, editingStatus.value)
    cancelEditingNotes()
  } catch (error) {
    console.error('Error saving notes:', error)
    alert('Error saving notes: ' + error.message)
  } finally {
    savingNotes.value = false
  }
}

// Remove favourite
const removeFavourite = async (favouriteId) => {
  if (!confirm('Are you sure you want to remove this project from your favourites?')) {
    return
  }
  
  removingFavourites.value.add(favouriteId)
  try {
    await favouriteService.removeFavourite(favouriteId)
  } catch (error) {
    console.error('Error removing favourite:', error)
    alert('Error removing favourite: ' + error.message)
  } finally {
    removingFavourites.value.delete(favouriteId)
  }
}

// Utility functions
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const formatStatus = (status) => {
  const statusMap = {
    'saved': 'Saved',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'abandoned': 'Abandoned'
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const classes = {
    'saved': 'bg-blue-100 text-blue-800',
    'in_progress': 'bg-yellow-100 text-yellow-800',
    'completed': 'bg-green-100 text-green-800',
    'abandoned': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getDifficultyClass = (difficulty) => {
  const classes = {
    'Beginner': 'bg-green-100 text-green-800',
    'Intermediate': 'bg-yellow-100 text-yellow-800',
    'Advanced': 'bg-red-100 text-red-800'
  }
  return classes[difficulty] || 'bg-gray-100 text-gray-800'
}

const toggleEditMode = (favouriteId) => {
  if (editingNotes.value === favouriteId) {
    cancelEditingNotes()
  } else {
    const favourite = favouriteService.favourites.value.find(f => f.id === favouriteId)
    if (favourite) {
      startEditingNotes(favourite)
    }
  }
}

const goToGenerator = () => {
  // Navigate to the main page where the form/generator is
  // You might want to use Vue Router here if you have multiple pages
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.6s ease-out forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>