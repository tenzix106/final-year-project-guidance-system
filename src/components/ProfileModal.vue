<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto" @click.self="closeModal">
    <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[95vh] my-auto flex flex-col animate-fade-in">
      <!-- Header -->
      <div class="relative bg-primary-500 text-white p-6 flex-shrink-0 rounded-t-3xl">
        <button @click="closeModal" class="absolute top-4 right-4 p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
          <X class="w-5 h-5" />
        </button>
        <div class="text-center">
          <div class="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
            <UserCircle class="w-8 h-8" />
          </div>
          <h2 class="text-2xl font-bold mb-1">My Profile</h2>
          <p class="text-white text-opacity-90">Update your personal information</p>
        </div>
      </div>

      <!-- Form Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- Error Message -->
        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
          <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0" />
          <span class="text-red-700 text-sm">{{ error }}</span>
        </div>

        <!-- Success Message -->
        <div v-if="success" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-2">
          <CheckCircle class="w-5 h-5 text-green-500 flex-shrink-0" />
          <span class="text-green-700 text-sm">{{ success }}</span>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Email (Read-only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                :value="currentUser?.email"
                type="email"
                disabled
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl bg-gray-100 text-gray-500 cursor-not-allowed"
              />
            </div>
            <p class="text-xs text-gray-500 mt-1">Email cannot be changed</p>
          </div>

          <!-- Full Name -->
          <div>
            <label for="fullName" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="fullName"
                v-model="formData.full_name"
                type="text"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Enter your full name"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- University/Institution -->
          <div>
            <label for="university" class="block text-sm font-medium text-gray-700 mb-1">University/Institution</label>
            <div class="relative">
              <Hash class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="university"
                v-model="formData.university"
                type="text"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="e.g., Stanford University, MIT, Oxford"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Program -->
          <div>
            <label for="program" class="block text-sm font-medium text-gray-700 mb-1">Program/Major</label>
            <div class="relative">
              <GraduationCap class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <select
                id="program"
                v-model="formData.program"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white appearance-none"
                :disabled="loading"
              >
                <option value="">Select your program</option>
                <option value="computer-science">Computer Science</option>
                <option value="software-engineering">Software Engineering</option>
                <option value="information-technology">Information Technology</option>
                <option value="data-science">Data Science</option>
                <option value="cybersecurity">Cybersecurity</option>
                <option value="business-administration">Business Administration</option>
                <option value="marketing">Marketing</option>
                <option value="finance">Finance</option>
                <option value="engineering">Engineering</option>
                <option value="mechanical-engineering">Mechanical Engineering</option>
                <option value="electrical-engineering">Electrical Engineering</option>
                <option value="civil-engineering">Civil Engineering</option>
                <option value="medicine">Medicine</option>
                <option value="nursing">Nursing</option>
                <option value="pharmacy">Pharmacy</option>
                <option value="psychology">Psychology</option>
                <option value="education">Education</option>
                <option value="environmental-science">Environmental Science</option>
                <option value="other">Other</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          <!-- Academic Year -->
          <div>
            <label for="academicYear" class="block text-sm font-medium text-gray-700 mb-1">Academic Year</label>
            <div class="relative">
              <Calendar class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <select
                id="academicYear"
                v-model="formData.academic_year"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white appearance-none"
                :disabled="loading"
              >
                <option value="">Select year</option>
                <option value="Year 1">Year 1</option>
                <option value="Year 2">Year 2</option>
                <option value="Year 3">Year 3</option>
                <option value="Year 4">Year 4</option>
                <option value="Year 5+">Year 5+</option>
                <option value="Graduate">Graduate Student</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-200 my-6"></div>
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Academic Interests & Skills</h3>

          <!-- Areas of Interest -->
          <div>
            <label for="interests" class="block text-sm font-medium text-gray-700 mb-1">Areas of Interest</label>
            <textarea
              id="interests"
              v-model="formData.interests"
              rows="3"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white resize-none"
              placeholder="e.g., Artificial Intelligence, Web Development, Data Analytics"
              :disabled="loading"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">Separate multiple interests with commas</p>
          </div>

          <!-- Technical Skills -->
          <div>
            <label for="skills" class="block text-sm font-medium text-gray-700 mb-1">Technical Skills</label>
            <textarea
              id="skills"
              v-model="formData.skills"
              rows="3"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white resize-none"
              placeholder="e.g., Python, JavaScript, Machine Learning, Database Design"
              :disabled="loading"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">Separate multiple skills with commas</p>
          </div>

          <!-- Project Preference -->
          <div>
            <label for="projectPreference" class="block text-sm font-medium text-gray-700 mb-1">Project Type Preference</label>
            <div class="relative">
              <select
                id="projectPreference"
                v-model="formData.project_preference"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white appearance-none"
                :disabled="loading"
              >
                <option value="">Select preference</option>
                <option value="Research">Research-oriented</option>
                <option value="Development">Development/Implementation</option>
                <option value="Both">Both Research & Development</option>
                <option value="No Preference">No Preference</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          <!-- Expected Duration -->
          <div>
            <label for="expectedDuration" class="block text-sm font-medium text-gray-700 mb-1">Expected Project Duration</label>
            <div class="relative">
              <select
                id="expectedDuration"
                v-model="formData.expected_duration"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white appearance-none"
                :disabled="loading"
              >
                <option value="">Select duration</option>
                <option value="3-4 months">3-4 months</option>
                <option value="4-6 months">4-6 months</option>
                <option value="6-8 months">6-8 months</option>
                <option value="8-12 months">8-12 months</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            </div>
          </div>

          <!-- Auth Provider Info -->
          <div class="mt-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
            <div class="flex items-center space-x-2 text-sm text-gray-600">
              <Info class="w-4 h-4" />
              <span>
                Signed in with: 
                <span class="font-semibold text-gray-900">
                  {{ currentUser?.auth_provider === 'google' ? 'Google' : 'Email' }}
                </span>
              </span>
            </div>
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="bg-gray-50 px-6 py-4 flex items-center justify-between border-t border-gray-200 flex-shrink-0 rounded-b-3xl">
        <button
          @click="closeModal"
          type="button"
          class="px-6 py-2.5 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-xl transition-colors font-medium"
          :disabled="loading"
        >
          Cancel
        </button>

        <button
          @click="handleSubmit"
          :disabled="loading || !hasChanges"
          class="flex items-center space-x-2 px-6 py-2.5 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
          <Save v-else class="w-5 h-5" />
          <span>{{ loading ? 'Saving...' : 'Save Changes' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { 
  X, UserCircle, Mail, User, Hash, GraduationCap, Calendar, 
  ChevronDown, AlertCircle, CheckCircle, Loader2, Save, Info 
} from 'lucide-vue-next'
import authService, { currentUser } from '../services/authService.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'updated'])

const loading = ref(false)
const error = ref('')
const success = ref('')

const formData = ref({
  full_name: '',
  university: '',
  program: '',
  academic_year: '',
  interests: '',
  skills: '',
  project_preference: '',
  expected_duration: ''
})

const originalData = ref({})

// Initialize form with current user data
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && currentUser.value) {
    formData.value = {
      full_name: currentUser.value.full_name || '',
      university: currentUser.value.university || '',
      program: currentUser.value.program || '',
      academic_year: currentUser.value.academic_year || '',
      interests: currentUser.value.interests ? currentUser.value.interests.join(', ') : '',
      skills: currentUser.value.skills ? currentUser.value.skills.join(', ') : '',
      project_preference: currentUser.value.project_preference || '',
      expected_duration: currentUser.value.expected_duration || ''
    }
    originalData.value = { ...formData.value }
    clearMessages()
  }
})

const hasChanges = computed(() => {
  return JSON.stringify(formData.value) !== JSON.stringify(originalData.value)
})

const clearMessages = () => {
  error.value = ''
  success.value = ''
}

const closeModal = () => {
  if (!loading.value) {
    emit('close')
    clearMessages()
  }
}

const handleSubmit = async () => {
  if (loading.value || !hasChanges.value) return
  
  clearMessages()
  loading.value = true
  
  try {
    // Prepare data - convert comma-separated strings to arrays for interests and skills
    const profileData = {
      full_name: formData.value.full_name,
      university: formData.value.university,
      program: formData.value.program,
      academic_year: formData.value.academic_year,
      interests: formData.value.interests ? formData.value.interests.split(',').map(i => i.trim()).filter(i => i) : [],
      skills: formData.value.skills ? formData.value.skills.split(',').map(s => s.trim()).filter(s => s) : [],
      project_preference: formData.value.project_preference || null,
      expected_duration: formData.value.expected_duration || null
    }
    
    await authService.updateProfile(profileData)
    success.value = 'Profile updated successfully!'
    originalData.value = { ...formData.value }
    
    setTimeout(() => {
      emit('updated')
      closeModal()
    }, 1500)
    
  } catch (err) {
    error.value = err.message || 'Failed to update profile. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
