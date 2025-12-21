<template>
  <transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4" @click.self="handleClose">
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 p-6 rounded-t-2xl">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-white">Complete Your Profile</h2>
              <p class="text-primary-100 mt-1">Help us personalize your experience</p>
            </div>
            <div class="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <UserCog class="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
          <!-- Progress Indicator -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
              <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold', 
                step >= 1 ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-400']">
                1
              </div>
              <div class="w-16 h-1 bg-gray-200">
                <div :class="['h-full bg-primary-500 transition-all duration-300']" :style="{ width: step >= 2 ? '100%' : '0%' }"></div>
              </div>
              <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold', 
                step >= 2 ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-400']">
                2
              </div>
            </div>
            <span class="text-sm text-gray-500">Step {{ step }} of 2</span>
          </div>

          <!-- Step 1: Basic Information -->
          <div v-if="step === 1" class="space-y-4">
            <div>
              <label for="fullName" class="block text-sm font-medium text-gray-700 mb-1">
                Full Name <span class="text-red-500">*</span>
              </label>
              <input
                id="fullName"
                v-model="formData.fullName"
                type="text"
                required
                placeholder="Enter your full name"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label for="university" class="block text-sm font-medium text-gray-700 mb-1">
                University/Institution <span class="text-red-500">*</span>
              </label>
              <input
                id="university"
                v-model="formData.university"
                type="text"
                required
                placeholder="e.g., University of Example"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label for="program" class="block text-sm font-medium text-gray-700 mb-1">
                Program/Major <span class="text-red-500">*</span>
              </label>
              <select
                id="program"
                v-model="formData.program"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">Select your program</option>
                <option value="Computer Science">Computer Science</option>
                <option value="Software Engineering">Software Engineering</option>
                <option value="Information Technology">Information Technology</option>
                <option value="Data Science">Data Science</option>
                <option value="Electrical Engineering">Electrical Engineering</option>
                <option value="Mechanical Engineering">Mechanical Engineering</option>
                <option value="Civil Engineering">Civil Engineering</option>
                <option value="Business Administration">Business Administration</option>
                <option value="Marketing">Marketing</option>
                <option value="Finance">Finance</option>
                <option value="Psychology">Psychology</option>
                <option value="Biology">Biology</option>
                <option value="Environmental Science">Environmental Science</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div v-if="formData.program === 'Other'">
              <label for="customProgram" class="block text-sm font-medium text-gray-700 mb-1">
                Specify Program <span class="text-red-500">*</span>
              </label>
              <input
                id="customProgram"
                v-model="formData.customProgram"
                type="text"
                required
                placeholder="Enter your program"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label for="academicYear" class="block text-sm font-medium text-gray-700 mb-1">
                Academic Year <span class="text-red-500">*</span>
              </label>
              <select
                id="academicYear"
                v-model="formData.academicYear"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">Select your year</option>
                <option value="Year 1">Year 1</option>
                <option value="Year 2">Year 2</option>
                <option value="Year 3">Year 3</option>
                <option value="Year 4">Year 4</option>
                <option value="Year 5+">Year 5+</option>
                <option value="Graduate">Graduate Student</option>
              </select>
            </div>
          </div>

          <!-- Step 2: Interests & Skills -->
          <div v-if="step === 2" class="space-y-4">
            <div>
              <label for="interests" class="block text-sm font-medium text-gray-700 mb-1">
                Areas of Interest <span class="text-gray-400">(Optional)</span>
              </label>
              <textarea
                id="interests"
                v-model="formData.interests"
                rows="3"
                placeholder="e.g., Artificial Intelligence, Web Development, Data Analytics"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Separate multiple interests with commas</p>
            </div>

            <div>
              <label for="skills" class="block text-sm font-medium text-gray-700 mb-1">
                Technical Skills <span class="text-gray-400">(Optional)</span>
              </label>
              <textarea
                id="skills"
                v-model="formData.skills"
                rows="3"
                placeholder="e.g., Python, JavaScript, Machine Learning, Database Design"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Separate multiple skills with commas</p>
            </div>

            <div>
              <label for="projectPreference" class="block text-sm font-medium text-gray-700 mb-1">
                Project Type Preference <span class="text-gray-400">(Optional)</span>
              </label>
              <select
                id="projectPreference"
                v-model="formData.projectPreference"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">Select preference</option>
                <option value="Research">Research-oriented</option>
                <option value="Development">Development/Implementation</option>
                <option value="Both">Both Research & Development</option>
                <option value="No Preference">No Preference</option>
              </select>
            </div>

            <div>
              <label for="expectedDuration" class="block text-sm font-medium text-gray-700 mb-1">
                Expected Project Duration <span class="text-gray-400">(Optional)</span>
              </label>
              <select
                id="expectedDuration"
                v-model="formData.expectedDuration"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              >
                <option value="">Select duration</option>
                <option value="3-4 months">3-4 months</option>
                <option value="4-6 months">4-6 months</option>
                <option value="6-8 months">6-8 months</option>
                <option value="8-12 months">8-12 months</option>
              </select>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-2">
            <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between pt-4 border-t">
            <button
              v-if="step === 2"
              type="button"
              @click="step = 1"
              class="px-6 py-3 text-gray-600 hover:text-gray-800 font-medium transition-colors"
            >
              ← Back
            </button>
            <div v-else></div>

            <div class="flex items-center space-x-3">
              <!-- <button
                type="button"
                @click="handleSkip"
                class="px-6 py-3 text-gray-500 hover:text-gray-700 font-medium transition-colors"
              >
                Skip for now
              </button> -->
              
              <button
                v-if="step === 1"
                type="button"
                @click="nextStep"
                :disabled="!isStep1Valid"
                class="px-6 py-3 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next →
              </button>

              <button
                v-else
                type="submit"
                :disabled="loading"
                class="px-6 py-3 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                <span>{{ loading ? 'Saving...' : 'Complete Profile' }}</span>
                <CheckCircle v-if="!loading" class="w-5 h-5" />
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { UserCog, CheckCircle, AlertCircle } from 'lucide-vue-next'
import authService from '../services/authService.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'completed'])

const step = ref(1)
const loading = ref(false)
const error = ref('')

const formData = ref({
  fullName: '',
  university: '',
  program: '',
  customProgram: '',
  academicYear: '',
  interests: '',
  skills: '',
  projectPreference: '',
  expectedDuration: ''
})

const isStep1Valid = computed(() => {
  const basicValid = formData.value.fullName && 
                     formData.value.university && 
                     formData.value.program && 
                     formData.value.academicYear
  
  if (formData.value.program === 'Other') {
    return basicValid && formData.value.customProgram
  }
  
  return basicValid
})

const nextStep = () => {
  if (isStep1Valid.value) {
    step.value = 2
  }
}

const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    // Check if user is authenticated
    const token = localStorage.getItem('auth_token')
    if (!token) {
      throw new Error('Authentication token not found. Please try logging in again.')
    }

    const profileData = {
      full_name: formData.value.fullName.trim(),
      university: formData.value.university.trim(),
      program: formData.value.program === 'Other' ? formData.value.customProgram.trim() : formData.value.program,
      academic_year: formData.value.academicYear,
      interests: formData.value.interests ? formData.value.interests.split(',').map(i => i.trim()).filter(i => i) : [],
      skills: formData.value.skills ? formData.value.skills.split(',').map(s => s.trim()).filter(s => s) : [],
      project_preference: formData.value.projectPreference || null,
      expected_duration: formData.value.expectedDuration || null
    }

    console.log('Saving profile data:', profileData)
    
    await authService.updateProfile(profileData)
    
    // Mark as completed
    await authService.completeOnboarding()
    
    emit('completed')
  } catch (err) {
    console.error('Profile completion error:', err)
    error.value = err.message || 'Failed to save profile. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleSkip = async () => {
  try {
    await authService.completeOnboarding()
    emit('completed', true) // true indicates skipped
  } catch (err) {
    console.error('Error skipping onboarding:', err)
    emit('completed', true)
  }
}

const handleClose = () => {
  // Don't allow closing without completing/skipping
  // Users must either complete or skip the profile
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

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.95);
}
</style>
