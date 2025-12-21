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
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
          <input
            v-model="formData.name"
            type="text"
            class="input-field"
            placeholder="Enter your full name"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">University/Institution</label>
          <input
            v-model="formData.studentId"
            type="text"
            class="input-field"
            placeholder="e.g., Stanford University, MIT, Oxford"
            required
          />
        </div>
      </div>

      <!-- Academic Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Program/Degree</label>
          <select v-model="formData.program" class="input-field" required>
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
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Academic Year</label>
          <select v-model="formData.academicYear" class="input-field" required>
            <option value="">Select academic year</option>
            <option value="2024">2024</option>
            <option value="2025">2025</option>
            <option value="2026">2026</option>
          </select>
        </div>
      </div>

      <!-- Skills & Knowledge -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Skills & Knowledge Areas</label>
        <p class="text-sm text-gray-600 mb-3">Enter keywords related to your skills, technologies, or areas of expertise (e.g., "Python programming", "Data analysis", "Marketing", "Graphic design", "Research methods")</p>
        <textarea
          v-model="formData.skillsText"
          class="input-field h-24 resize-none"
          placeholder="Enter your skills and knowledge areas separated by commas or new lines..."
          required
        ></textarea>
        <div class="mt-2 text-xs text-gray-500">
          <strong>Examples:</strong> Web development, Machine learning, Business analysis, Digital marketing, Statistical analysis, Creative writing, Laboratory techniques, Financial modeling, etc.
        </div>
      </div>

      <!-- Areas of Interest -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Areas of Interest & Research Topics</label>
        <p class="text-sm text-gray-600 mb-3">Enter keywords related to topics, fields, or subjects that interest you (e.g., "Artificial Intelligence", "Sustainable energy", "Healthcare technology", "Social media", "Environmental science")</p>
        <textarea
          v-model="formData.interestsText"
          class="input-field h-24 resize-none"
          placeholder="Enter your areas of interest separated by commas or new lines..."
          required
        ></textarea>
        <div class="mt-2 text-xs text-gray-500">
          <strong>Examples:</strong> Climate change, Human psychology, E-commerce, Renewable energy, Education technology, Urban planning, Biotechnology, Digital transformation, etc.
        </div>
      </div>

      <!-- Project Preferences -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Preferred Difficulty Level</label>
          <select v-model="formData.difficulty" class="input-field" required>
            <option value="">Select difficulty</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Project Duration</label>
          <select v-model="formData.duration" class="input-field" required>
            <option value="">Select duration</option>
            <option value="3-4">3-4 months</option>
            <option value="4-6">4-6 months</option>
            <option value="6-8">6-8 months</option>
            <option value="8-12">8-12 months</option>
          </select>
        </div>
      </div>

      <!-- Project Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-3">Project Type Preference</label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label v-for="type in projectTypes" :key="type.value" class="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-colors">
            <input
              type="radio"
              :value="type.value"
              v-model="formData.projectType"
              class="w-4 h-4 text-primary-600 border-gray-300 focus:ring-primary-500"
            />
            <div>
              <div class="font-medium text-gray-900">{{ type.label }}</div>
              <div class="text-sm text-gray-600">{{ type.description }}</div>
            </div>
          </label>
        </div>
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
    // Extract year number from formats like "Year 3" or "2024"
    const yearMatch = user.academic_year.match(/\d{4}/)
    if (yearMatch) {
      formData.academicYear = yearMatch[0]
      hasData = true
    }
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
  isSubmitting.value = true
  
  // Validate required fields
  if (!formData.name || !formData.studentId || !formData.program || 
      !formData.academicYear || !formData.difficulty || !formData.duration || 
      !formData.projectType) {
    alert('Please fill in all required fields')
    isSubmitting.value = false
    return
  }

  if (!formData.skillsText.trim() || !formData.interestsText.trim()) {
    alert('Please enter your skills and areas of interest')
    isSubmitting.value = false
    return
  }

  // Emit the form data
  emit('generate-topics', { ...formData })
  
  // Reset submitting state after a delay
  setTimeout(() => {
    isSubmitting.value = false
  }, 2000)
}
</script>
