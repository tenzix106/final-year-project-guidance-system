
import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Content filtering for inappropriate topics
const PROHIBITED_KEYWORDS = [
  // Explicit content
  'porn', 'pornography', 'sexual', 'nude', 'nudity', 'explicit', 'adult content', 'xxx',
  'sex', 'erotic', 'hentai', 'nsfw',
  
  // Violence & terrorism
  'terrorism', 'terrorist', 'bomb', 'explosive', 'weapon', 'violence', 'kill', 'murder',
  'assassination', 'extremist', 'radical', 'jihad', 'suicide bomber',
  
  // Hate speech & discrimination
  'racist', 'racism', 'hate speech', 'supremacy', 'genocide', 'ethnic cleansing',
  
  // Politics (controversial)
  'election fraud', 'coup', 'revolution', 'overthrow government', 'political assassination',
  
  // Illegal activities
  'drug trafficking', 'money laundering', 'illegal', 'counterfeit', 'fraud', 'scam',
  'hacking', 'phishing', 'malware', 'ransomware', 'cyber attack',
  
  // Self-harm
  'suicide', 'self-harm', 'self harm'
];

function containsProhibitedContent(text) {
  if (!text) return false;
  
  const lowerText = text.toLowerCase();
  
  for (const keyword of PROHIBITED_KEYWORDS) {
    // Use word boundary check to avoid false positives
    const regex = new RegExp(`\\b${keyword.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')}\\b`, 'i');
    if (regex.test(lowerText)) {
      return keyword;
    }
  }
  
  return false;
}

function validateContent(data) {
  const textsToCheck = [];
  
  // Extract all text fields to check
  if (typeof data === 'string') {
    textsToCheck.push(data);
  } else if (typeof data === 'object') {
    Object.values(data).forEach(value => {
      if (typeof value === 'string') {
        textsToCheck.push(value);
      } else if (Array.isArray(value)) {
        value.forEach(item => {
          if (typeof item === 'string') {
            textsToCheck.push(item);
          }
        });
      }
    });
  }
  
  // Check each text field
  for (const text of textsToCheck) {
    const prohibited = containsProhibitedContent(text);
    if (prohibited) {
      return {
        valid: false,
        keyword: prohibited
      };
    }
  }
  
  return { valid: true };
}

// Gemini API proxy endpoint
app.post('/api/generate-topics', async (req, res) => {
  try {
    const { prompt } = req.body;
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
      return res.status(500).json({ 
        error: 'Gemini API key not configured on server' 
      });
    }

    // Validate content before sending to AI
    const validation = validateContent(req.body);
    if (!validation.valid) {
      return res.status(400).json({ 
        error: 'Content policy violation',
        message: `Your request contains prohibited content related to: "${validation.keyword}". Please ensure your project topic is appropriate for academic purposes and does not include explicit, violent, illegal, or other sensitive content.`
      });
    }

    // Add safety instruction to the prompt
    const safetyPrompt = `IMPORTANT: Generate ONLY academic, educational, and professional project topics suitable for university Final Year Projects. Do NOT generate content related to: explicit/adult content, violence, terrorism, illegal activities, hate speech, or any sensitive/controversial topics.\n\n${prompt}`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: safetyPrompt
            }]
          }],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 6000
          },
          safetySettings: [
            {
              category: "HARM_CATEGORY_HARASSMENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_HATE_SPEECH",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_DANGEROUS_CONTENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            }
          ]
        })
      }
    );

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json({ 
        error: error.error?.message || 'Gemini API error' 
      });
    }

    const data = await response.json();
    
    // Check if content was blocked by Gemini's safety filters
    if (data.promptFeedback?.blockReason) {
      return res.status(400).json({
        error: 'Content policy violation',
        message: 'Your request was blocked due to safety concerns. Please ensure your input is appropriate for academic purposes.'
      });
    }
    
    res.json(data);

  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ 
      error: 'Failed to generate topics',
      details: error.message 
    });
  }
});

// Custom timeline generation endpoint
app.post('/api/generate-custom-timeline', async (req, res) => {
  try {
    const { saved_project_id, project_title, project_description, custom_requirements } = req.body;
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
      return res.status(500).json({ 
        error: 'Gemini API key not configured on server' 
      });
    }

    // Validate content before sending to AI
    const validation = validateContent({ 
      project_title, 
      project_description, 
      custom_requirements 
    });
    if (!validation.valid) {
      return res.status(400).json({ 
        error: 'Content policy violation',
        message: `Your project contains prohibited content related to: "${validation.keyword}". Please ensure your project is appropriate for academic purposes and does not include explicit, violent, illegal, or other sensitive content.`
      });
    }

    // Build the AI prompt for timeline generation with safety instruction
    const prompt = `IMPORTANT: Generate ONLY academic, educational, and professional project timelines suitable for university Final Year Projects. Do NOT generate content related to: explicit/adult content, violence, terrorism, illegal activities, hate speech, or any sensitive/controversial topics.

You are a Final Year Project (FYP) advisor helping students create personalized project timelines.

PROJECT DETAILS:
Title: ${project_title}
Description: ${project_description}

${custom_requirements ? `CUSTOM REQUIREMENTS:\n${custom_requirements}\n` : ''}

Generate a comprehensive project timeline with 5-8 phases. Each phase should include:
1. Phase name (e.g., "Research & Literature Review", "System Design", "Development - Backend")
2. Phase description (2-3 sentences explaining what needs to be done)
3. Duration in weeks (realistic estimate)
4. 3-6 specific tasks for this phase

Consider the project complexity, scope, and any custom requirements provided. Make the timeline realistic and achievable for a university FYP (typically 15-20 weeks total).

OUTPUT FORMAT - You must respond with ONLY a valid JSON array, no other text:
[
  {
    "name": "Phase Name",
    "description": "Detailed description of this phase...",
    "duration_weeks": 3,
    "tasks": [
      "Task 1 description",
      "Task 2 description",
      "Task 3 description"
    ]
  }
]

Ensure the JSON is valid with no trailing commas. Output ONLY the JSON array.`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: prompt
            }]
          }],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 4000
          },
          safetySettings: [
            {
              category: "HARM_CATEGORY_HARASSMENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_HATE_SPEECH",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
              category: "HARM_CATEGORY_DANGEROUS_CONTENT",
              threshold: "BLOCK_MEDIUM_AND_ABOVE"
            }
          ]
        })
      }
    );

    if (!response.ok) {
      const error = await response.json();
      return res.status(response.status).json({ 
        error: error.error?.message || 'Gemini API error' 
      });
    }

    const data = await response.json();
    
    // Check if content was blocked by Gemini's safety filters
    if (data.promptFeedback?.blockReason) {
      return res.status(400).json({
        error: 'Content policy violation',
        message: 'Your project was blocked due to safety concerns. Please ensure your project is appropriate for academic purposes.'
      });
    }
    
    // Extract the generated text
    const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text;
    
    if (!generatedText) {
      return res.status(500).json({ error: 'No content generated' });
    }

    // Parse the JSON from the response
    let phases;
    try {
      // Extract JSON array from the response (handle markdown code blocks)
      const jsonMatch = generatedText.match(/\[[\s\S]*\]/);
      if (!jsonMatch) {
        throw new Error('No JSON array found in response');
      }
      phases = JSON.parse(jsonMatch[0]);
    } catch (parseError) {
      console.error('Failed to parse AI response:', generatedText);
      return res.status(500).json({ 
        error: 'Failed to parse AI response',
        details: parseError.message
      });
    }

    // Now save the custom phases to the database via Flask backend
    const flaskResponse = await fetch(
      `http://localhost:5000/api/progress/customize/${saved_project_id}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': req.headers.authorization // Pass through the auth token
        },
        body: JSON.stringify({ phases })
      }
    );

    if (!flaskResponse.ok) {
      const error = await flaskResponse.json();
      return res.status(flaskResponse.status).json({ 
        error: error.message || 'Failed to save custom timeline' 
      });
    }

    const result = await flaskResponse.json();
    res.json(result);

  } catch (error) {
    console.error('Custom timeline generation error:', error);
    res.status(500).json({ 
      error: 'Failed to generate custom timeline',
      details: error.message 
    });
  }
});

// Test endpoint for ScholarAI
app.get('/api/test-scholarai', async (req, res) => {
  try {
    const apiKey = process.env.SCHOLARAI_API_KEY;

    if (!apiKey) {
      return res.json({ 
        status: 'error',
        message: 'ScholarAI API key not configured'
      });
    }

    // Try different parameter combinations
    const testQueries = [
      // Test 1: Minimal parameters
      {
        name: 'Test 1: Minimal',
        params: new URLSearchParams({
          query: 'deep learning'
        })
      },
      // Test 2: With sort
      {
        name: 'Test 2: With sort',
        params: new URLSearchParams({
          query: 'neural networks',
          sort: 'relevance'
        })
      },
      // Test 3: Original format
      {
        name: 'Test 3: Full params',
        params: new URLSearchParams({
          query: 'artificial intelligence',
          sort: 'cited_by_count',
          peer_reviewed_only: 'true',
          offset: '0'
        })
      }
    ];

    const results = [];

    for (const test of testQueries) {
      const apiUrl = `https://api.scholarai.io/api/abstracts?${test.params.toString()}`;
      console.log(`${test.name} - URL:`, apiUrl);

      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'x-scholarai-api-key': apiKey
        }
      });

      const responseText = await response.text();
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        data = responseText;
      }

      results.push({
        test: test.name,
        status: response.status,
        paperCount: Array.isArray(data) ? data.length : 0,
        response: Array.isArray(data) && data.length > 0 ? {
          firstPaper: data[0].title
        } : (typeof data === 'string' ? data.substring(0, 200) : data)
      });
    }

    return res.json({
      status: 'testing',
      message: 'Tested multiple query formats',
      results: results
    });

  } catch (error) {
    console.error('ScholarAI test error:', error);
    return res.json({
      status: 'error',
      message: error.message
    });
  }
});

// ScholarAI proxy endpoint
app.post('/api/search-papers', async (req, res) => {
  try {
    const { query, limit = 5 } = req.body;
    const apiKey = process.env.SCHOLARAI_API_KEY;

    if (!apiKey) {
      console.log('ScholarAI API key not configured, returning mock flag');
      return res.status(200).json({ 
        error: 'ScholarAI API key not configured on server',
        useMock: true 
      });
    }

    // Extract key technical terms for better search
    const stopWords = ['about', 'using', 'with', 'from', 'that', 'this', 'will', 'your', 'have', 'more', 'when', 'what', 'where', 'develop', 'system', 'project', 'application'];
    const keywords = query
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 3 && !stopWords.includes(word))
      .slice(0, 5)
      .join(' ');

    const finalQuery = keywords || query;

    const params = new URLSearchParams({
      query: finalQuery,
      sort: 'cited_by_count',
      peer_reviewed_only: 'true',
      offset: '0'
    });

    const apiUrl = `https://api.scholarai.io/api/abstracts?${params.toString()}`;
    console.log('ScholarAI API request with query:', finalQuery);

    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'x-scholarai-api-key': apiKey
      }
    });

    console.log('ScholarAI API response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('ScholarAI API error:', response.status, errorText);
      
      return res.status(200).json({ 
        error: 'API error',
        useMock: true 
      });
    }

    const data = await response.json();
    
    // ScholarAI returns: { paper_data: [...], total_num_results: N, next_offset: M }
    const papers = data.paper_data || [];
    console.log('ScholarAI API returned:', papers.length, 'papers out of', data.total_num_results || 0, 'total');
    
    if (papers.length === 0) {
      console.log('No papers found, using mock data fallback');
      return res.status(200).json({ 
        error: 'No papers found for this query',
        useMock: true 
      });
    }
    
    // Transform ScholarAI format to our expected format
    const transformedPapers = papers.slice(0, limit).map(paper => ({
      title: paper.title || 'Untitled Paper',
      abstract: paper.answer || 'No abstract available',
      authors: paper.creators || [],
      publication_date: paper.publicationDate || 'N/A',
      cited_by_count: 0,
      url: paper.landing_page_url || '#',
      ss_id: paper.ss_id || null,
      doi: paper.doi || null,
      pdf_url: paper.pdf_id ? paper.pdf_id.replace('PDF_URL:', '') : null
    }));
    
    res.json({ 
      results: transformedPapers,
      totalResults: data.total_num_results || papers.length
    });

  } catch (error) {
    console.error('ScholarAI proxy error:', error);
    res.status(200).json({ 
      error: 'Failed to search papers',
      details: error.message,
      useMock: true 
    });
  }
});

app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}`);
});