// AI Service for FYP Topic Generation
// This service handles communication with AI APIs for generating personalized project topics

class AIService {
  constructor() {
    // You can switch between different AI providers
    this.provider = 'gemini' // 'openai', 'gemini', 'huggingface'
    this.apiKey = import.meta.env.VITE_GEMINI_API_KEY || ''
    this.baseURL = 'https://generativelanguage.googleapis.com/v1'
    this.backendBaseURL = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:3001'
  }

  /**
   * Generate FYP topics based on student profile
   * @param {Object} formData - Student form data
   * @returns {Promise<Array>} Generated topics
   */
  async generateTopics(formData) {
    try {
      const prompt = this.buildPrompt(formData)
      
      switch (this.provider) {
        case 'openai':
          return await this.generateWithOpenAI(prompt)
        case 'gemini':
          return await this.generateWithGemini(prompt)
        case 'huggingface':
          return await this.generateWithHuggingFace(prompt)
        default:
          throw new Error('Unsupported AI provider')
      }
    } catch (error) {
      console.error('AI Service Error:', error)
      throw new Error('Failed to generate topics. Please try again.')
    }
  }

  /**
   * Build the prompt for AI topic generation
   */
  buildPrompt(formData) {
    const skills = formData.skillsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
    const interests = formData.interestsText.split(/[,\n]/).map(s => s.trim()).filter(s => s.length > 0)
    
    return `You are an expert academic advisor helping students find their perfect Final Year Project (FYP) topic.

STUDENT PROFILE:
- Name: ${formData.name}
- Program: ${formData.program}
- Academic Year: ${formData.academicYear}
- Skills & Knowledge: ${skills.join(', ')}
- Areas of Interest: ${interests.join(', ')}
- Difficulty Preference: ${formData.difficulty}
- Project Duration: ${formData.duration}
- Project Type: ${formData.projectType}
- Additional Requirements: ${formData.additionalRequirements || 'None specified'}

TASK: Generate 3 personalized, innovative, and feasible FYP project topics that match the student's profile.

REQUIREMENTS:
1. Each topic should be relevant to their program and interests
2. Match the specified difficulty level and duration
3. Be innovative but feasible for a final year student
4. Include practical applications and real-world impact
5. Consider current trends and technologies in their field

OUTPUT FORMAT: Return a JSON array with exactly 3 objects, each containing:
{
  "id": number,
  "title": "Project Title",
  "description": "Detailed project description (2-3 sentences)",
  "difficulty": "Beginner/Intermediate/Advanced",
  "duration": "X-Y months",
  "skills": ["skill1", "skill2", "skill3", "skill4"],
  "resources": [
    {"type": "Paper", "title": "Resource Title", "url": "#"},
    {"type": "Tutorial", "title": "Tutorial Title", "url": "#"},
    {"type": "Tool", "title": "Tool Title", "url": "#"}
  ],
  "tags": ["tag1", "tag2", "tag3"],
  "objectives": ["objective1", "objective2", "objective3"],
  "methodology": "Brief methodology description",
  "expectedOutcomes": "What the student will achieve"
}

Make sure the JSON is valid and properly formatted.`
  }

  /**
   * Generate topics using OpenAI GPT API
   */
  async generateWithOpenAI(prompt) {
    if (!this.apiKey) {
      throw new Error('OpenAI API key not configured. Please add VITE_OPENAI_API_KEY to your environment variables.')
    }

    const response = await fetch(`${this.baseURL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'You are an expert academic advisor specializing in Final Year Project guidance. Always respond with valid JSON format.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        max_tokens: 2000,
        temperature: 0.7,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0
      })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(`OpenAI API Error: ${error.error?.message || 'Unknown error'}`)
    }

    const data = await response.json()
    const content = data.choices[0].message.content
    
    try {
      // Extract JSON from the response
      const jsonMatch = content.match(/\[[\s\S]*\]/)
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0])
      } else {
        throw new Error('No valid JSON found in response')
      }
    } catch (parseError) {
      console.error('JSON Parse Error:', parseError)
      console.error('Raw Response:', content)
      throw new Error('Failed to parse AI response')
    }
  }

  /**
   * Generate topics using Google Gemini API
   */
  async generateWithGemini(prompt) {
    // Use Express backend for AI proxy to avoid CORS issues
    const backendBase = import.meta.env.VITE_BACKEND_BASE_URL || 'http://localhost:3002'
    const response = await fetch(`${backendBase}/api/generate-topics`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(`Gemini API Error: ${error.error || 'Unknown error'}`)
    }

    const data = await response.json()

    // Validate candidates exist
    if (!data || !Array.isArray(data.candidates) || data.candidates.length === 0) {
      const blockReason = data?.promptFeedback?.blockReason || 'No candidates returned'
      throw new Error(`Gemini returned no candidates (${blockReason}). Please adjust your input and try again.`)
    }

    const firstCandidate = data.candidates[0]
    const parts = firstCandidate?.content?.parts || []
    const content = parts
      .map(p => (typeof p.text === 'string' ? p.text : ''))
      .filter(t => t && t.trim().length > 0)
      .join('\n')
      .trim()

    if (!content) {
      const finishReason = firstCandidate?.finishReason || data?.promptFeedback?.blockReason || 'Empty content'
      throw new Error(`Gemini produced empty content (${finishReason}). Try again or refine inputs.`)
    }

    try {
      // Remove markdown code fences
      const withoutFences = content.replace(/```json\s*|```/g, '').trim()

      // Extract a balanced JSON array starting from the first '['
      const startIdx = withoutFences.indexOf('[')
      if (startIdx === -1) {
        throw new Error('No JSON array start found in response')
      }
      let depth = 0
      let endIdx = -1
      for (let i = startIdx; i < withoutFences.length; i++) {
        const ch = withoutFences[i]
        if (ch === '[') depth++
        if (ch === ']') depth--
        if (depth === 0) { endIdx = i; break }
      }
      if (endIdx === -1) {
        throw new Error('Unbalanced JSON array in response')
      }
      let slice = withoutFences.slice(startIdx, endIdx + 1)

      // Remove trailing commas before } or ] to tolerate minor formatting
      slice = slice.replace(/,(\s*[}\]])/g, '$1')

      return JSON.parse(slice)
    } catch (parseError) {
      console.error('JSON Parse Error:', parseError)
      console.error('Raw Response:', content)
      throw new Error('Failed to parse Gemini response. Please try again.')
    }
  }

  /**
   * Generate topics using Hugging Face API
   */
  async generateWithHuggingFace(prompt) {
    const apiKey = import.meta.env.VITE_HUGGINGFACE_API_KEY
    const headers = {
      'Content-Type': 'application/json'
    }
    
    if (apiKey) {
      headers['Authorization'] = `Bearer ${apiKey}`
    }

    const response = await fetch('https://api-inference.huggingface.co/models/microsoft/DialoGPT-large', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        inputs: prompt,
        parameters: {
          max_length: 1000,
          temperature: 0.7,
          do_sample: true
        }
      })
    })

    if (!response.ok) {
      throw new Error('Hugging Face API Error')
    }

    const data = await response.json()
    // Hugging Face returns different format, would need custom parsing
    return this.parseHuggingFaceResponse(data)
  }

  /**
   * Parse Hugging Face response (custom implementation needed)
   */
  parseHuggingFaceResponse(data) {
    // This would need custom implementation based on the specific model
    // For now, return mock data
    return [
      {
        id: 1,
        title: "AI-Generated Topic",
        description: "This is a placeholder for Hugging Face generated content.",
        difficulty: "Intermediate",
        duration: "4-6 months",
        skills: ["AI/ML", "Research"],
        resources: [],
        tags: ["AI", "Research"],
        objectives: ["Learn AI concepts"],
        methodology: "Research-based approach",
        expectedOutcomes: "Understanding of AI applications"
      }
    ]
  }

  /**
   * Get AI service status
   */
  getStatus() {
    return {
      provider: this.provider,
      hasApiKey: !!import.meta.env.VITE_GEMINI_API_KEY,
      isConfigured: this.isConfigured()
    }
  }

  /**
   * Check if AI service is properly configured
   */
  isConfigured() {
    switch (this.provider) {
      case 'openai':
        return !!import.meta.env.VITE_OPENAI_API_KEY
      case 'gemini':
        return !!import.meta.env.VITE_GEMINI_API_KEY
      case 'huggingface':
        return true // Hugging Face can work without API key (with limitations)
      default:
        return false
    }
  }
}

// Export singleton instance
export default new AIService()
