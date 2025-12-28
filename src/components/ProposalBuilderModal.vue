<template>
  <transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4" @click.self="handleClose">
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 p-6 rounded-t-2xl sticky top-0 z-10">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-white">Project Proposal Builder</h2>
              <p class="text-primary-100 mt-1">AI-powered proposal generator for your FYP</p>
            </div>
            <button @click="handleClose" class="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
              <X class="w-6 h-6 text-white" />
            </button>
          </div>

          <!-- Progress Indicator -->
          <div class="flex items-center justify-between mt-6">
            <div class="flex items-center space-x-2 flex-1">
              <div v-for="stepNum in 6" :key="stepNum" class="flex items-center">
                <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-all', 
                  step >= stepNum ? 'bg-white text-primary-600' : 'bg-white bg-opacity-20 text-white']">
                  {{ stepNum }}
                </div>
                <div v-if="stepNum < 6" class="w-8 md:w-16 h-1 bg-white bg-opacity-20 mx-1">
                  <div :class="['h-full bg-white transition-all duration-300']" 
                       :style="{ width: step > stepNum ? '100%' : '0%' }"></div>
                </div>
              </div>
            </div>
            <span class="text-sm text-white ml-4">Step {{ step }} of 6</span>
          </div>
        </div>

        <!-- Success Message -->
        <transition name="fade">
          <div v-if="success" class="mx-6 mt-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-3 shadow-sm">
            <CheckCircle class="w-5 h-5 text-green-600 flex-shrink-0" />
            <span class="text-green-800 text-sm font-medium flex-1">{{ success }}</span>
            <button @click="success = ''" class="text-green-600 hover:text-green-800 transition-colors">
              <X class="w-4 h-4" />
            </button>
          </div>
        </transition>

        <!-- Form Content -->
        <form @submit.prevent="handleNext" class="p-6 space-y-6">
          <!-- Step 1: Project Basics -->
          <div v-if="step === 1" class="space-y-4 animate-fade-in">
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Project Information</h3>
            
            <!-- Load from Favourites -->
            <div v-if="userFavourites.length > 0" class="bg-primary-50 border border-primary-200 rounded-lg p-4">
              <div class="flex items-start space-x-3">
                <Heart class="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
                <div class="flex-1">
                  <label for="favourite-select" class="block text-sm font-medium text-gray-900 mb-2">
                    Start from a Saved Favourite
                  </label>
                  <select
                    id="favourite-select"
                    v-model="selectedFavouriteId"
                    @change="handleFavouriteSelection"
                    class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all bg-white"
                  >
                    <option value="">Choose a favourite project...</option>
                    <option v-for="fav in userFavourites" :key="fav.id" :value="fav.id">
                      {{ fav.custom_title || fav.project_topic?.title || 'Untitled Project' }}
                    </option>
                  </select>
                  <p class="text-xs text-gray-600 mt-1.5">Select a saved project to auto-fill the fields below</p>
                </div>
              </div>
            </div>
            
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
                Project Title <span class="text-red-500">*</span>
              </label>
              <input
                id="title"
                v-model="formData.title"
                type="text"
                required
                placeholder="e.g., AI-Powered Student Performance Prediction System"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
                Brief Description <span class="text-red-500">*</span>
              </label>
              <textarea
                id="description"
                v-model="formData.description"
                rows="4"
                required
                placeholder="Describe what your project aims to achieve, the problem it solves, and its key features..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Provide a clear overview of your project idea</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="domain" class="block text-sm font-medium text-gray-700 mb-1">
                  Domain/Field <span class="text-red-500">*</span>
                </label>
                <select
                  id="domain"
                  v-model="formData.domain"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                >
                  <option value="">Select domain</option>
                  <option value="Web Development">Web Development</option>
                  <option value="Mobile Development">Mobile Development</option>
                  <option value="Artificial Intelligence">Artificial Intelligence</option>
                  <option value="Machine Learning">Machine Learning</option>
                  <option value="Data Science">Data Science</option>
                  <option value="Cybersecurity">Cybersecurity</option>
                  <option value="Internet of Things">Internet of Things</option>
                  <option value="Cloud Computing">Cloud Computing</option>
                  <option value="Business Analytics">Business Analytics</option>
                  <option value="E-Commerce">E-Commerce</option>
                  <option value="Healthcare Technology">Healthcare Technology</option>
                  <option value="Educational Technology">Educational Technology</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label for="program" class="block text-sm font-medium text-gray-700 mb-1">
                  Your Program <span class="text-red-500">*</span>
                </label>
                <input
                  id="program"
                  v-model="formData.program"
                  type="text"
                  required
                  placeholder="e.g., Computer Science"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div>
              <label for="technologies" class="block text-sm font-medium text-gray-700 mb-1">
                Technologies/Tools <span class="text-red-500">*</span>
              </label>
              <input
                id="technologies"
                v-model="formData.technologies"
                type="text"
                required
                placeholder="e.g., Python, TensorFlow, React, PostgreSQL"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
              <p class="text-xs text-gray-500 mt-1">List the main technologies you plan to use</p>
            </div>

            <div>
              <label for="supervisor" class="block text-sm font-medium text-gray-700 mb-1">
                Supervisor Name <span class="text-gray-400">(Optional)</span>
              </label>
              <input
                id="supervisor"
                v-model="formData.supervisor"
                type="text"
                placeholder="e.g., Dr. John Smith"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Step 2: Background -->
          <div v-if="step === 2" class="space-y-4 animate-fade-in">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-900">Background & Motivation</h3>
              <button
                v-if="!generatedSections.background && !generating.background"
                @click.prevent="generateSection('background')"
                type="button"
                class="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                <Sparkles class="w-4 h-4" />
                <span>Generate with AI</span>
              </button>
              <div v-if="generating.background" class="flex items-center space-x-2 text-primary-600">
                <Loader2 class="w-5 h-5 animate-spin" />
                <span class="text-sm">Generating...</span>
              </div>
            </div>

            <div>
              <label for="background" class="block text-sm font-medium text-gray-700 mb-1">
                Background Section
              </label>
              <textarea
                id="background"
                v-model="generatedSections.background"
                rows="8"
                placeholder="Click 'Generate with AI' or write your own background section explaining the context, significance, and challenges..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Explain the context, current challenges, and why this project is needed (150-200 words)</p>
            </div>
          </div>

          <!-- Step 3: Objectives -->
          <div v-if="step === 3" class="space-y-4 animate-fade-in">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-900">Project Objectives</h3>
              <button
                v-if="!generatedSections.objectives && !generating.objectives"
                @click.prevent="generateSection('objectives')"
                type="button"
                class="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                <Sparkles class="w-4 h-4" />
                <span>Generate with AI</span>
              </button>
              <div v-if="generating.objectives" class="flex items-center space-x-2 text-primary-600">
                <Loader2 class="w-5 h-5 animate-spin" />
                <span class="text-sm">Generating...</span>
              </div>
            </div>

            <div class="space-y-3">
              <div v-for="(objective, index) in objectives" :key="index" class="flex items-start space-x-2">
                <span class="text-sm font-medium text-gray-600 mt-3">{{ index + 1 }}.</span>
                <input
                  v-model="objectives[index]"
                  type="text"
                  placeholder="Enter project objective..."
                  class="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
                <button
                  v-if="objectives.length > 1"
                  @click.prevent="removeObjective(index)"
                  type="button"
                  class="p-2.5 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <Trash2 class="w-5 h-5" />
                </button>
              </div>
            </div>

            <button
              @click.prevent="addObjective"
              type="button"
              class="flex items-center space-x-2 px-4 py-2 border-2 border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-primary-500 hover:text-primary-600 transition-colors w-full justify-center"
            >
              <Plus class="w-4 h-4" />
              <span>Add Another Objective</span>
            </button>
          </div>

          <!-- Step 4: Scope -->
          <div v-if="step === 4" class="space-y-4 animate-fade-in">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-900">Project Scope</h3>
              <button
                v-if="!generatedSections.scope && !generating.scope"
                @click.prevent="generateSection('scope')"
                type="button"
                class="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                <Sparkles class="w-4 h-4" />
                <span>Generate with AI</span>
              </button>
              <div v-if="generating.scope" class="flex items-center space-x-2 text-primary-600">
                <Loader2 class="w-5 h-5 animate-spin" />
                <span class="text-sm">Generating...</span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- In Scope -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <Check class="w-5 h-5 text-green-600 mr-2" />
                  In Scope
                </h4>
                <div class="space-y-2">
                  <div v-for="(item, index) in scope.inScope" :key="index" class="flex items-start space-x-2">
                    <input
                      v-model="scope.inScope[index]"
                      type="text"
                      placeholder="What will be included..."
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                    />
                    <button
                      v-if="scope.inScope.length > 1"
                      @click.prevent="scope.inScope.splice(index, 1)"
                      type="button"
                      class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <X class="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <button
                  @click.prevent="scope.inScope.push('')"
                  type="button"
                  class="mt-2 flex items-center space-x-1 px-3 py-1.5 text-sm border border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-green-500 hover:text-green-600 transition-colors"
                >
                  <Plus class="w-3 h-3" />
                  <span>Add Item</span>
                </button>
              </div>

              <!-- Out of Scope -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-3 flex items-center">
                  <X class="w-5 h-5 text-red-600 mr-2" />
                  Out of Scope
                </h4>
                <div class="space-y-2">
                  <div v-for="(item, index) in scope.outScope" :key="index" class="flex items-start space-x-2">
                    <input
                      v-model="scope.outScope[index]"
                      type="text"
                      placeholder="What will be excluded..."
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                    />
                    <button
                      v-if="scope.outScope.length > 1"
                      @click.prevent="scope.outScope.splice(index, 1)"
                      type="button"
                      class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <X class="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <button
                  @click.prevent="scope.outScope.push('')"
                  type="button"
                  class="mt-2 flex items-center space-x-1 px-3 py-1.5 text-sm border border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-red-500 hover:text-red-600 transition-colors"
                >
                  <Plus class="w-3 h-3" />
                  <span>Add Item</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 5: Methodology -->
          <div v-if="step === 5" class="space-y-4 animate-fade-in">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-900">Methodology</h3>
              <button
                v-if="!generatedSections.methodology && !generating.methodology"
                @click.prevent="generateSection('methodology')"
                type="button"
                class="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                <Sparkles class="w-4 h-4" />
                <span>Generate with AI</span>
              </button>
              <div v-if="generating.methodology" class="flex items-center space-x-2 text-primary-600">
                <Loader2 class="w-5 h-5 animate-spin" />
                <span class="text-sm">Generating...</span>
              </div>
            </div>

            <div>
              <label for="methodology" class="block text-sm font-medium text-gray-700 mb-1">
                Methodology Section
              </label>
              <textarea
                id="methodology"
                v-model="generatedSections.methodology"
                rows="10"
                placeholder="Click 'Generate with AI' or describe your approach, phases, tools, and testing strategy..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Describe your development approach, phases, tools, and validation methods (200-250 words)</p>
            </div>
          </div>

          <!-- Step 6: Timeline -->
          <div v-if="step === 6" class="space-y-4 animate-fade-in">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-semibold text-gray-900">Project Timeline</h3>
              <button
                v-if="timeline.length === 0 && !generating.timeline"
                @click.prevent="generateSection('timeline')"
                type="button"
                class="flex items-center space-x-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
              >
                <Sparkles class="w-4 h-4" />
                <span>Generate with AI</span>
              </button>
              <div v-if="generating.timeline" class="flex items-center space-x-2 text-primary-600">
                <Loader2 class="w-5 h-5 animate-spin" />
                <span class="text-sm">Generating...</span>
              </div>
            </div>

            <div class="space-y-4">
              <div v-for="(phase, index) in timeline" :key="index" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <input
                    v-model="phase.phase"
                    type="text"
                    placeholder="Phase name..."
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all font-medium"
                  />
                  <button
                    v-if="timeline.length > 1"
                    @click.prevent="timeline.splice(index, 1)"
                    type="button"
                    class="ml-2 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 class="w-5 h-5" />
                  </button>
                </div>

                <div class="grid grid-cols-2 gap-3 mb-3">
                  <input
                    v-model="phase.duration"
                    type="text"
                    placeholder="Duration (e.g., 2-3 weeks)"
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                  />
                  <input
                    v-model="phase.deliverable"
                    type="text"
                    placeholder="Key deliverable..."
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                  />
                </div>

                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-2">Activities:</label>
                  <div class="space-y-2">
                    <div v-for="(activity, actIdx) in phase.activities" :key="actIdx" class="flex items-center space-x-2">
                      <input
                        v-model="phase.activities[actIdx]"
                        type="text"
                        placeholder="Activity..."
                        class="flex-1 px-3 py-1.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-sm"
                      />
                      <button
                        v-if="phase.activities.length > 1"
                        @click.prevent="phase.activities.splice(actIdx, 1)"
                        type="button"
                        class="p-1.5 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <X class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  <button
                    @click.prevent="phase.activities.push('')"
                    type="button"
                    class="mt-2 flex items-center space-x-1 px-2 py-1 text-xs border border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-primary-500 hover:text-primary-600 transition-colors"
                  >
                    <Plus class="w-3 h-3" />
                    <span>Add Activity</span>
                  </button>
                </div>
              </div>
            </div>

            <button
              @click.prevent="addPhase"
              type="button"
              class="flex items-center space-x-2 px-4 py-2 border-2 border-dashed border-gray-300 text-gray-600 rounded-lg hover:border-primary-500 hover:text-primary-600 transition-colors w-full justify-center"
            >
              <Plus class="w-4 h-4" />
              <span>Add Another Phase</span>
            </button>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-2">
            <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>

          <!-- Navigation Buttons -->
          <div class="flex justify-between pt-4 border-t border-gray-200">
            <button
              v-if="step > 1"
              @click.prevent="previousStep"
              type="button"
              class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              ← Previous
            </button>
            <div v-else></div>

            <div class="flex space-x-3">
              <button
                v-if="step === 6"
                @click.prevent="previewProposal"
                type="button"
                class="px-6 py-2.5 border border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition-colors font-medium flex items-center space-x-2"
              >
                <FileText class="w-4 h-4" />
                <span>Preview</span>
              </button>
              <button
                v-if="step < 6"
                type="submit"
                class="px-6 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
              >
                Next →
              </button>
              <button
                v-else
                @click.prevent="downloadProposal"
                type="button"
                class="px-6 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium flex items-center space-x-2"
              >
                <FileDown class="w-4 h-4" />
                <span>Download Proposal</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </transition>

  <!-- Preview Modal -->
  <transition name="modal">
    <div v-if="showPreview" class="fixed inset-0 z-[60] flex items-center justify-center bg-black bg-opacity-50 p-4" @click.self="showPreview = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 p-6 rounded-t-2xl sticky top-0 z-10">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-white">Proposal Preview</h2>
            <button @click="showPreview = false" class="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors">
              <X class="w-6 h-6 text-white" />
            </button>
          </div>
        </div>

        <div class="p-8 prose max-w-none">
          <div v-html="previewContent"></div>
        </div>

        <div class="p-6 border-t border-gray-200 flex justify-end space-x-3 sticky bottom-0 bg-white">
          <button
            @click="showPreview = false"
            class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
          >
            Close
          </button>
          <button
            @click="downloadProposal"
            class="px-6 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium flex items-center space-x-2"
          >
            <FileDown class="w-4 h-4" />
            <span>Download</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { X, Sparkles, Loader2, AlertCircle, Plus, Trash2, Check, FileText, FileDown, Heart, CheckCircle } from 'lucide-vue-next'
import proposalService from '../services/proposalService.js'
import authService from '../services/authService.js'
import favouriteService from '../services/favouriteService.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  projectTopic: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const step = ref(1)
const error = ref('')
const success = ref('')
const showPreview = ref(false)
const previewContent = ref('')

const formData = ref({
  title: '',
  description: '',
  domain: '',
  program: '',
  technologies: '',
  supervisor: ''
})

const generatedSections = ref({
  background: '',
  methodology: ''
})

const objectives = ref([''])
const scope = ref({
  inScope: [''],
  outScope: ['']
})
const timeline = ref([])

const generating = ref({
  background: false,
  objectives: false,
  methodology: false,
  scope: false,
  timeline: false
})

const userFavourites = ref([])
const selectedFavouriteId = ref('')
const loadingFavourites = ref(false)

// Fetch favourites when modal opens
const fetchFavourites = async () => {
  loadingFavourites.value = true
  try {
    await favouriteService.getFavourites()
    userFavourites.value = favouriteService.favourites.value || []
  } catch (err) {
    console.error('Error fetching favourites:', err)
    userFavourites.value = []
  } finally {
    loadingFavourites.value = false
  }
}

// Auto-populate from selected favourite
const handleFavouriteSelection = () => {
  if (!selectedFavouriteId.value) return
  
  const favourite = userFavourites.value.find(f => f.id === parseInt(selectedFavouriteId.value))
  if (!favourite) return
  
  // Get data from project_topic or custom fields
  const topic = favourite.project_topic || {}
  
  // Populate form fields from favourite
  formData.value.title = favourite.custom_title || topic.title || ''
  formData.value.description = topic.description || ''
  formData.value.domain = topic.domain || ''
  
  // Handle technologies - convert array to comma-separated string
  if (topic.technologies) {
    formData.value.technologies = Array.isArray(topic.technologies) 
      ? topic.technologies.join(', ') 
      : topic.technologies
  }
}

// Initialize with project topic if provided
watch(() => props.isOpen, async (isOpen) => {
  if (isOpen) {
    // Auto-fill program from user profile FIRST
    const user = authService.currentUser
    if (user) {
      formData.value.program = user.program || ''
    }
    
    // Fetch favourites
    await fetchFavourites()
    
    if (props.projectTopic) {
      formData.value.title = props.projectTopic.title || ''
      formData.value.description = props.projectTopic.description || ''
      formData.value.technologies = props.projectTopic.technologies?.join(', ') || ''
    }
  }
})

const handleClose = () => {
  if (step.value > 1) {
    if (confirm('Are you sure you want to close? Your progress will be lost.')) {
      resetForm()
      emit('close')
    }
  } else {
    resetForm()
    emit('close')
  }
}

const resetForm = () => {
  step.value = 1
  error.value = ''
  selectedFavouriteId.value = ''
  formData.value = {
    title: '',
    description: '',
    domain: '',
    program: '',
    technologies: '',
    supervisor: ''
  }
  generatedSections.value = {
    background: '',
    methodology: ''
  }
  objectives.value = ['']
  scope.value = {
    inScope: [''],
    outScope: ['']
  }
  timeline.value = []
}

const handleNext = () => {
  error.value = ''
  
  if (step.value === 1) {
    if (!formData.value.title || !formData.value.description || !formData.value.domain || !formData.value.program || !formData.value.technologies) {
      error.value = 'Please fill in all required fields'
      return
    }
  }
  
  if (step.value < 6) {
    step.value++
  }
}

const previousStep = () => {
  error.value = ''
  if (step.value > 1) {
    step.value--
  }
}

const generateSection = async (sectionType) => {
  error.value = ''
  generating.value[sectionType] = true

  try {
    const projectData = {
      title: formData.value.title,
      description: formData.value.description,
      program: formData.value.program,
      domain: formData.value.domain,
      technologies: formData.value.technologies
    }

    const result = await proposalService.generateProposalSection(sectionType, projectData)

    if (sectionType === 'objectives') {
      objectives.value = Array.isArray(result) ? result : [result]
    } else if (sectionType === 'scope') {
      scope.value = result
    } else if (sectionType === 'timeline') {
      timeline.value = Array.isArray(result) ? result : []
    } else {
      generatedSections.value[sectionType] = result
    }
  } catch (err) {
    console.error(`Error generating ${sectionType}:`, err)
    error.value = `Failed to generate ${sectionType}. Please try again or enter manually.`
  } finally {
    generating.value[sectionType] = false
  }
}

const addObjective = () => {
  objectives.value.push('')
}

const removeObjective = (index) => {
  if (objectives.value.length > 1) {
    objectives.value.splice(index, 1)
  }
}

const addPhase = () => {
  timeline.value.push({
    phase: '',
    duration: '',
    activities: [''],
    deliverable: ''
  })
}

const previewProposal = () => {
  const proposalData = {
    background: generatedSections.value.background,
    objectives: objectives.value.filter(o => o.trim()),
    scope: scope.value,
    methodology: generatedSections.value.methodology,
    timeline: timeline.value
  }

  const projectInfo = {
    title: formData.value.title,
    studentName: authService.currentUser?.full_name || 'Student Name',
    program: formData.value.program,
    supervisor: formData.value.supervisor
  }

  const markdown = proposalService.exportToMarkdown(proposalData, projectInfo)
  
  // Convert markdown to HTML for preview (simple conversion)
  previewContent.value = markdown
    .replace(/^# (.+)$/gm, '<h1 class="text-3xl font-bold mb-4">$1</h1>')
    .replace(/^## (.+)$/gm, '<h2 class="text-2xl font-bold mt-6 mb-3">$1</h2>')
    .replace(/^### (.+)$/gm, '<h3 class="text-xl font-semibold mt-4 mb-2">$1</h3>')
    .replace(/^\*\*(.+?)\*\*/gm, '<strong>$1</strong>')
    .replace(/^- (.+)$/gm, '<li class="ml-4">$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li class="ml-4">$2</li>')
    .replace(/^---$/gm, '<hr class="my-4" />')
    .replace(/\n\n/g, '</p><p class="mb-2">')
    .replace(/^(?!<[hlu])/gm, '<p class="mb-2">')

  showPreview.value = true
}

const downloadProposal = () => {
  const proposalData = {
    background: generatedSections.value.background,
    objectives: objectives.value.filter(o => o.trim()),
    scope: scope.value,
    methodology: generatedSections.value.methodology,
    timeline: timeline.value
  }

  const projectInfo = {
    title: formData.value.title,
    studentName: authService.currentUser?.full_name || 'Student Name',
    program: formData.value.program,
    supervisor: formData.value.supervisor
  }

  // Generate PDF instead of Markdown
  const pdf = proposalService.exportToPDF(proposalData, projectInfo)
  const filename = `${formData.value.title.replace(/[^a-z0-9]/gi, '_')}_Proposal.pdf`
  
  pdf.save(filename)
  
  showPreview.value = false
  
  // Show success message
  success.value = `Proposal "${formData.value.title}" downloaded successfully as PDF!`
  
  // Auto-hide success message after 5 seconds
  setTimeout(() => {
    success.value = ''
  }, 5000)
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

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.prose {
  color: #374151;
}

.prose h1 {
  color: #111827;
}

.prose h2 {
  color: #1f2937;
}

.prose h3 {
  color: #374151;
}

.prose li {
  margin-bottom: 0.5rem;
}
</style>
