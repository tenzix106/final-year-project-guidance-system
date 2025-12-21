<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeModal">
    <div class="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden animate-fade-in">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
            <FileText class="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Project Proposal</h2>
            <p class="text-gray-600">{{ topic?.title }}</p>
          </div>
        </div>
        <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
          <X class="w-6 h-6 text-gray-500" />
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
        <div class="space-y-8">
          <!-- Project Overview -->
          <section>
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <BookOpen class="w-5 h-5 mr-2 text-primary-600" />
              Project Overview
            </h3>
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-100">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div class="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div class="text-2xl font-bold text-primary-600">{{ topic?.difficulty }}</div>
                  <div class="text-sm text-gray-600 font-medium">Difficulty Level</div>
                </div>
                <div class="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div class="text-2xl font-bold text-primary-600">{{ topic?.duration }}</div>
                  <div class="text-sm text-gray-600 font-medium">Duration</div>
                </div>
                <div class="text-center p-4 bg-white rounded-lg shadow-sm">
                  <div class="text-2xl font-bold text-primary-600">{{ topic?.skills?.length || 0 }}</div>
                  <div class="text-sm text-gray-600 font-medium">Skills Required</div>
                </div>
              </div>
              <div class="bg-white rounded-lg p-4 shadow-sm">
                <p class="text-gray-700 text-lg leading-relaxed">{{ topic?.description }}</p>
              </div>
            </div>
          </section>

          <!-- Objectives -->
          <section v-if="topic?.objectives">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Target class="w-5 h-5 mr-2 text-primary-600" />
              Project Objectives
            </h3>
            <ul class="space-y-3">
              <li v-for="(objective, index) in topic.objectives" :key="index" 
                  class="flex items-start space-x-3">
                <div class="w-6 h-6 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-sm font-medium">{{ index + 1 }}</span>
                </div>
                <span class="text-gray-700">{{ objective }}</span>
              </li>
            </ul>
          </section>

          <!-- Methodology -->
          <section v-if="topic?.methodology">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Settings class="w-5 h-5 mr-2 text-primary-600" />
              Methodology
            </h3>
            <div class="bg-blue-50 rounded-lg p-6">
              <p class="text-gray-700 leading-relaxed">{{ topic.methodology }}</p>
            </div>
          </section>

          <!-- Required Skills & Technologies -->
          <section>
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Code class="w-5 h-5 mr-2 text-primary-600" />
              Required Skills & Technologies
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 class="font-semibold text-gray-700 mb-3">Technical Skills</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="skill in topic?.skills" :key="skill"
                        class="inline-flex items-center px-3 py-2 rounded-full text-sm bg-blue-100 text-blue-800 font-medium">
                    {{ skill }}
                  </span>
                </div>
              </div>
              <div>
                <h4 class="font-semibold text-gray-700 mb-3">Categories</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tag in topic?.tags" :key="tag"
                        class="inline-flex items-center px-3 py-2 rounded-full text-sm bg-purple-100 text-purple-800 font-medium">
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </section>

          <!-- Expected Outcomes -->
          <section v-if="topic?.expectedOutcomes">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <CheckCircle class="w-5 h-5 mr-2 text-primary-600" />
              Expected Outcomes
            </h3>
            <div class="bg-green-50 rounded-lg p-6">
              <p class="text-gray-700 leading-relaxed">{{ topic.expectedOutcomes }}</p>
            </div>
          </section>

          <!-- Resources -->
          <section v-if="topic?.resources?.length">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <BookOpen class="w-5 h-5 mr-2 text-primary-600" />
              Recommended Resources
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="resource in topic.resources" :key="resource.title"
                   class="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all duration-300 cursor-pointer group">
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform"
                       :class="getResourceTypeClass(resource.type)">
                    <component :is="getResourceIcon(resource.type)" class="w-5 h-5" />
                  </div>
                  <div class="flex-1">
                    <h6 class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{{ resource.title }}</h6>
                    <span class="text-sm text-gray-600">{{ resource.type }}</span>
                    <p class="text-sm text-gray-500 mt-1 group-hover:text-primary-500 transition-colors">Click to access resource</p>
                  </div>
                  <div class="opacity-0 group-hover:opacity-100 transition-opacity">
                    <ExternalLink class="w-4 h-4 text-primary-600" />
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Timeline (if available) -->
          <section v-if="getProjectTimeline().length > 0">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Calendar class="w-5 h-5 mr-2 text-primary-600" />
              Suggested Timeline
            </h3>
            <div class="space-y-4">
              <div v-for="(phase, index) in getProjectTimeline()" :key="index"
                   class="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                <div class="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-sm font-bold">{{ index + 1 }}</span>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900">{{ phase.title }}</h4>
                  <p class="text-sm text-gray-600">{{ phase.duration }}</p>
                  <p class="text-gray-700 mt-1">{{ phase.description }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
        <div class="flex items-center space-x-4">
          <button class="btn-secondary">
            <Download class="w-4 h-4 mr-2" />
            Export PDF
          </button>
          <button class="btn-secondary">
            <Share2 class="w-4 h-4 mr-2" />
            Share Proposal
          </button>
        </div>
        <div class="flex items-center space-x-3">
          <button @click="closeModal" class="btn-secondary">
            Close
          </button>
          <button class="btn-primary">
            <Heart class="w-4 h-4 mr-2" />
            Save to Favourites
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  X, FileText, BookOpen, Target, Settings, Code, CheckCircle, 
  Calendar, Download, Share2, Heart, ExternalLink,
  FileText as PaperIcon, PlayCircle as TutorialIcon, Wrench as ToolIcon 
} from 'lucide-vue-next'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  topic: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
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

const getProjectTimeline = () => {
  if (!props.topic) return []
  
  // Generate a basic timeline based on duration and difficulty
  const duration = props.topic.duration
  const difficulty = props.topic.difficulty
  
  if (duration?.includes('3-4')) {
    return [
      { title: 'Research & Planning', duration: '2-3 weeks', description: 'Literature review, requirement analysis, and project planning' },
      { title: 'Design & Prototyping', duration: '4-5 weeks', description: 'System design, architecture planning, and initial prototypes' },
      { title: 'Implementation', duration: '6-8 weeks', description: 'Core development and feature implementation' },
      { title: 'Testing & Documentation', duration: '2-3 weeks', description: 'Testing, bug fixes, and documentation' }
    ]
  } else if (duration?.includes('4-6')) {
    return [
      { title: 'Research & Analysis', duration: '3-4 weeks', description: 'Comprehensive literature review and requirement gathering' },
      { title: 'Design & Architecture', duration: '4-5 weeks', description: 'Detailed system design and technology selection' },
      { title: 'Development Phase 1', duration: '6-8 weeks', description: 'Core functionality and basic features' },
      { title: 'Development Phase 2', duration: '4-6 weeks', description: 'Advanced features and integrations' },
      { title: 'Testing & Refinement', duration: '3-4 weeks', description: 'Comprehensive testing and optimization' }
    ]
  } else if (duration?.includes('6-8') || duration?.includes('8-12')) {
    return [
      { title: 'Research & Planning', duration: '4-5 weeks', description: 'In-depth research and comprehensive project planning' },
      { title: 'System Design', duration: '3-4 weeks', description: 'Detailed architecture and technical specifications' },
      { title: 'Development Sprint 1', duration: '6-8 weeks', description: 'Core system development and basic functionality' },
      { title: 'Development Sprint 2', duration: '6-8 weeks', description: 'Advanced features and system integration' },
      { title: 'Testing & Validation', duration: '4-5 weeks', description: 'Comprehensive testing and performance validation' },
      { title: 'Documentation & Deployment', duration: '2-3 weeks', description: 'Final documentation and system deployment' }
    ]
  }
  
  return []
}

// Close modal on escape key
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    closeModal()
  }
}

// Add event listener when component mounts
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>