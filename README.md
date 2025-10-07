# FYP Guidance System

A modern, AI-powered Final Year Project Research and Guidance System built with Vue.js and Tailwind CSS. This single-page application helps students discover personalized project topics and access relevant resources for their final year projects.

## Features

-  **AI-Powered Topic Generation**: Intelligent suggestions using OpenAI GPT, Google Gemini, or Hugging Face
-  **Personalized Recommendations**: Based on student profile, skills, and interests
-  **Comprehensive Form**: Detailed input form covering skills, interests, and project requirements
-  **Resource Library**: Curated collection of academic papers, tools, and learning materials
-  **Modern UI/UX**: Beautiful, responsive design with smooth animations
-  **Mobile-First**: Fully responsive design that works on all devices
-  **Fast & Lightweight**: Built with Vue 3 and Vite for optimal performance
-  **Flexible AI Integration**: Support for multiple AI providers with fallback to mock data

## Technology Stack

- **Frontend**: Vue.js 3 (Composition API)
- **Styling**: Tailwind CSS
- **Icons**: Lucide Vue Next
- **Build Tool**: Vite
- **Package Manager**: npm

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fyp-guidance-system
```

2. Install dependencies:
```bash
npm install
```

3. Configure AI services (optional but recommended):
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your API keys
# VITE_OPENAI_API_KEY=your_openai_api_key_here
# VITE_GEMINI_API_KEY=your_gemini_api_key_here
# VITE_HUGGINGFACE_API_KEY=your_huggingface_token_here
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── components/
│   ├── FYPForm.vue          # Main input form component
│   ├── FYPResults.vue       # Results display component
│   └── FYPResources.vue     # Resources library component
├── App.vue                  # Main application component
├── main.js                  # Application entry point
└── style.css               # Global styles and Tailwind imports
```

## Key Components

### FYPForm.vue
- Comprehensive form with all necessary fields for project generation
- Input validation and user-friendly interface
- Skills and interests selection with checkboxes
- Project preferences and constraints

### FYPResults.vue
- Displays AI-generated project topics
- Shows project details, required skills, and resources
- Interactive cards with hover effects
- Loading states and empty states

### FYPResources.vue
- Curated collection of academic resources
- Development tools and learning materials
- Quick access links and success tips
- Organized by categories for easy navigation

## Customization

### Styling
The application uses Tailwind CSS with custom configuration. You can modify:
- Colors in `tailwind.config.js`
- Custom components in `src/style.css`
- Component-specific styles in individual Vue files

### Content
- Update form options in `FYPForm.vue`
- Modify mock data in `App.vue`
- Add new resources in `FYPResources.vue`

## Features in Detail

### Form Input Fields
- Personal information (name, student ID)
- Academic details (program, year)
- Technical skills selection
- Areas of interest
- Project preferences (difficulty, duration, type)
- Additional requirements and constraints
- Supervisor and budget information

### Generated Results
- Project title and description
- Difficulty level and duration
- Required skills and technologies
- Recommended resources
- Project categories and tags
- Action buttons for further interaction

### Resource Categories
- **Academic Resources**: Research papers, journals, databases
- **Development Tools**: Frameworks, libraries, environments
- **Learning Materials**: Tutorials, courses, documentation

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## AI Integration

The system supports multiple AI providers for topic generation:

### OpenAI GPT (Recommended)
- **Setup**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Cost**: ~$0.001-0.002 per topic generation
- **Quality**: High-quality, contextually relevant topics

### Google Gemini (Alternative)
- **Setup**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Cost**: Competitive pricing
- **Quality**: Good performance with recent model updates

### Hugging Face (Free Option)
- **Setup**: Get token from [Hugging Face](https://huggingface.co/settings/tokens)
- **Cost**: Free tier available with rate limits
- **Quality**: Good for development and testing

### Fallback Mode
- If no AI service is configured, the system uses intelligent mock data
- Topics are still personalized based on form inputs
- Perfect for development and demonstration purposes

## Future Enhancements

- [x] AI integration for topic generation
- [ ] User authentication and project saving
- [ ] Advanced filtering and search
- [ ] Progress tracking and timeline management
- [ ] Supervisor dashboard
- [ ] Export functionality for project proposals
- [ ] Integration with academic databases
- [ ] Mobile app version
- [ ] Real-time collaboration features
- [ ] Advanced AI prompt customization

## Support

For support or questions, please open an issue in the repository or contact the development team.
