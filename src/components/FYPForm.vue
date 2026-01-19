<template>
  <div class="card max-w-4xl mx-auto">
    <div class="text-center mb-8">
      <h3 class="text-3xl font-bold text-gray-900 mb-4">Project Information</h3>
      <p class="text-gray-600">Tell us about your interests, skills, and requirements to get personalized project suggestions.</p>
      
      <!-- Auto-fill Notification -->
      <div v-if="isAuthenticated && profileDataLoaded" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg inline-flex items-center space-x-2">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-sm text-blue-700 font-medium">Form auto-filled from your profile</span>
        <button 
          type="button" 
          @click="clearForm" 
          class="text-xs text-blue-600 hover:text-blue-800 underline ml-2"
        >
          Clear
        </button>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-8">
      <!-- Personal Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div data-field="name">
          <label class="block text-sm font-medium text-gray-700 mb-2">Full Name <span class="text-red-500">*</span></label>
          <input
            v-model="formData.name"
            type="text"
            class="input-field"
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.name }"
            placeholder="Enter your full name"
            @blur="validateField('name')"
            required
          />
          <p v-if="showValidation && validationErrors.name" class="mt-1 text-sm text-red-600">{{ validationErrors.name }}</p>
        </div>
        <div data-field="studentId">
          <label class="block text-sm font-medium text-gray-700 mb-2">University/Institution <span class="text-red-500">*</span></label>
          <input
            v-model="formData.studentId"
            type="text"
            class="input-field"
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.studentId }"
            placeholder="e.g., Stanford University, MIT, Oxford"
            @blur="validateField('studentId')"
            required
          />
          <p v-if="showValidation && validationErrors.studentId" class="mt-1 text-sm text-red-600">{{ validationErrors.studentId }}</p>
        </div>
      </div>

      <!-- Academic Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div data-field="program">
          <label class="block text-sm font-medium text-gray-700 mb-2">Program/Degree <span class="text-red-500">*</span></label>
          <select 
            v-model="formData.program" 
            class="input-field" 
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.program }"
            @change="validateField('program')"
            required
          >
            <option value="">Select your program</option>
            <optgroup label="Technology & Computing">
              <option value="computer-science">Computer Science</option>
              <option value="software-engineering">Software Engineering</option>
              <option value="information-technology">Information Technology</option>
              <option value="data-science">Data Science</option>
              <option value="cybersecurity">Cybersecurity</option>
              <option value="computer-engineering">Computer Engineering</option>
            </optgroup>
            <optgroup label="Business & Management">
              <option value="business-administration">Business Administration</option>
              <option value="marketing">Marketing</option>
              <option value="finance">Finance</option>
              <option value="accounting">Accounting</option>
              <option value="economics">Economics</option>
              <option value="management">Management</option>
            </optgroup>
            <optgroup label="Engineering">
              <option value="mechanical-engineering">Mechanical Engineering</option>
              <option value="electrical-engineering">Electrical Engineering</option>
              <option value="civil-engineering">Civil Engineering</option>
              <option value="chemical-engineering">Chemical Engineering</option>
              <option value="biomedical-engineering">Biomedical Engineering</option>
            </optgroup>
            <optgroup label="Health & Life Sciences">
              <option value="medicine">Medicine</option>
              <option value="nursing">Nursing</option>
              <option value="pharmacy">Pharmacy</option>
              <option value="biology">Biology</option>
              <option value="biochemistry">Biochemistry</option>
              <option value="psychology">Psychology</option>
            </optgroup>
            <optgroup label="Arts & Humanities">
              <option value="english-literature">English Literature</option>
              <option value="history">History</option>
              <option value="philosophy">Philosophy</option>
              <option value="art-design">Art & Design</option>
              <option value="communication">Communication</option>
              <option value="journalism">Journalism</option>
            </optgroup>
            <optgroup label="Social Sciences">
              <option value="sociology">Sociology</option>
              <option value="political-science">Political Science</option>
              <option value="international-relations">International Relations</option>
              <option value="education">Education</option>
              <option value="social-work">Social Work</option>
            </optgroup>
            <optgroup label="Natural Sciences">
              <option value="physics">Physics</option>
              <option value="chemistry">Chemistry</option>
              <option value="mathematics">Mathematics</option>
              <option value="environmental-science">Environmental Science</option>
              <option value="geology">Geology</option>
            </optgroup>
            <option value="other">Other</option>
          </select>
          <p v-if="showValidation && validationErrors.program" class="mt-1 text-sm text-red-600">{{ validationErrors.program }}</p>
        </div>
        <div data-field="academicYear">
          <label class="block text-sm font-medium text-gray-700 mb-2">Academic Year <span class="text-red-500">*</span></label>
          <select 
            v-model="formData.academicYear" 
            class="input-field" 
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.academicYear }"
            @change="validateField('academicYear')"
            required
          >
            <option value="">Select academic year</option>
            <option value="Year 1">Year 1</option>
            <option value="Year 2">Year 2</option>
            <option value="Year 3">Year 3</option>
            <option value="Year 4">Year 4</option>
            <option value="Year 5+">Year 5+</option>
            <option value="Graduate">Graduate Student</option>
          </select>
          <p v-if="showValidation && validationErrors.academicYear" class="mt-1 text-sm text-red-600">{{ validationErrors.academicYear }}</p>
        </div>
      </div>

      <!-- Skills & Knowledge -->
      <div data-field="skillsText">
        <label class="block text-sm font-medium text-gray-700 mb-2">Skills & Knowledge Areas <span class="text-red-500">*</span></label>
        <p class="text-sm text-gray-600 mb-3">Enter keywords related to your skills, technologies, or areas of expertise (e.g., "Python programming", "Data analysis", "Marketing", "Graphic design", "Research methods")</p>
        <textarea
          v-model="formData.skillsText"
          class="input-field h-24 resize-none"
          :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.skillsText }"
          placeholder="Enter your skills and knowledge areas separated by commas or new lines..."
          @blur="validateField('skillsText')"
          required
        ></textarea>
        <p v-if="showValidation && validationErrors.skillsText" class="mt-1 text-sm text-red-600">{{ validationErrors.skillsText }}</p>
        <div v-else class="mt-2 text-xs text-gray-500">
          <strong>Examples:</strong> Web development, Machine learning, Business analysis, Digital marketing, Statistical analysis, Creative writing, Laboratory techniques, Financial modeling, etc.
        </div>
      </div>

      <!-- Areas of Interest -->
      <div data-field="interestsText">
        <label class="block text-sm font-medium text-gray-700 mb-2">Areas of Interest & Research Topics <span class="text-red-500">*</span></label>
        <p class="text-sm text-gray-600 mb-3">Enter keywords related to topics, fields, or subjects that interest you (e.g., "Artificial Intelligence", "Sustainable energy", "Healthcare technology", "Social media", "Environmental science")</p>
        <textarea
          v-model="formData.interestsText"
          class="input-field h-24 resize-none"
          :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.interestsText }"
          placeholder="Enter your areas of interest separated by commas or new lines..."
          @blur="validateField('interestsText')"
          required
        ></textarea>
        <p v-if="showValidation && validationErrors.interestsText" class="mt-1 text-sm text-red-600">{{ validationErrors.interestsText }}</p>
        <div v-else class="mt-2 text-xs text-gray-500">
          <strong>Examples:</strong> Climate change, Human psychology, E-commerce, Renewable energy, Education technology, Urban planning, Biotechnology, Digital transformation, etc.
        </div>
      </div>

      <!-- Project Preferences -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div data-field="difficulty">
          <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Difficulty Level <span class="text-red-500">*</span></label>
          <select 
            v-model="formData.difficulty" 
            class="input-field" 
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.difficulty }"
            @change="validateField('difficulty')"
            required
          >
            <option value="">Select difficulty</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <p v-if="showValidation && validationErrors.difficulty" class="mt-1 text-sm text-red-600">{{ validationErrors.difficulty }}</p>
        </div>
        <div data-field="duration">
          <label class="block text-sm font-medium text-gray-700 mb-2">Project Duration <span class="text-red-500">*</span></label>
          <select 
            v-model="formData.duration" 
            class="input-field" 
            :class="{ 'border-red-500 focus:ring-red-500 focus:border-red-500': showValidation && validationErrors.duration }"
            @change="validateField('duration')"
            required
          >
            <option value="">Select duration</option>
            <option value="3-4">3-4 months</option>
            <option value="4-6">4-6 months</option>
            <option value="6-8">6-8 months</option>
            <option value="8-12">8-12 months</option>
          </select>
          <p v-if="showValidation && validationErrors.duration" class="mt-1 text-sm text-red-600">{{ validationErrors.duration }}</p>
        </div>
      </div>

      <!-- Project Type -->
      <div data-field="projectType">
        <label class="block text-sm font-medium text-gray-700 mb-3">Project Type Preference <span class="text-red-500">*</span></label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label 
            v-for="type in projectTypes" 
            :key="type.value" 
            class="flex items-center space-x-3 p-4 border rounded-lg cursor-pointer hover:border-primary-300 transition-colors"
            :class="showValidation && validationErrors.projectType ? 'border-red-500' : 'border-gray-200'"
          >
            <input
              type="radio"
              :value="type.value"
              v-model="formData.projectType"
              class="w-4 h-4 text-primary-600 border-gray-300 focus:ring-primary-500"
              @change="validateField('projectType')"
            />
            <div>
              <div class="font-medium text-gray-900">{{ type.label }}</div>
              <div class="text-sm text-gray-600">{{ type.description }}</div>
            </div>
          </label>
        </div>
        <p v-if="showValidation && validationErrors.projectType" class="mt-2 text-sm text-red-600">{{ validationErrors.projectType }}</p>
      </div>

      <!-- Additional Requirements -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Additional Requirements or Constraints</label>
        <textarea
          v-model="formData.additionalRequirements"
          class="input-field h-32 resize-none"
          placeholder="Any specific requirements, constraints, or preferences for your project..."
        ></textarea>
      </div>

      <!-- Supervisor Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Supervisor (Optional)</label>
          <input
            v-model="formData.supervisor"
            type="text"
            class="input-field"
            placeholder="Enter supervisor name or leave blank"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Budget Range (Optional)</label>
          <select v-model="formData.budget" class="input-field">
            <option value="">Select budget range</option>
            <option value="0-500">$0 - $500</option>
            <option value="500-1000">$500 - $1,000</option>
            <option value="1000-2000">$1,000 - $2,000</option>
            <option value="2000+">$2,000+</option>
          </select>
        </div>
      </div>

      <!-- Submit Button -->
      <div class="text-center pt-6">
        <button

          type="submit"
          :disabled="isSubmitting"
          class="btn-primary text-lg px-12 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Loader2 v-if="isSubmitting" class="w-5 h-5 inline mr-2 animate-spin" />
          <Sparkles v-else class="w-5 h-5 inline mr-2" />
          {{ isSubmitting ? 'Generating Topics...' : 'Generate FYP Topics' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { Sparkles, Loader2 } from 'lucide-vue-next'
import { currentUser, isAuthenticated } from '../services/authService.js'

const emit = defineEmits(['generate-topics'])
const isSubmitting = ref(false)
const profileDataLoaded = ref(false)
const showValidation = ref(false)

const formData = reactive({
  name: '',
  studentId: '',
  program: '',
  academicYear: '',
  skillsText: '',
  interestsText: '',
  difficulty: '',
  duration: '',
  projectType: '',
  additionalRequirements: '',
  supervisor: '',
  budget: ''
})

const validationErrors = reactive({
  name: '',
  studentId: '',
  program: '',
  academicYear: '',
  skillsText: '',
  interestsText: '',
  difficulty: '',
  duration: '',
  projectType: ''
})

// Store original empty state
const emptyFormData = {
  name: '',
  studentId: '',
  program: '',
  academicYear: '',
  skillsText: '',
  interestsText: '',
  difficulty: '',
  duration: '',
  projectType: '',
  additionalRequirements: '',
  supervisor: '',
  budget: ''
}

// Clear form back to empty state
const clearForm = () => {
  Object.assign(formData, emptyFormData)
  profileDataLoaded.value = false
  showValidation.value = false
  // Clear validation errors
  Object.keys(validationErrors).forEach(key => {
    validationErrors[key] = ''
  })
}

// Validate individual field
const validateField = (field) => {
  if (!showValidation.value) return
  
  switch(field) {
    case 'name':
      validationErrors.name = !formData.name.trim() ? 'Please enter your full name' : ''
      break
    case 'studentId':
      validationErrors.studentId = !formData.studentId.trim() ? 'Please enter your university/institution' : ''
      break
    case 'program':
      validationErrors.program = !formData.program ? 'Please select your program/degree' : ''
      break
    case 'academicYear':
      validationErrors.academicYear = !formData.academicYear ? 'Please select your academic year' : ''
      break
    case 'skillsText':
      validationErrors.skillsText = !formData.skillsText.trim() ? 'Please enter at least one skill or knowledge area' : ''
      break
    case 'interestsText':
      validationErrors.interestsText = !formData.interestsText.trim() ? 'Please enter at least one area of interest' : ''
      break
    case 'difficulty':
      validationErrors.difficulty = !formData.difficulty ? 'Please select a difficulty level' : ''
      break
    case 'duration':
      validationErrors.duration = !formData.duration ? 'Please select a project duration' : ''
      break
    case 'projectType':
      validationErrors.projectType = !formData.projectType ? 'Please select a project type preference' : ''
      break
  }
}

// Validate all fields
const validateAllFields = () => {
  showValidation.value = true
  const fields = ['name', 'studentId', 'program', 'academicYear', 'skillsText', 'interestsText', 'difficulty', 'duration', 'projectType']
  fields.forEach(field => validateField(field))
  
  // Check if there are any errors
  return !Object.values(validationErrors).some(error => error !== '')
}

// Auto-populate form from user profile
const populateFromProfile = () => {
  if (!isAuthenticated.value || !currentUser.value) {
    profileDataLoaded.value = false
    return
  }
  
  const user = currentUser.value
  let hasData = false
  
  // Populate basic information
  if (user.full_name) {
    formData.name = user.full_name
    hasData = true
  }
  
  if (user.university) {
    formData.studentId = user.university
    hasData = true
  }
  
  // Map program from profile to form dropdown value
  if (user.program) {
    // Convert stored program to kebab-case for dropdown
    const programValue = user.program.toLowerCase().replace(/\s+/g, '-')
    formData.program = programValue
    hasData = true
  }
  
  if (user.academic_year) {
    // Use academic_year directly (Year 1, Year 2, etc.)
    formData.academicYear = user.academic_year
    hasData = true
  }
  
  // Populate skills from profile
  if (user.skills && Array.isArray(user.skills) && user.skills.length > 0) {
    formData.skillsText = user.skills.join(', ')
    hasData = true
  }
  
  // Populate interests from profile
  if (user.interests && Array.isArray(user.interests) && user.interests.length > 0) {
    formData.interestsText = user.interests.join(', ')
    hasData = true
  }
  
  // Populate project preference
  if (user.project_preference) {
    const preferenceMap = {
      'Research': 'research',
      'Development': 'application',
      'Both': 'innovation',
      'No Preference': ''
    }
    formData.projectType = preferenceMap[user.project_preference] || ''
    if (formData.projectType) hasData = true
  }
  
  // Populate expected duration
  if (user.expected_duration) {
    const durationMap = {
      '3-4 months': '3-4',
      '4-6 months': '4-6',
      '6-8 months': '6-8',
      '8-12 months': '8-12'
    }
    formData.duration = durationMap[user.expected_duration] || ''
    if (formData.duration) hasData = true
  }
  
  // Set flag if any data was populated
  profileDataLoaded.value = hasData
}

// Populate form when component mounts
onMounted(() => {
  populateFromProfile()
})

// Watch for user changes (e.g., after login or profile update)
watch([isAuthenticated, currentUser], () => {
  populateFromProfile()
}, { deep: true })

const projectTypes = [
  {
    value: 'research',
    label: 'Research Project',
    description: 'Focus on academic research and contribution to knowledge'
  },
  {
    value: 'application',
    label: 'Application Development',
    description: 'Build a practical software application or system'
  },
  {
    value: 'analysis',
    label: 'Analysis & Study',
    description: 'Analyze existing systems or conduct comparative studies'
  },
  {
    value: 'innovation',
    label: 'Innovation Project',
    description: 'Create something new or improve existing solutions'
  }
]

const handleSubmit = async () => {
  // Validate all fields
  const isValid = validateAllFields()
  
  if (!isValid) {
    // Scroll to first error
    const firstErrorField = Object.keys(validationErrors).find(key => validationErrors[key] !== '')
    if (firstErrorField) {
      const element = document.querySelector(`[data-field="${firstErrorField}"]`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
    return
  }
  
  isSubmitting.value = true

  // Emit the form data
  emit('generate-topics', { ...formData })
  
  // Reset submitting state after a delay
  setTimeout(() => {
    isSubmitting.value = false
  }, 2000)
}
</script>
