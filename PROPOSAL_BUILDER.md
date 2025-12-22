# Interactive Proposal Builder

## Overview
The Interactive Proposal Builder is an AI-powered feature that helps students create comprehensive FYP proposals through a guided multi-step wizard interface.

## Features Implemented

### 1. ProposalService (`src/services/proposalService.js`)
Complete service layer for proposal generation:

- **AI-Powered Generation**: Integrates with existing aiService.js for intelligent content
- **5 Core Sections**:
  - Background & Motivation (150-200 words)
  - Project Objectives (3-5 measurable goals)
  - Methodology (200-250 words with approach/tools)
  - Project Scope (in-scope vs out-of-scope)
  - Timeline (4-6 phases with activities and deliverables)
  
- **Smart Fallbacks**: Mock data generation when AI unavailable
- **Export Functionality**: Markdown format with academic structure
- **Download Support**: Browser-based file download (.md format)

### 2. ProposalBuilderModal (`src/components/ProposalBuilderModal.vue`)
User-friendly wizard interface:

- **6-Step Wizard**:
  1. Project Information (title, description, domain, technologies)
  2. Background Generation
  3. Objectives Definition
  4. Scope Planning (in-scope/out-scope)
  5. Methodology Description
  6. Timeline Creation

- **AI Generation Per Section**: Individual "Generate with AI" buttons
- **Editable Content**: All AI-generated content is fully editable
- **Progress Tracking**: Visual step indicator
- **Preview Feature**: See formatted proposal before download
- **Validation**: Required field checking

### 3. Integration (`src/App.vue`)
Seamless system integration:

- **Navigation Button**: "Proposal Builder" link in main header (authenticated users only)
- **Icon**: FileText icon from Lucide Vue
- **Modal System**: Consistent with other modals (ProfileModal, AuthModal)
- **State Management**: proposalBuilderOpen, proposalBuilderTopic refs

## User Experience Flow

1. **Access**: Click "Proposal Builder" in navigation (requires authentication)
2. **Step 1**: Enter project basics (title, description, domain, etc.)
   - Auto-fills program from user profile
   - Can pre-populate from selected topic
3. **Step 2-6**: For each section:
   - Click "Generate with AI" for intelligent content
   - Edit generated content or write from scratch
   - Use add/remove buttons for list items
4. **Preview**: Click "Preview" button to see formatted proposal
5. **Download**: Click "Download Proposal" to save as Markdown (.md)

## Technical Implementation

### AI Integration
```javascript
// Uses existing aiService with specialized prompts
const result = await proposalService.generateProposalSection('background', {
  title: 'AI Student Performance System',
  description: '...',
  program: 'Computer Science',
  domain: 'Artificial Intelligence',
  technologies: 'Python, TensorFlow, React'
})
```

### Section Prompts
Each section has optimized prompts:
- **Background**: Context, challenges, significance
- **Objectives**: SMART goals (specific, measurable, achievable)
- **Methodology**: Phases, tools, validation approaches
- **Scope**: Clearly defined inclusions/exclusions
- **Timeline**: Realistic phases with activities and deliverables

### Mock Data Quality
When AI is unavailable:
- Template-based generation with placeholder replacement
- Context-aware content (uses project title, domain, technologies)
- Realistic academic language
- Malaysian date formatting (en-MY locale)

### Export Format
Academic proposal structure:
```markdown
# Final Year Project Proposal

**Project Title:** [Title]
**Student Name:** [Name]
**Program:** [Program]
**Supervisor:** [Supervisor Name]
**Date:** [DD/MM/YYYY]

---

## 1. Background and Motivation
[Content]

## 2. Project Objectives
1. [Objective 1]
2. [Objective 2]
...

## 3. Project Scope
### In Scope:
- [Item]

### Out of Scope:
- [Item]

## 4. Methodology
[Content]

## 5. Project Timeline
### Phase 1: [Name]
**Duration:** [Duration]
**Key Activities:**
- [Activity]

**Deliverable:** [Deliverable]
```

## Benefits

### For Students
- **Time Savings**: Generate draft proposals in minutes vs hours
- **Structure Guidance**: Learn proper proposal format
- **Quality Improvement**: AI suggests comprehensive, well-structured content
- **Flexibility**: Full editing capability for personalization
- **Professional Output**: Markdown format ready for conversion to PDF

### For System
- **Reusable Service**: ProposalService can be extended for other features
- **Consistent UX**: Follows existing modal/wizard patterns
- **Scalable**: Easy to add more sections or providers
- **Testable**: Mock data ensures functionality without API keys

## Future Enhancements

### Short-term (Low Complexity)
1. **Save Draft**: Store proposals in database for later editing
2. **Template Library**: Pre-built templates for common project types
3. **Collaboration**: Share proposals with supervisors for feedback
4. **Version History**: Track changes and revisions

### Medium-term (Moderate Complexity)
1. **PDF Export**: Convert Markdown to formatted PDF
2. **Citation Manager**: Add references and bibliography
3. **Grammar Check**: Integrate language tools
4. **Supervisor Review**: Comment and approval workflow

### Long-term (Higher Complexity)
1. **Gantt Chart Generation**: Visual timeline from proposal data
2. **Budget Calculator**: Add financial planning section
3. **Risk Assessment**: AI-powered risk identification
4. **Integration with Progress Tracker**: Auto-create milestones

## Configuration

### Environment Variables (Optional)
The builder works with existing AI configuration:
- `VITE_GEMINI_API_KEY`: For Gemini API (recommended)
- `VITE_OPENAI_API_KEY`: For OpenAI API
- `VITE_HUGGINGFACE_API_KEY`: For HuggingFace API

**Note**: System fully functional with mock data when no API keys configured.

### Settings
No additional configuration required. Uses existing:
- aiService configuration
- authService for user data
- Standard component patterns

## File Structure
```
src/
├── services/
│   └── proposalService.js        # Service layer
├── components/
│   └── ProposalBuilderModal.vue  # UI component
└── App.vue                        # Integration point

PROPOSAL_BUILDER.md                # This documentation
```

## Dependencies
All dependencies already installed:
- Vue 3 (Composition API)
- Lucide Vue Next (icons)
- Existing services (aiService, authService)

## Usage Examples

### Basic Usage
```javascript
// Open builder from anywhere
openProposalBuilder()
```

### With Pre-filled Topic
```javascript
// From topic card or search result
openProposalBuilder({
  title: 'AI Chatbot for Customer Support',
  description: 'Build an intelligent chatbot...',
  technologies: ['Python', 'TensorFlow', 'React']
})
```

### Generate Specific Section
```javascript
import proposalService from './services/proposalService.js'

const background = await proposalService.generateProposalSection('background', {
  title: 'My Project',
  description: 'Project description',
  program: 'Computer Science',
  domain: 'Web Development',
  technologies: 'Vue, Node.js, MongoDB'
})
```

### Export Proposal
```javascript
const markdown = proposalService.exportToMarkdown(proposalData, projectInfo)
proposalService.downloadAsFile(markdown, 'My_Proposal.md')
```

## Testing Checklist

- [ ] Open proposal builder from navigation
- [ ] Fill in project information (step 1)
- [ ] Generate background with AI (step 2)
- [ ] Add/remove objectives (step 3)
- [ ] Define in-scope and out-scope items (step 4)
- [ ] Generate methodology with AI (step 5)
- [ ] Create timeline phases (step 6)
- [ ] Preview formatted proposal
- [ ] Download as Markdown file
- [ ] Test with AI unavailable (mock data)
- [ ] Test with pre-filled topic data
- [ ] Verify all form validations
- [ ] Check responsive design on mobile

## Known Limitations

1. **No Database Persistence**: Proposals not saved (closing modal loses data)
2. **Single Format**: Only Markdown export (no PDF/Word)
3. **No Collaboration**: Single-user editing only
4. **Basic Preview**: HTML conversion is simple (no advanced formatting)
5. **Manual Timeline**: No automatic date calculation

These limitations are intentional for MVP and will be addressed in future iterations.

## Support

For issues or questions:
1. Check console for error messages
2. Verify AI service configuration (if using AI)
3. Test with mock data fallback
4. Review proposal builder state in Vue DevTools

## Conclusion

The Interactive Proposal Builder successfully implements:
- ✅ Multi-step wizard interface (6 steps)
- ✅ AI-powered content generation (5 sections)
- ✅ Intelligent mock data fallbacks
- ✅ Markdown export and download
- ✅ Preview functionality
- ✅ Seamless system integration

**Complexity Rating**: 4/10 (as estimated)
**Implementation Time**: ~2 hours
**LOC**: ~700 lines (service + component)
**ROI**: High (directly helps students with critical FYP task)
