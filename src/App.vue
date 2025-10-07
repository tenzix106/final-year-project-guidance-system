<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
              <GraduationCap class="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 class="text-2xl font-bold gradient-text">FYP Guidance</h1>
              <p class="text-sm text-gray-600">Research & Topic Generator</p>
            </div>
          </div>
          <nav class="hidden md:flex space-x-8">
            <a href="#form" class="text-gray-600 hover:text-primary-600 transition-colors">Generate Topics</a>
            <a href="#results" class="text-gray-600 hover:text-primary-600 transition-colors">View Results</a>
            <a href="#resources" class="text-gray-600 hover:text-primary-600 transition-colors">Resources</a>
            <a href="#setup" class="text-gray-600 hover:text-primary-600 transition-colors">AI Setup</a>
          </nav>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-5xl font-bold text-gray-900 mb-6 animate-fade-in">
          Find Your Perfect
          <span class="gradient-text">Final Year Project</span>
        </h2>
        <p class="text-xl text-gray-600 mb-8 animate-slide-up">
          Get AI-powered project suggestions tailored to your interests, skills, and academic requirements.
          Discover relevant resources and guidance for your research journey.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up">
          <button @click="scrollToForm" class="btn-primary">
            <Sparkles class="w-5 h-5 inline mr-2" />
            Generate Topics
          </button>
          <button @click="scrollToResults" class="btn-secondary">
            <BookOpen class="w-5 h-5 inline mr-2" />
            View Examples
          </button>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <!-- AI Status Banner -->
      <div v-if="aiStatus.provider" class="mb-8">
        <div class="card max-w-4xl mx-auto">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center"
                   :class="useAI ? 'bg-green-100' : 'bg-yellow-100'">
                <Sparkles class="w-4 h-4" :class="useAI ? 'text-green-600' : 'text-yellow-600'" />
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">
                  {{ useAI ? 'AI-Powered Topic Generation' : 'Mock Data Mode' }}
                </h4>
                <p class="text-sm text-gray-600">
                  {{ useAI ? `Using ${aiStatus.provider.toUpperCase()} AI for personalized topic generation` : 'AI not configured - using sample topics' }}
                </p>
              </div>
            </div>
            <div v-if="!useAI" class="text-right">
              <p class="text-xs text-gray-500 mb-1">To enable AI features:</p>
              <a href="#setup" class="text-sm text-primary-600 hover:text-primary-700 underline">
                Setup Guide
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Section -->
      <section id="form" class="mb-20">
        <FYPForm @generate-topics="handleGenerateTopics" />
      </section>

      <!-- Results Section -->
      <section id="results" class="mb-20">
        <!-- AI Error Display -->
        <div v-if="aiError" class="mb-6">
          <div class="card max-w-4xl mx-auto bg-red-50 border-red-200">
            <div class="flex items-center space-x-3">
              <AlertCircle class="w-5 h-5 text-red-600" />
              <div>
                <h4 class="font-semibold text-red-800">AI Generation Error</h4>
                <p class="text-sm text-red-700">{{ aiError }}</p>
                <p class="text-xs text-red-600 mt-1">Showing sample topics instead.</p>
              </div>
            </div>
          </div>
        </div>
        
        <FYPResults :topics="generatedTopics" :loading="isLoading" />
      </section>

      <!-- Resources Section -->
      <section id="resources" class="mb-20">
        <FYPResources />
      </section>

      <!-- AI Setup Section -->
      <section id="setup" class="mb-20">
        <AISetupGuide />
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-8 h-8 bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
                <GraduationCap class="w-5 h-5 text-white" />
              </div>
              <span class="text-xl font-bold gradient-text">FYP Guidance</span>
            </div>
            <p class="text-gray-600">
              Empowering students with AI-driven project suggestions and comprehensive research guidance.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Links</h3>
            <ul class="space-y-2">
              <li><a href="#form" class="text-gray-600 hover:text-primary-600 transition-colors">Generate Topics</a></li>
              <li><a href="#results" class="text-gray-600 hover:text-primary-600 transition-colors">View Results</a></li>
              <li><a href="#resources" class="text-gray-600 hover:text-primary-600 transition-colors">Resources</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Support</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Help Center</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Contact Us</a></li>
              <li><a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">Documentation</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-200 mt-8 pt-8 text-center">
          <p class="text-gray-600">&copy; 2024 FYP Guidance System. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { GraduationCap, Sparkles, BookOpen, AlertCircle } from 'lucide-vue-next'
import FYPForm from './components/FYPForm.vue'
import FYPResults from './components/FYPResults.vue'
import FYPResources from './components/FYPResources.vue'
import AISetupGuide from './components/AISetupGuide.vue'
import aiService from './services/aiService.js'

const generatedTopics = ref([])
const isLoading = ref(false)
const aiError = ref('')
const aiStatus = ref({})
const useAI = ref(false)

const scrollToForm = () => {
  document.getElementById('form')?.scrollIntoView({ behavior: 'smooth' })
}

const scrollToResults = () => {
  document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
}

const handleGenerateTopics = async (formData) => {
  isLoading.value = true
  aiError.value = ''
  
  try {
    if (useAI.value && aiService.isConfigured()) {
      // Use AI service for topic generation
      generatedTopics.value = await aiService.generateTopics(formData)
    } else {
      // Fallback to mock data
      generatedTopics.value = generateMockTopics(formData)
    }
  } catch (error) {
    console.error('Topic generation error:', error)
    aiError.value = error.message
    // Fallback to mock data on error
    generatedTopics.value = generateMockTopics(formData)
  } finally {
    isLoading.value = false
    scrollToResults()
  }
}

// Check AI service status on component mount
onMounted(() => {
  aiStatus.value = aiService.getStatus()
  useAI.value = aiService.isConfigured()
})

const generateMockTopics = (formData) => {
  // Parse skills and interests from text input
  const skills = formData.skillsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
  const interests = formData.interestsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
  
  // Generate topics based on program and interests
  const topics = []
  
  // Technology/Computing topics
  if (formData.program.includes('computer') || formData.program.includes('software') || 
      formData.program.includes('information') || formData.program.includes('data') ||
      formData.program.includes('cybersecurity') || interests.some(i => 
        i.toLowerCase().includes('ai') || i.toLowerCase().includes('machine learning') ||
        i.toLowerCase().includes('software') || i.toLowerCase().includes('programming'))) {
    
    topics.push({
      id: 1,
      title: "AI-Powered Learning Management System",
      description: "Develop an intelligent LMS that adapts to individual learning patterns and provides personalized content recommendations using machine learning algorithms.",
      difficulty: "Advanced",
      duration: "6-8 months",
      skills: ["Machine Learning", "Web Development", "Database Design", "Python"],
      resources: [
        { type: "Paper", title: "Personalized Learning Systems: A Survey", url: "#" },
        { type: "Tutorial", title: "Building ML Models with TensorFlow", url: "#" },
        { type: "Tool", title: "React.js Documentation", url: "#" }
      ],
      tags: ["AI/ML", "Education", "Web Development"]
    })
  }
  
  // Business/Marketing topics
  if (formData.program.includes('business') || formData.program.includes('marketing') || 
      formData.program.includes('finance') || formData.program.includes('management') ||
      interests.some(i => i.toLowerCase().includes('business') || i.toLowerCase().includes('marketing') ||
        i.toLowerCase().includes('finance') || i.toLowerCase().includes('e-commerce'))) {
    
    topics.push({
      id: 2,
      title: "Digital Marketing Analytics Dashboard",
      description: "Create a comprehensive analytics platform for tracking and analyzing digital marketing campaigns across multiple channels with real-time insights.",
      difficulty: "Intermediate",
      duration: "4-6 months",
      skills: ["Data Analytics", "Web Development", "Marketing", "Statistics"],
      resources: [
        { type: "Paper", title: "Digital Marketing Analytics: Current Trends", url: "#" },
        { type: "Tutorial", title: "Building Analytics Dashboards", url: "#" },
        { type: "Tool", title: "Google Analytics API Documentation", url: "#" }
      ],
      tags: ["Marketing", "Analytics", "Business Intelligence"]
    })
  }
  
  // Engineering topics
  if (formData.program.includes('engineering') || formData.program.includes('mechanical') ||
      formData.program.includes('electrical') || formData.program.includes('civil') ||
      interests.some(i => i.toLowerCase().includes('engineering') || i.toLowerCase().includes('automation') ||
        i.toLowerCase().includes('sustainability') || i.toLowerCase().includes('renewable'))) {
    
    topics.push({
      id: 3,
      title: "Smart Energy Management System for Buildings",
      description: "Design and implement an IoT-based system for monitoring and optimizing energy consumption in commercial buildings with predictive analytics.",
      difficulty: "Advanced",
      duration: "6-8 months",
      skills: ["IoT", "Embedded Systems", "Energy Systems", "Data Analytics"],
      resources: [
        { type: "Paper", title: "Smart Building Energy Management Systems", url: "#" },
        { type: "Tutorial", title: "IoT Sensor Networks for Energy Monitoring", url: "#" },
        { type: "Tool", title: "Arduino and Raspberry Pi Integration", url: "#" }
      ],
      tags: ["IoT", "Energy", "Sustainability", "Automation"]
    })
  }
  
  // Health/Medical topics
  if (formData.program.includes('medicine') || formData.program.includes('nursing') ||
      formData.program.includes('pharmacy') || formData.program.includes('biology') ||
      interests.some(i => i.toLowerCase().includes('health') || i.toLowerCase().includes('medical') ||
        i.toLowerCase().includes('healthcare') || i.toLowerCase().includes('biotechnology'))) {
    
    topics.push({
      id: 4,
      title: "Telemedicine Platform for Remote Patient Monitoring",
      description: "Develop a comprehensive telemedicine platform that enables remote patient monitoring, virtual consultations, and health data tracking.",
      difficulty: "Advanced",
      duration: "7-9 months",
      skills: ["Web Development", "Mobile Development", "Healthcare Systems", "Data Security"],
      resources: [
        { type: "Paper", title: "Telemedicine: Current Applications and Future Prospects", url: "#" },
        { type: "Tutorial", title: "Healthcare App Development", url: "#" },
        { type: "Tool", title: "HIPAA Compliance Guidelines", url: "#" }
      ],
      tags: ["Healthcare", "Telemedicine", "Mobile Health", "Patient Care"]
    })
  }
  
  // Social Sciences/Psychology topics
  if (formData.program.includes('psychology') || formData.program.includes('sociology') ||
      formData.program.includes('education') || formData.program.includes('social') ||
      interests.some(i => i.toLowerCase().includes('psychology') || i.toLowerCase().includes('social') ||
        i.toLowerCase().includes('education') || i.toLowerCase().includes('behavior'))) {
    
    topics.push({
      id: 5,
      title: "Social Media Impact on Mental Health Study",
      description: "Conduct a comprehensive research study analyzing the relationship between social media usage patterns and mental health outcomes among university students.",
      difficulty: "Intermediate",
      duration: "5-7 months",
      skills: ["Research Methods", "Statistics", "Data Analysis", "Survey Design"],
      resources: [
        { type: "Paper", title: "Social Media and Mental Health: A Systematic Review", url: "#" },
        { type: "Tutorial", title: "Statistical Analysis with SPSS", url: "#" },
        { type: "Tool", title: "Survey Design Best Practices", url: "#" }
      ],
      tags: ["Psychology", "Social Media", "Mental Health", "Research"]
    })
  }
  
  // Environmental/Sustainability topics
  if (formData.program.includes('environmental') || formData.program.includes('biology') ||
      interests.some(i => i.toLowerCase().includes('environment') || i.toLowerCase().includes('climate') ||
        i.toLowerCase().includes('sustainability') || i.toLowerCase().includes('renewable'))) {
    
    topics.push({
      id: 6,
      title: "Climate Change Impact Assessment Tool",
      description: "Develop a web-based tool for assessing and visualizing the potential impacts of climate change on local communities and ecosystems.",
      difficulty: "Intermediate",
      duration: "6-8 months",
      skills: ["Web Development", "Data Visualization", "Environmental Science", "GIS"],
      resources: [
        { type: "Paper", title: "Climate Change Impact Assessment Methodologies", url: "#" },
        { type: "Tutorial", title: "Environmental Data Visualization", url: "#" },
        { type: "Tool", title: "GIS Software Documentation", url: "#" }
      ],
      tags: ["Climate Change", "Environmental Science", "Data Visualization", "Sustainability"]
    })
  }
  
  // If no specific topics match, generate generic ones based on skills
  if (topics.length === 0) {
    topics.push({
      id: 1,
      title: "Comprehensive Research Study in Your Field",
      description: `Conduct an in-depth research study focusing on ${interests[0] || 'your area of interest'} using ${skills[0] || 'your skills'} to contribute new knowledge to the field.`,
      difficulty: formData.difficulty === 'beginner' ? 'Beginner' : formData.difficulty === 'advanced' ? 'Advanced' : 'Intermediate',
      duration: formData.duration === '3-4' ? '3-4 months' : formData.duration === '4-6' ? '4-6 months' : formData.duration === '6-8' ? '6-8 months' : '8-12 months',
      skills: skills.slice(0, 4),
      resources: [
        { type: "Paper", title: "Research Methods in Your Field", url: "#" },
        { type: "Tutorial", title: "Academic Writing and Research", url: "#" },
        { type: "Tool", title: "Research Tools and Databases", url: "#" }
      ],
      tags: ["Research", "Academic Study", "Field Analysis"]
    })
  }
  
  return topics.slice(0, 3) // Return up to 3 topics
}
</script>
