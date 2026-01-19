<template>
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <h3 class="text-3xl font-bold text-gray-900 mb-4">Generated Project Topics</h3>
      <p class="text-gray-600">AI-powered suggestions tailored to your profile and preferences</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-20">
      <div class="inline-flex items-center space-x-3">
        <Loader2 class="w-8 h-8 text-primary-600 animate-spin" />
        <span class="text-lg text-gray-600">Generating personalized project topics...</span>
      </div>
      <div class="mt-8 max-w-md mx-auto">
        <div class="bg-gray-200 rounded-full h-2">
          <div class="bg-primary-600 h-2 rounded-full animate-pulse" style="width: 60%"></div>
        </div>
        <p class="text-sm text-gray-500 mt-2">Analyzing your preferences and matching with available resources...</p>
      </div>
    </div>

    <!-- Results -->
    <div v-else-if="topics.length > 0" class="space-y-8">
      <div v-for="(topic, index) in topics" :key="topic.id" 
           class="card hover:shadow-2xl transition-all duration-300 animate-slide-up"
           :style="{ animationDelay: `${index * 0.1}s` }">
        
        <!-- Topic Header -->
        <div class="flex items-start justify-between mb-6">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-lg">{{ index + 1 }}</span>
              </div>
              <div>
                <h4 class="text-2xl font-bold text-gray-900">{{ topic.title }}</h4>
                <div class="flex items-center space-x-4 mt-1">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                        :class="getDifficultyClass(topic.difficulty)">
                    {{ topic.difficulty }}
                  </span>
                  <span class="text-gray-500 text-sm">
                    <Clock class="w-4 h-4 inline mr-1" />
                    {{ topic.duration }}
                  </span>
                </div>
              </div>
            </div>
            <p class="text-gray-600 text-lg leading-relaxed">{{ topic.description }}</p>
          </div>
        </div>

        <!-- Skills Required -->
        <div class="mb-6">
          <h5 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
            <Code class="w-4 h-4 mr-2" />
            Required Skills
          </h5>
          <div class="flex flex-wrap gap-2">
            <span v-for="skill in topic.skills" :key="skill"
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
              {{ skill }}
            </span>
          </div>
        </div>

        <!-- Tags -->
        <div class="mb-6">
          <h5 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
            <Tag class="w-4 h-4 mr-2" />
            Categories
          </h5>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in topic.tags" :key="tag"
                  class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-purple-100 text-purple-800">
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- Resources -->
        <div class="mb-6">
          <h5 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
            <BookOpen class="w-4 h-4 mr-2" />
            Recommended Resources
          </h5>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="resource in topic.resources" :key="resource.title"
                 class="p-4 border border-gray-200 rounded-lg hover:border-primary-300 transition-colors">
              <div class="flex items-start space-x-3">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center"
                     :class="getResourceTypeClass(resource.type)">
                  <component :is="getResourceIcon(resource.type)" class="w-4 h-4" />
                </div>
                <div class="flex-1">
                  <h6 class="font-medium text-gray-900 text-sm">{{ resource.title }}</h6>
                  <span class="text-xs text-gray-500">{{ resource.type }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
          <button @click="openProposal(topic)" class="btn-primary flex-1">
            <FileText class="w-4 h-4 mr-2" />
            View Full Proposal
          </button>
          <button 
            @click="toggleFavourite(topic)" 
            :disabled="isSavingFavourite(topic.title)"
            :class="[
              'btn-secondary',
              isFavourite(topic.title) ? 'bg-red-50 text-red-600 border-red-200 hover:bg-red-100' : '',
              isSavingFavourite(topic.title) ? 'opacity-50 cursor-not-allowed' : ''
            ]">
            <component 
              :is="isSavingFavourite(topic.title) ? Loader2 : Heart" 
              :class="[
                'w-4 h-4 mr-2',
                isSavingFavourite(topic.title) ? 'animate-spin' : '',
                isFavourite(topic.title) ? 'fill-current' : ''
              ]"
            />
            {{ isFavourite(topic.title) ? 'Remove from Favourites' : 'Save to Favourites' }}
          </button>
        </div>
      </div>

      <!-- Load More Button -->
      <div class="text-center pt-8">
        <button @click="generateMore" class="btn-secondary">
          <Plus class="w-4 h-4 mr-2" />
          Generate More Topics
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-20">
      <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <Search class="w-12 h-12 text-gray-400" />
      </div>
      <h4 class="text-xl font-semibold text-gray-900 mb-2">No topics generated yet</h4>
      <p class="text-gray-600 mb-6">Fill out the form above to get personalized project suggestions</p>
      <button @click="scrollToForm" class="btn-primary">
        <ArrowUp class="w-4 h-4 mr-2" />
        Go to Form
      </button>
    </div>

    <!-- Proposal Modal -->
    <ProposalModal 
      :is-open="isModalOpen" 
      :topic="selectedTopic" 
      @close="closeProposal" 
    />
  </div>
</template>

<script setup>
import { 
  Loader2, Clock, Code, Tag, BookOpen, FileText, Heart, 
  Plus, Search, ArrowUp, FileText as PaperIcon, 
  PlayCircle as TutorialIcon, Wrench as ToolIcon 
} from 'lucide-vue-next'
import { ref, computed, onMounted, watch } from 'vue'
import ProposalModal from './ProposalModal.vue'
import favouriteService from '../services/favouriteService.js'
import authService from '../services/authService.js'

const emit = defineEmits(['generate-more'])

const props = defineProps({
  topics: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Modal state
const isModalOpen = ref(false)
const selectedTopic = ref(null)

// Favourites state
const savingFavourites = ref(new Set())
const favouriteStatuses = ref(new Map())

// Load favourite statuses when topics change
const loadFavouriteStatuses = async () => {
  for (const topic of props.topics) {
    try {
      const status = await favouriteService.checkFavouriteStatus(topic.title)
      favouriteStatuses.value.set(topic.title, status)
    } catch (error) {
      console.error('Error checking favourite status:', error)
    }
  }
}

// Check if topic is favourite
const isFavourite = (topicTitle) => {
  const status = favouriteStatuses.value.get(topicTitle)
  return status?.is_favourite || false
}

// Save/unsave favourite
const toggleFavourite = async (topic) => {
  // Check authentication first
  if (!authService.authenticated) {
    alert('Please log in to save favourites')
    return
  }

  const isCurrentlyFavourite = isFavourite(topic.title)
  savingFavourites.value.add(topic.title)
  
  try {
    if (isCurrentlyFavourite) {
      // Remove from favourites
      const status = favouriteStatuses.value.get(topic.title)
      if (status?.favourite_id) {
        await favouriteService.removeFavourite(status.favourite_id)
        // Update local state after successful removal
        favouriteStatuses.value.set(topic.title, { is_favourite: false, favourite_id: null })
      }
    } else {
      // Add to favourites
      const result = await favouriteService.saveFavourite(topic)
      // Refresh the favourite status from the server to get the favourite_id
      const updatedStatus = await favouriteService.checkFavouriteStatus(topic.title)
      favouriteStatuses.value.set(topic.title, updatedStatus)
    }
  } catch (error) {
    console.error('Error toggling favourite:', error)
    // Show error message to user
    alert(`Error ${isCurrentlyFavourite ? 'removing' : 'saving'} favourite: ${error.message}`)
  } finally {
    savingFavourites.value.delete(topic.title)
  }
}

// Check if currently saving
const isSavingFavourite = (topicTitle) => {
  return savingFavourites.value.has(topicTitle)
}

const openProposal = (topic) => {
  selectedTopic.value = topic
  isModalOpen.value = true
}

const closeProposal = () => {
  isModalOpen.value = false
  selectedTopic.value = null
}

const getDifficultyClass = (difficulty) => {
  const classes = {
    'Beginner': 'bg-green-100 text-green-800',
    'Intermediate': 'bg-yellow-100 text-yellow-800',
    'Advanced': 'bg-red-100 text-red-800'
  }
  return classes[difficulty] || 'bg-gray-100 text-gray-800'
}

const getResourceTypeClass = (type) => {
  const classes = {
    'Paper': 'bg-blue-100 text-blue-600',
    'Tutorial': 'bg-green-100 text-green-600',
    'Tool': 'bg-purple-100 text-purple-600'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

const getResourceIcon = (type) => {
  const icons = {
    'Paper': PaperIcon,
    'Tutorial': TutorialIcon,
    'Tool': ToolIcon
  }
  return icons[type] || BookOpen
}

const scrollToForm = () => {
  document.getElementById('form')?.scrollIntoView({ behavior: 'smooth' })
}

const generateMore = () => {
  emit('generate-more')
  scrollToForm()
}

// Load favourite statuses when component mounts or topics change
onMounted(() => {
  if (props.topics.length > 0) {
    loadFavouriteStatuses()
  }
})

// Watch for topics changes
watch(() => props.topics, (newTopics) => {
  if (newTopics && newTopics.length > 0) {
    loadFavouriteStatuses()
  }
}, { immediate: true })
</script>
