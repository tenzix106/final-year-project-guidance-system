# FYP Guidance System - AI Coding Agent Instructions

## Architecture Overview

This is a **hybrid full-stack application** with **two separate backend implementations** coexisting:

- **Frontend**: Vue 3 (Composition API) + Tailwind CSS + Vite (port 3000)
- **Backend Option 1**: Express.js proxy server (`backend/`) - handles AI API calls (port 3001)
- **Backend Option 2**: Flask API server (`backend_flask/`) - handles auth + database + AI (port 5000)

**Key Insight**: The system gracefully degrades to mock data when AI services aren't configured, making it fully functional without API keys.

## Project Structure Patterns

### Frontend Architecture (`src/`)
- **Single Page Application** with Vue 3 Composition API
- **Services Pattern**: `src/services/` contains reusable API clients
- **Component Composition**: Large components broken into logical UI sections
- **Smart Fallbacks**: All AI features have mock data equivalents

### Backend Duality
- **`backend/`**: Minimal Express proxy for Gemini API (CORS bypass)
- **`backend_flask/`**: Full Flask app with SQLAlchemy, JWT auth, migrations

### AI Service Integration (`src/services/aiService.js`)
```javascript
// Multi-provider pattern with graceful degradation
this.provider = 'gemini' // Switch between 'openai', 'gemini', 'huggingface'
// Falls back to intelligent mock data when unconfigured
```

## Development Workflows

### Frontend Development
```bash
npm run dev  # Vite dev server on port 3000
npm run build && npm run preview  # Production build testing
```

### Backend Development (Choose One)
```bash
# Express proxy (backend/)
cd backend && npm run dev  # Port 3001

# Flask API (backend_flask/)
cd backend_flask && flask --app wsgi run --debug  # Port 5000
```

### Environment Configuration
- **Frontend**: `.env` with `VITE_*` prefixed variables
- **Backend**: `.env.example` templates in both backend directories
- **AI APIs**: Gemini (primary), OpenAI, HuggingFace support

## Key Conventions

### Vue Component Structure
```vue
<script setup>
// Composition API pattern throughout
import { ref, onMounted } from 'vue'
// Services imported for reusability
import aiService from './services/aiService.js'
</script>
```

### Tailwind Usage
- Custom color system: `primary-*` and `secondary-*` scales
- Custom animations: `animate-fade-in`, `animate-slide-up`
- Component classes: `.btn-primary`, `.btn-secondary`, `.card`

### Error Handling Pattern
```javascript
try {
  if (useAI.value && aiService.isConfigured()) {
    // AI generation
  } else {
    // Fallback to mock data
  }
} catch (error) {
  // Always fallback to mock data on error
}
```

## Database & Migrations (Flask)

### Flask-SQLAlchemy Pattern
```python
# Simple User model with bcrypt password hashing
class User(db.Model):
    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
```

### Migration Commands
```bash
flask --app wsgi db init      # Initialize migrations
flask --app wsgi db migrate   # Create migration
flask --app wsgi db upgrade   # Apply migrations
```

## AI Integration Specifics

### Prompt Engineering Pattern
- **Structured prompts** with student profile section
- **JSON output format** specification in prompts
- **Fallback mock data** generation based on form inputs

### Multi-Provider Support
- **Gemini**: Primary provider via Flask backend (avoids CORS)
- **OpenAI**: Direct frontend integration
- **HuggingFace**: Free tier option with custom parsing

### Response Parsing
```javascript
// Robust JSON extraction from AI responses
const jsonMatch = content.match(/\[[\s\S]*\]/)
// Handles markdown code fences and trailing commas
```

## Development Context

### Technology Choices
- **Vue 3 Composition API**: Modern reactive programming
- **Tailwind CSS**: Utility-first styling with custom design system
- **Vite**: Fast build tool with HMR
- **Flask**: Lightweight Python backend with JWT auth
- **SQLite**: Default database for development simplicity

### Project-Specific Patterns
- **Mock data intelligence**: Generates relevant topics based on user program/interests
- **Responsive design**: Mobile-first approach with smooth animations
- **Modular components**: Each major feature is a separate Vue component
- **Environment flexibility**: Works with or without AI API configuration

## Common Tasks

### Adding New AI Providers
1. Add configuration to `aiService.js` constructor
2. Implement `generateWith[Provider]` method
3. Add parsing logic for provider-specific response format
4. Update `isConfigured()` method

### Extending Backend APIs
- **Flask**: Add blueprints in `app/[feature]/routes.py`
- **Express**: Add routes in `server.js`

### Database Changes
```bash
# After model changes in models.py
flask --app wsgi db migrate -m "description"
flask --app wsgi db upgrade
```

### Frontend Component Development
- Follow existing patterns in `components/` directory
- Use Composition API with `<script setup>`
- Implement responsive design with Tailwind utilities
- Include loading states and error handling