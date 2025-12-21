<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2 sm:p-4 overflow-y-auto" @click.self="closeModal">
    <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full max-h-[98vh] sm:max-h-[95vh] my-auto flex flex-col animate-fade-in">
      <!-- Header -->
      <div class="relative bg-primary-500 text-white p-4 sm:p-6 flex-shrink-0 rounded-t-3xl">
        <button @click="closeModal" class="absolute top-4 right-4 p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
          <X class="w-5 h-5" />
        </button>
        <div class="text-center">
          <div class="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
            <User class="w-8 h-8" />
          </div>
          <h2 class="text-2xl font-bold mb-1">
            {{ isLoginMode ? 'Welcome Back!' : 'Join Us Today!' }}
          </h2>
          <p class="text-white text-opacity-90">
            {{ isLoginMode ? 'Sign in to access your account' : 'Create your account to get started' }}
          </p>
        </div>
      </div>

      <!-- Form Content -->
      <div class="flex-1 overflow-y-auto p-4 sm:p-6">
        <!-- Mode Toggle -->
        <div class="flex bg-gray-100 rounded-xl p-1 mb-4 sm:mb-6">
          <button 
            @click="setMode(true)"
            :class="[
              'flex-1 py-3 px-4 rounded-lg text-sm font-semibold transition-all duration-300 transform',
              isLoginMode 
                ? 'bg-white text-gray-900 shadow-md scale-[1.02] border border-gray-200' 
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
            ]"
          >
            Sign In
          </button>
          <button 
            @click="setMode(false)"
            :class="[
              'flex-1 py-3 px-4 rounded-lg text-sm font-semibold transition-all duration-300 transform',
              !isLoginMode 
                ? 'bg-white text-gray-900 shadow-md scale-[1.02] border border-gray-200' 
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
            ]"
          >
            Sign Up
          </button>
        </div>

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

        <!-- Login Form -->
        <form v-if="isLoginMode" @submit.prevent="handleLogin" class="space-y-3 sm:space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="email"
                v-model="loginForm.email"
                type="email"
                required
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Enter your email"
                :disabled="loading"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full pl-10 pr-12 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Enter your password"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary-500 text-white py-2.5 px-4 rounded-xl font-semibold hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <span>{{ loading ? 'Signing In...' : 'Sign In' }}</span>
          </button>
        </form>

        <!-- Registration Form -->
        <form v-else @submit.prevent="handleRegister" class="space-y-3 sm:space-y-4">
          <div>
            <label for="reg-email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="reg-email"
                v-model="registerForm.email"
                type="email"
                required
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Enter your email"
                :disabled="loading"
              />
            </div>
          </div>

          <div>
            <label for="reg-password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="reg-password"
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                minlength="6"
                class="w-full pl-10 pr-12 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Create a password (min 6 characters)"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                id="confirm-password"
                v-model="registerForm.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 bg-gray-50 focus:bg-white"
                placeholder="Confirm your password"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Password Match Indicator -->
          <div v-if="registerForm.password && registerForm.confirmPassword" class="text-sm">
            <div v-if="passwordsMatch" class="text-green-600 flex items-center space-x-2 bg-green-50 px-3 py-2 rounded-lg border border-green-200">
              <CheckCircle class="w-4 h-4" />
              <span class="font-medium">Passwords match</span>
            </div>
            <div v-else class="text-red-600 flex items-center space-x-2 bg-red-50 px-3 py-2 rounded-lg border border-red-200">
              <AlertCircle class="w-4 h-4" />
              <span class="font-medium">Passwords do not match</span>
            </div>
          </div>

         

          <button
            type="submit"
            :disabled="loading || !canRegister"
            class="w-full bg-primary-500 text-white py-2.5 px-4 rounded-xl font-semibold hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <span>{{ loading ? 'Creating Account...' : 'Create Account' }}</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="my-4 sm:my-6 flex items-center">
          <div class="flex-1 border-t border-gray-300"></div>
          <span class="px-4 text-sm text-gray-500">or</span>
          <div class="flex-1 border-t border-gray-300"></div>
        </div>

        <!-- Social Login -->
        <div class="space-y-3">
          <button 
            @click="handleGoogleLogin" 
            :disabled="loading"
            class="w-full flex items-center justify-center space-x-2 py-2.5 px-4 border border-gray-300 rounded-xl hover:bg-gray-50 transition-all duration-200 font-medium shadow-sm hover:shadow-md transform hover:scale-[1.01] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285f4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34a853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#fbbc05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#ea4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span class="text-gray-700 font-medium">Continue with Google</span>
          </button>
        </div>

        <!-- Footer Text -->
        <div class="mt-4 sm:mt-6 text-center text-sm text-gray-600">
          <span v-if="isLoginMode">
            Don't have an account? 
            <button @click="setMode(false)" class="text-primary-600 hover:text-primary-700 font-medium">
              Sign up
            </button>
          </span>
          <span v-else>
            Already have an account? 
            <button @click="setMode(true)" class="text-primary-600 hover:text-primary-700 font-medium">
              Sign in
            </button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  X, User, Mail, Lock, Eye, EyeOff, Loader2, 
  AlertCircle, CheckCircle 
} from 'lucide-vue-next'
import authService from '../services/authService.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  initialMode: {
    type: String,
    default: 'login', // 'login' or 'register'
    validator: (value) => ['login', 'register'].includes(value)
  }
})

const emit = defineEmits(['close', 'success'])

// Form state
const isLoginMode = ref(props.initialMode === 'login')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')
const success = ref('')

// Form data
const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

// Computed properties
const passwordsMatch = computed(() => {
  return registerForm.value.password === registerForm.value.confirmPassword
})

const canRegister = computed(() => {
  return registerForm.value.email && 
         registerForm.value.password && 
         registerForm.value.confirmPassword &&
         passwordsMatch.value &&
         registerForm.value.password.length >= 6
})

// Methods
const setMode = (login) => {
  isLoginMode.value = login
  clearMessages()
  showPassword.value = false
}

const clearMessages = () => {
  error.value = ''
  success.value = ''
}

const closeModal = () => {
  emit('close')
  clearMessages()
  resetForms()
}

const resetForms = () => {
  loginForm.value = { email: '', password: '' }
  registerForm.value = { email: '', password: '', confirmPassword: '' }
  showPassword.value = false
}

const handleLogin = async () => {
  if (loading.value) return
  
  clearMessages()
  loading.value = true
  
  try {
    await authService.login(loginForm.value.email, loginForm.value.password)
    success.value = 'Successfully signed in!'
    
    setTimeout(() => {
      emit('success', 'login')
      closeModal()
    }, 1000)
    
  } catch (err) {
    error.value = err.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (loading.value || !canRegister.value) return
  
  clearMessages()
  loading.value = true
  
  try {
    await authService.register(registerForm.value.email, registerForm.value.password)
    
    // Log in the user automatically after registration
    await authService.login(registerForm.value.email, registerForm.value.password)
    
    success.value = 'Account created successfully!'
    
    setTimeout(() => {
      emit('success', 'register')
      closeModal()
    }, 1000)
    
  } catch (err) {
    error.value = err.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleGoogleLogin = () => {
  // Redirect to backend Google OAuth endpoint
  window.location.href = 'http://127.0.0.1:5000/api/auth/google/login'
}

// Keyboard handling
const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    closeModal()
  }
}

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
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Ensure the modal is properly sized on mobile */
@media (max-height: 600px) {
  .space-y-3 > * + * {
    margin-top: 0.5rem !important;
  }
}

/* Improve touch targets on mobile */
@media (max-width: 640px) {
  .modal-content {
    max-height: calc(100vh - 1rem);
  }
}
</style>