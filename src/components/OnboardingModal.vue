<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden animate-fade-in">
      <!-- Header -->
      <div class="relative bg-primary-500 text-white p-8">
        <button 
          @click="skipOnboarding" 
          class="absolute top-4 right-4 px-4 py-2 text-sm bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg transition-colors"
        >
          Skip
        </button>
        <div class="text-center">
          <div class="w-20 h-20 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
            <component :is="currentStepIcon" class="w-10 h-10" />
          </div>
          <h2 class="text-3xl font-bold mb-2">Welcome to FYP Guidance!</h2>
          <p class="text-white text-opacity-90">Let's get you started in just a few steps</p>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="bg-gray-100 px-8 py-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-600">Step {{ currentStep + 1 }} of {{ steps.length }}</span>
          <span class="text-sm font-medium text-primary-600">{{ Math.round(progress) }}%</span>
        </div>
        <div class="w-full bg-gray-300 rounded-full h-2">
          <div 
            class="bg-primary-500 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <!-- Content -->
      <div class="p-8 overflow-y-auto max-h-[50vh]">
        <transition name="slide-fade" mode="out-in">
          <div :key="currentStep" class="space-y-4">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">{{ steps[currentStep].title }}</h3>
            <p class="text-gray-600 text-lg leading-relaxed">{{ steps[currentStep].description }}</p>
            
            <!-- Step-specific content -->
            <!-- <div class="mt-6 bg-gray-50 rounded-xl p-6 border border-gray-200">
              <component :is="steps[currentStep].component" />
            </div> -->
          </div>
        </transition>
      </div>

      <!-- Footer -->
      <div class="bg-gray-50 px-8 py-6 flex items-center justify-between border-t border-gray-200">
        <button
          v-if="currentStep > 0"
          @click="previousStep"
          class="flex items-center space-x-2 px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-xl transition-colors font-medium"
        >
          <ChevronLeft class="w-5 h-5" />
          <span>Back</span>
        </button>
        <div v-else></div>

        <button
          @click="nextStep"
          class="flex items-center space-x-2 px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
        >
          <span>{{ isLastStep ? 'Get Started' : 'Next' }}</span>
          <ChevronRight v-if="!isLastStep" class="w-5 h-5" />
          <CheckCircle v-else class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  Sparkles, FileText, BookOpen, Loader2, ChevronLeft, 
  ChevronRight, CheckCircle, Target, TrendingUp, BookMarked 
} from 'lucide-vue-next'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'complete'])

const currentStep = ref(0)

const steps = [
  {
    title: 'Generate Project Topics',
    description: 'Fill out the form with your interests, skills, and preferences. Our AI will generate personalized FYP topics tailored just for you.',
    icon: 'Sparkles',
    component: {
      template: `
        <div class="space-y-3">
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <FileText class="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Complete the Form</h4>
              <p class="text-gray-600 text-sm">Share your program, interests, and skills</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <Sparkles class="w-5 h-5 text-secondary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">AI Generation</h4>
              <p class="text-gray-600 text-sm">Get AI-powered project suggestions instantly</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-accent-200 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <Target class="w-5 h-5 text-gray-700" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Review & Select</h4>
              <p class="text-gray-600 text-sm">Browse through personalized topics and choose your favorite</p>
            </div>
          </div>
        </div>
      `,
      components: { FileText, Sparkles, Target }
    }
  },
  {
    title: 'Save Your Favorites',
    description: 'Found a project you like? Save it to your favorites! Add notes, track progress, and access academic papers to support your research.',
    icon: 'BookMarked',
    component: {
      template: `
        <div class="space-y-3">
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <BookMarked class="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Bookmark Projects</h4>
              <p class="text-gray-600 text-sm">Save interesting topics to revisit later</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <FileText class="w-5 h-5 text-secondary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Add Notes</h4>
              <p class="text-gray-600 text-sm">Keep track of ideas and modifications</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-accent-200 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <BookOpen class="w-5 h-5 text-gray-700" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Find Research Papers</h4>
              <p class="text-gray-600 text-sm">Access relevant academic papers with one click</p>
            </div>
          </div>
        </div>
      `,
      components: { BookMarked, FileText, BookOpen }
    }
  },
  {
    title: 'Track Your Progress',
    description: 'Use our built-in progress tracker to manage your FYP journey. Create custom timelines, track phases, and stay organized from start to finish.',
    icon: 'TrendingUp',
    component: {
      template: `
        <div class="space-y-3">
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <TrendingUp class="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">5-Phase Timeline</h4>
              <p class="text-gray-600 text-sm">Default structure: Planning → Research → Development → Testing → Documentation</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-secondary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <Sparkles class="w-5 h-5 text-secondary-600" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">AI Customization</h4>
              <p class="text-gray-600 text-sm">Generate personalized timelines based on your project</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-accent-200 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
              <CheckCircle class="w-5 h-5 text-gray-700" />
            </div>
            <div>
              <h4 class="font-semibold text-gray-900">Task Management</h4>
              <p class="text-gray-600 text-sm">Add tasks to each phase and check them off as you go</p>
            </div>
          </div>
        </div>
      `,
      components: { TrendingUp, Sparkles, CheckCircle }
    }
  },
  {
    title: 'You\'re All Set!',
    description: 'Ready to start your FYP journey? Click "Get Started" below to explore the platform and generate your first project topics!',
    icon: 'CheckCircle',
    component: {
      template: `
        <div class="text-center py-6">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle class="w-8 h-8 text-green-600" />
          </div>
          <h4 class="font-semibold text-gray-900 text-xl mb-2">Ready to Begin!</h4>
          <p class="text-gray-600">Start exploring and find the perfect project for your Final Year</p>
        </div>
      `,
      components: { CheckCircle }
    }
  }
]

const currentStepIcon = computed(() => {
  const iconName = steps[currentStep.value].icon
  const icons = { Sparkles, FileText, BookOpen, TrendingUp, CheckCircle, BookMarked, Target }
  return icons[iconName]
})

const progress = computed(() => {
  return ((currentStep.value + 1) / steps.length) * 100
})

const isLastStep = computed(() => {
  return currentStep.value === steps.length - 1
})

const nextStep = () => {
  if (isLastStep.value) {
    completeOnboarding()
  } else {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const skipOnboarding = () => {
  emit('complete', true) // true = skipped
}

const completeOnboarding = () => {
  emit('complete', false) // false = completed normally
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}
</style>
