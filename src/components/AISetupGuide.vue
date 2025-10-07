<template>
  <div class="max-w-4xl mx-auto">
    <div class="card">
      <div class="text-center mb-8">
        <h3 class="text-3xl font-bold text-gray-900 mb-4">AI Integration Setup Guide</h3>
        <p class="text-gray-600">Configure AI services to enable personalized topic generation</p>
      </div>

      <!-- OpenAI Setup -->
      <div class="mb-8">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <Sparkles class="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">OpenAI GPT (Recommended)</h4>
            <p class="text-gray-600">High-quality topic generation with GPT-3.5-turbo</p>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-6">
          <h5 class="font-semibold text-gray-900 mb-3">Setup Steps:</h5>
          <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
            <li>Visit <a href="https://platform.openai.com/api-keys" target="_blank" class="text-primary-600 hover:underline">OpenAI Platform</a> and create an account</li>
            <li>Generate a new API key</li>
            <li>Create a <code class="bg-gray-200 px-2 py-1 rounded text-xs">.env</code> file in your project root</li>
            <li>Add your API key: <code class="bg-gray-200 px-2 py-1 rounded text-xs">VITE_OPENAI_API_KEY=your_api_key_here</code></li>
            <li>Restart your development server</li>
          </ol>
          
          <div class="mt-4 p-4 bg-blue-50 rounded-lg">
            <h6 class="font-semibold text-blue-900 mb-2">Cost Information:</h6>
            <p class="text-sm text-blue-800">
              GPT-3.5-turbo costs approximately $0.002 per 1K tokens. 
              Each topic generation uses roughly 500-1000 tokens (~$0.001-0.002 per request).
            </p>
          </div>
        </div>
      </div>

      <!-- Google Gemini Setup -->
      <div class="mb-8">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <Brain class="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">Google Gemini (Alternative)</h4>
            <p class="text-gray-600">Competitive AI model with good performance</p>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-6">
          <h5 class="font-semibold text-gray-900 mb-3">Setup Steps:</h5>
          <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
            <li>Visit <a href="https://makersuite.google.com/app/apikey" target="_blank" class="text-primary-600 hover:underline">Google AI Studio</a></li>
            <li>Create a new API key</li>
            <li>Add to your <code class="bg-gray-200 px-2 py-1 rounded text-xs">.env</code> file: <code class="bg-gray-200 px-2 py-1 rounded text-xs">VITE_GEMINI_API_KEY=your_api_key_here</code></li>
            <li>Update the provider in <code class="bg-gray-200 px-2 py-1 rounded text-xs">src/services/aiService.js</code></li>
          </ol>
        </div>
      </div>

      <!-- Hugging Face Setup -->
      <div class="mb-8">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <Cpu class="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h4 class="text-xl font-bold text-gray-900">Hugging Face (Free Option)</h4>
            <p class="text-gray-600">Open-source models with free tier available</p>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-6">
          <h5 class="font-semibold text-gray-900 mb-3">Setup Steps:</h5>
          <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
            <li>Visit <a href="https://huggingface.co/settings/tokens" target="_blank" class="text-primary-600 hover:underline">Hugging Face</a> and create an account</li>
            <li>Generate an access token (optional for free tier)</li>
            <li>Add to your <code class="bg-gray-200 px-2 py-1 rounded text-xs">.env</code> file: <code class="bg-gray-200 px-2 py-1 rounded text-xs">VITE_HUGGINGFACE_API_KEY=your_token_here</code></li>
            <li>Update the provider in <code class="bg-gray-200 px-2 py-1 rounded text-xs">src/services/aiService.js</code></li>
          </ol>
          
          <div class="mt-4 p-4 bg-green-50 rounded-lg">
            <h6 class="font-semibold text-green-900 mb-2">Free Tier:</h6>
            <p class="text-sm text-green-800">
              Hugging Face offers free API access with rate limits. 
              Perfect for development and testing.
            </p>
          </div>
        </div>
      </div>

      <!-- Configuration Example -->
      <div class="mb-8">
        <h4 class="text-xl font-bold text-gray-900 mb-4">Environment Configuration</h4>
        <div class="bg-gray-900 rounded-lg p-6">
          <pre class="text-green-400 text-sm overflow-x-auto"><code># .env file
VITE_OPENAI_API_KEY=sk-your-openai-api-key-here
VITE_GEMINI_API_KEY=your-gemini-api-key-here
VITE_HUGGINGFACE_API_KEY=your-huggingface-token-here

# Optional: Switch AI provider
VITE_AI_PROVIDER=openai  # openai, gemini, huggingface</code></pre>
        </div>
      </div>

      <!-- Testing Section -->
      <div class="mb-8">
        <h4 class="text-xl font-bold text-gray-900 mb-4">Testing Your Setup</h4>
        <div class="bg-gray-50 rounded-lg p-6">
          <p class="text-gray-700 mb-4">After setting up your API key, test the integration:</p>
          <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
            <li>Fill out the FYP form with sample data</li>
            <li>Click "Generate FYP Topics"</li>
            <li>Check the AI status banner at the top</li>
            <li>Verify that topics are generated (not mock data)</li>
          </ol>
        </div>
      </div>

      <!-- Troubleshooting -->
      <div class="mb-8">
        <h4 class="text-xl font-bold text-gray-900 mb-4">Troubleshooting</h4>
        <div class="space-y-4">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h5 class="font-semibold text-yellow-800 mb-2">API Key Not Working</h5>
            <ul class="text-sm text-yellow-700 space-y-1">
              <li>• Ensure your API key is correct and active</li>
              <li>• Check that you have sufficient credits/quota</li>
              <li>• Verify the .env file is in the project root</li>
              <li>• Restart your development server after adding the key</li>
            </ul>
          </div>
          
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <h5 class="font-semibold text-red-800 mb-2">CORS Errors</h5>
            <ul class="text-sm text-red-700 space-y-1">
              <li>• Some APIs may require server-side implementation</li>
              <li>• Consider using a proxy server for production</li>
              <li>• Check API documentation for CORS policies</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Security Note -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h4 class="font-semibold text-blue-900 mb-2">Security Best Practices</h4>
        <ul class="text-sm text-blue-800 space-y-1">
          <li>• Never commit your .env file to version control</li>
          <li>• Use environment variables in production</li>
          <li>• Monitor your API usage and set spending limits</li>
          <li>• Rotate API keys regularly</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Sparkles, Brain, Cpu } from 'lucide-vue-next'
</script>
