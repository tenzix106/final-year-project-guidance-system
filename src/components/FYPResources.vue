<template>
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <h3 class="text-3xl font-bold text-gray-900 mb-4">Research Resources</h3>
      <p class="text-gray-600">Comprehensive collection of tools, papers, and guides for your FYP journey</p>
    </div>

    <!-- Resource Categories -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Academic Resources -->
      <div class="card">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <GraduationCap class="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">Academic Resources</h4>
            <p class="text-gray-600">Research papers, journals, and academic databases</p>
          </div>
        </div>
        
        <div class="space-y-4">
          <div v-for="resource in academicResources" :key="resource.name" 
               class="p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors cursor-pointer">
            <div class="flex items-start space-x-3">
              <component :is="resource.icon" class="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h5 class="font-medium text-gray-900">{{ resource.name }}</h5>
                <p class="text-sm text-gray-600">{{ resource.description }}</p>
                <a :href="resource.url" class="text-sm text-blue-600 hover:text-blue-700 mt-1 inline-block">
                  Visit Resource →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Development Tools -->
      <div class="card">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <Code class="w-6 h-6 text-green-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">Development Tools</h4>
            <p class="text-gray-600">Frameworks, libraries, and development environments</p>
          </div>
        </div>
        
        <div class="space-y-4">
          <div v-for="resource in developmentTools" :key="resource.name" 
               class="p-4 border border-gray-200 rounded-lg hover:border-green-300 transition-colors cursor-pointer">
            <div class="flex items-start space-x-3">
              <component :is="resource.icon" class="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <h5 class="font-medium text-gray-900">{{ resource.name }}</h5>
                <p class="text-sm text-gray-600">{{ resource.description }}</p>
                <a :href="resource.url" class="text-sm text-green-600 hover:text-green-700 mt-1 inline-block">
                  Get Started →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Materials -->
      <div class="card">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <BookOpen class="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">Learning Materials</h4>
            <p class="text-gray-600">Tutorials, courses, and educational content</p>
          </div>
        </div>
        
        <div class="space-y-4">
          <div v-for="resource in learningMaterials" :key="resource.name" 
               class="p-4 border border-gray-200 rounded-lg hover:border-purple-300 transition-colors cursor-pointer">
            <div class="flex items-start space-x-3">
              <component :is="resource.icon" class="w-5 h-5 text-purple-600 mt-0.5" />
              <div>
                <h5 class="font-medium text-gray-900">{{ resource.name }}</h5>
                <p class="text-sm text-gray-600">{{ resource.description }}</p>
                <a :href="resource.url" class="text-sm text-purple-600 hover:text-purple-700 mt-1 inline-block">
                  Start Learning →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Access Section -->
    <!-- <div class="mt-16">
      <h4 class="text-2xl font-bold text-gray-900 mb-8 text-center">Quick Access</h4>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button v-for="quickLink in quickLinks" :key="quickLink.name"
                class="p-6 bg-white rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition-all duration-200 text-center group">
          <component :is="quickLink.icon" class="w-8 h-8 text-primary-600 mx-auto mb-3 group-hover:scale-110 transition-transform" />
          <h5 class="font-medium text-gray-900">{{ quickLink.name }}</h5>
        </button>
      </div>
    </div> -->

    <!-- Tips Section -->
    <div class="mt-16 card">
      <h4 class="text-2xl font-bold text-gray-900 mb-6 text-center">FYP Success Tips</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(tip, index) in successTips" :key="index" 
             class="p-6 bg-gradient-to-br from-primary-50 to-purple-50 rounded-lg">
          <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center mb-4">
            <span class="text-white font-bold">{{ index + 1 }}</span>
          </div>
          <h5 class="font-semibold text-gray-900 mb-2">{{ tip.title }}</h5>
          <p class="text-gray-600 text-sm">{{ tip.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  GraduationCap, Code, BookOpen, FileText, Database, 
  Globe, Github, PlayCircle, Users, Calendar, 
  Target, Lightbulb, CheckCircle, TrendingUp,
  ExternalLink, Search, Download, Share2
} from 'lucide-vue-next'

const academicResources = [
  {
    name: 'Google Scholar',
    description: 'Search across many disciplines and sources for academic papers',
    icon: Search,
    url: 'https://scholar.google.com/'
  },
  {
    name: 'IEEE Xplore',
    description: 'Access to technical literature in engineering and technology',
    icon: FileText,
    url: 'https://scholar.google.com/'
  },
  {
    name: 'JSTOR',
    description: 'Digital library for academic journals, books, and primary sources',
    icon: Database,
    url: 'https://www.jstor.org/'
  },
  {
    name: 'PubMed',
    description: 'Database of biomedical literature and life sciences',
    icon: FileText,
    url: 'https://pubmed.ncbi.nlm.nih.gov/'
  },
  {
    name: 'ResearchGate',
    description: 'Professional network for scientists and researchers',
    icon: Users,
    url: 'https://www.researchgate.net/'
  },
  {
    name: 'ScienceDirect',
    description: 'Full-text scientific database covering all fields of science',
    icon: Database,
    url: 'https://www.sciencedirect.com/'
  }
]

const developmentTools = [
  {
    name: 'GitHub',
    description: 'Version control and collaboration platform',
    icon: Github,
    url: 'https://github.com/'
  },
  {
    name: 'VS Code',
    description: 'Popular code editor with extensive extensions',
    icon: Code,
    url: 'https://code.visualstudio.com/'
  },
  {
    name: 'Google Colab',
    description: 'Free cloud-based Jupyter notebook environment',
    icon: Globe,
    url: 'https://colab.research.google.com/'
  },
  {
    name: 'SPSS',
    description: 'Statistical analysis software for social sciences',
    icon: TrendingUp,
    url: 'https://www.ibm.com/products/spss-statistics'
  },
  {
    name: 'Tableau',
    description: 'Data visualization and business intelligence tool',
    icon: Target,
    url: 'https://www.tableau.com/'
  },
  {
    name: 'Mendeley',
    description: 'Reference manager and academic social network',
    icon: BookOpen,
    url: 'https://www.mendeley.com/'
  }
]

const learningMaterials = [
  {
    name: 'Coursera',
    description: 'Online courses from top universities and companies',
    icon: PlayCircle,
    url: 'https://www.coursera.org/'
  },
  {
    name: 'edX',
    description: 'Free online courses from leading universities',
    icon: PlayCircle,
    url: 'https://www.edx.org/'
  },
  {
    name: 'Khan Academy',
    description: 'Free educational resources across all subjects',
    icon: BookOpen,
    url: 'https://www.khanacademy.org/'
  },
  {
    name: 'YouTube Education',
    description: 'Free video tutorials and educational content',
    icon: PlayCircle,
    url: 'https://www.youtube.com/channel/UCtFRv9O2AHqOZjjynzrv-xg'
  },
  {
    name: 'Academic Writing Guides',
    description: 'Resources for improving academic writing skills',
    icon: FileText,
    url: 'https://subjectguides.york.ac.uk/academic-writing'
  }
  // {
  //   name: 'Research Methodology',
  //   description: 'Guides for conducting academic research',
  //   icon: Target,
  //   url: '#'
  // }
]

const quickLinks = [
  { name: 'Project Templates', icon: FileText },
  { name: 'Citation Tools', icon: BookOpen },
  { name: 'Timeline Planner', icon: Calendar },
  { name: 'Progress Tracker', icon: Target }
]

const successTips = [
  {
    title: 'Start Early',
    description: 'Begin your research and planning as soon as possible to avoid last-minute stress.'
  },
  {
    title: 'Choose Wisely',
    description: 'Select a topic that genuinely interests you and aligns with your career goals.'
  },
  {
    title: 'Plan Thoroughly',
    description: 'Create a detailed timeline with milestones and regular check-ins with your supervisor.'
  },
  {
    title: 'Document Everything',
    description: 'Keep detailed records of your research, experiments, and findings throughout the process.'
  },
  {
    title: 'Seek Feedback',
    description: 'Regularly consult with your supervisor and peers for guidance and improvement suggestions.'
  },
  {
    title: 'Stay Organized',
    description: 'Use project management tools and maintain a clean, well-structured codebase.'
  }
]
</script>
