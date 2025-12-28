import aiService from './aiService.js'
import { jsPDF } from 'jspdf'

class ProposalService {
  constructor() {
    this.mockTemplates = {
      background: [
        "The rapid evolution of {topic} has created significant challenges in {domain}. Current solutions often lack {limitation}, creating opportunities for innovative approaches.",
        "In recent years, {topic} has gained prominence due to {trend}. However, existing implementations face challenges in {problem_area}, necessitating new research directions.",
        "The integration of {topic} in {domain} represents a critical area of study. This project addresses the gap in {specific_area} through innovative application of {technology}."
      ],
      objectives: [
        "To design and implement a {solution_type} that addresses {problem}",
        "To investigate the effectiveness of {approach} in solving {challenge}",
        "To develop a novel {system_type} capable of {capability}"
      ],
      methodology: [
        "This project will follow an iterative development approach, beginning with requirements analysis and system design. The implementation will utilize {technology_stack}, with regular testing and refinement cycles.",
        "The research methodology combines {method1} and {method2} approaches. Data will be collected through {data_source}, analyzed using {tool}, and validated against {benchmark}.",
        "Development will proceed in phases: (1) Literature review and requirement gathering, (2) System architecture design, (3) Implementation and testing, (4) Evaluation and documentation."
      ]
    }
  }

  async generateProposalSection(sectionType, projectData) {
    const prompt = this.buildSectionPrompt(sectionType, projectData)
    
    try {
      if (aiService.isConfigured()) {
        const response = await aiService.generateWithCustomPrompt(prompt)
        return this.parseSectionResponse(response, sectionType)
      } else {
        console.log(`AI not configured, using mock data for ${sectionType}`)
        return this.generateMockSection(sectionType, projectData)
      }
    } catch (error) {
      console.warn(`AI generation failed for ${sectionType}, falling back to mock data:`, error.message)
      return this.generateMockSection(sectionType, projectData)
    }
  }

  buildSectionPrompt(sectionType, projectData) {
    const { title, description, program, domain, technologies } = projectData
    
    const prompts = {
      background: `Generate a comprehensive background section (150-200 words) for a final year project titled "${title}".
        
Project Context:
- Program: ${program}
- Domain: ${domain}
- Description: ${description}
- Technologies: ${technologies}

The background should:
1. Explain the context and significance of the problem
2. Highlight current challenges or limitations
3. Justify why this project is needed
4. Reference relevant trends or technologies

Provide only the background text, no additional formatting.`,

      objectives: `Generate 3-5 specific, measurable objectives for a final year project titled "${title}".

Project Context:
- Description: ${description}
- Domain: ${domain}
- Technologies: ${technologies}

Each objective should:
- Start with an action verb (develop, implement, analyze, evaluate)
- Be specific and measurable
- Be achievable within an academic semester
- Contribute to the overall project goal

Format: Return as a JSON array of strings. Example: ["Objective 1", "Objective 2", "Objective 3"]`,

      methodology: `Generate a detailed methodology section (200-250 words) for a final year project titled "${title}".

Project Context:
- Description: ${description}
- Program: ${program}
- Technologies: ${technologies}

The methodology should include:
1. Overall approach (Agile, Waterfall, Research-based, etc.)
2. Key phases or stages
3. Tools and technologies to be used
4. Data collection/analysis methods (if applicable)
5. Testing and validation strategy

Provide only the methodology text, no additional formatting.`,

      scope: `Define the scope for a final year project titled "${title}".

Project Context:
- Description: ${description}
- Domain: ${domain}

Generate two sections:
1. IN SCOPE: What will be included (3-5 bullet points)
2. OUT OF SCOPE: What will be excluded (3-5 bullet points)

Format as JSON:
{
  "inScope": ["item 1", "item 2", "item 3"],
  "outScope": ["item 1", "item 2", "item 3"]
}`,

      timeline: `Generate a realistic project timeline for "${title}" spanning 12-16 weeks.

Project Context:
- Description: ${description}
- Technologies: ${technologies}

Format as JSON array with phases:
[
  {
    "phase": "Phase name",
    "duration": "X weeks",
    "activities": ["activity 1", "activity 2"],
    "deliverable": "Key deliverable"
  }
]

Include 4-6 phases covering: Research, Design, Implementation, Testing, Documentation.`
    }

    return prompts[sectionType] || ''
  }

  parseSectionResponse(response, sectionType) {
    if (!response) {
      throw new Error('Empty AI response')
    }

    // Handle both array format (from old API) and direct string format
    let content = ''
    if (typeof response === 'string') {
      content = response
    } else if (Array.isArray(response) && response.length > 0) {
      content = response[0]?.text || response[0]?.content || JSON.stringify(response)
    } else {
      content = JSON.stringify(response)
    }

    if (sectionType === 'objectives' || sectionType === 'scope' || sectionType === 'timeline') {
      // Extract JSON from response
      const jsonMatch = content.match(/\{[\s\S]*\}|\[[\s\S]*\]/)
      if (jsonMatch) {
        try {
          return JSON.parse(jsonMatch[0])
        } catch (e) {
          throw new Error('Failed to parse JSON response')
        }
      }
    }

    // For text sections (background, methodology)
    return content.trim()
  }

  generateMockSection(sectionType, projectData) {
    const { title, description, program, domain, technologies = 'modern technologies' } = projectData

    const replacements = {
      topic: title || 'the proposed system',
      domain: domain || 'the field',
      problem: description || 'current challenges',
      technology: technologies.split(',')[0]?.trim() || 'technology',
      program: program || 'the program',
      limitation: 'efficiency and scalability',
      trend: 'technological advancements',
      problem_area: 'integration and deployment',
      specific_area: 'practical applications',
      solution_type: 'solution',
      approach: 'proposed methodology',
      challenge: 'identified challenges',
      system_type: 'system',
      capability: 'enhanced functionality',
      technology_stack: technologies || 'modern development tools',
      method1: 'qualitative',
      method2: 'quantitative',
      data_source: 'user studies and existing systems',
      tool: 'analytical frameworks',
      benchmark: 'industry standards'
    }

    if (sectionType === 'background') {
      let template = this.mockTemplates.background[Math.floor(Math.random() * this.mockTemplates.background.length)]
      Object.entries(replacements).forEach(([key, value]) => {
        template = template.replace(new RegExp(`\\{${key}\\}`, 'g'), value)
      })
      return template
    }

    if (sectionType === 'objectives') {
      return [
        `To design and implement a ${replacements.topic} system that addresses key challenges in ${replacements.domain}`,
        `To evaluate the effectiveness and performance of the proposed solution`,
        `To compare the developed system with existing approaches in ${replacements.domain}`,
        `To document the development process and create comprehensive user documentation`
      ]
    }

    if (sectionType === 'methodology') {
      return `This project will follow an Agile development methodology with iterative sprints. The implementation will utilize ${replacements.technology} and related tools. Development will proceed through phases including requirements analysis, system design, implementation, testing, and deployment. Regular evaluations will ensure the system meets specified objectives and quality standards.`
    }

    if (sectionType === 'scope') {
      return {
        inScope: [
          `Core ${replacements.topic} functionality`,
          `User interface design and implementation`,
          `Basic testing and validation`,
          `Documentation and user guides`
        ],
        outScope: [
          `Advanced enterprise features`,
          `Large-scale deployment`,
          `Commercial licensing considerations`,
          `Long-term maintenance and support`
        ]
      }
    }

    if (sectionType === 'timeline') {
      return [
        {
          phase: 'Research & Planning',
          duration: '2-3 weeks',
          activities: ['Literature review', 'Requirements gathering', 'Technology selection'],
          deliverable: 'Project proposal and requirements document'
        },
        {
          phase: 'Design',
          duration: '2-3 weeks',
          activities: ['System architecture design', 'Database schema design', 'UI/UX wireframes'],
          deliverable: 'Design specifications and mockups'
        },
        {
          phase: 'Implementation',
          duration: '4-6 weeks',
          activities: ['Core functionality development', 'Frontend development', 'Backend integration'],
          deliverable: 'Working prototype'
        },
        {
          phase: 'Testing & Refinement',
          duration: '2-3 weeks',
          activities: ['Unit testing', 'Integration testing', 'User acceptance testing', 'Bug fixes'],
          deliverable: 'Tested and validated system'
        },
        {
          phase: 'Documentation & Finalization',
          duration: '2 weeks',
          activities: ['Technical documentation', 'User manual creation', 'Final presentation preparation'],
          deliverable: 'Complete project documentation'
        }
      ]
    }

    return ''
  }

  async generateCompleteProposal(projectData) {
    const sections = ['background', 'objectives', 'methodology', 'scope', 'timeline']
    const proposal = {}

    for (const section of sections) {
      proposal[section] = await this.generateProposalSection(section, projectData)
    }

    return proposal
  }

  exportToMarkdown(proposalData, projectInfo) {
    const { title, studentName, program, supervisor = 'To be assigned' } = projectInfo
    const date = new Date().toLocaleDateString('en-MY', { year: 'numeric', month: 'long', day: 'numeric' })

    let markdown = `# Final Year Project Proposal\n\n`
    markdown += `**Title:** ${title}\n\n`
    markdown += `**Student:** ${studentName}\n\n`
    markdown += `**Program:** ${program}\n\n`
    markdown += `**Supervisor:** ${supervisor}\n\n`
    markdown += `**Date:** ${date}\n\n`
    markdown += `---\n\n`

    markdown += `## 1. Background and Motivation\n\n${proposalData.background}\n\n`
    
    markdown += `## 2. Objectives\n\n`
    if (Array.isArray(proposalData.objectives)) {
      proposalData.objectives.forEach((obj, idx) => {
        markdown += `${idx + 1}. ${obj}\n`
      })
    }
    markdown += `\n`

    markdown += `## 3. Scope\n\n`
    markdown += `### In Scope\n`
    proposalData.scope?.inScope?.forEach(item => markdown += `- ${item}\n`)
    markdown += `\n### Out of Scope\n`
    proposalData.scope?.outScope?.forEach(item => markdown += `- ${item}\n`)
    markdown += `\n`

    markdown += `## 4. Methodology\n\n${proposalData.methodology}\n\n`

    markdown += `## 5. Project Timeline\n\n`
    if (Array.isArray(proposalData.timeline)) {
      proposalData.timeline.forEach((phase, idx) => {
        markdown += `### ${idx + 1}. ${phase.phase} (${phase.duration})\n`
        markdown += `**Activities:**\n`
        phase.activities?.forEach(act => markdown += `- ${act}\n`)
        markdown += `\n**Deliverable:** ${phase.deliverable}\n\n`
      })
    }

    return markdown
  }

  exportToPDF(proposalData, projectInfo) {
    const { title, studentName, program, supervisor = 'To be assigned' } = projectInfo
    const date = new Date().toLocaleDateString('en-MY', { year: 'numeric', month: 'long', day: 'numeric' })

    // Create new PDF document
    const doc = new jsPDF()
    
    // Set font sizes
    const titleSize = 20
    const headingSize = 16
    const subheadingSize = 12
    const normalSize = 10
    
    let yPosition = 20
    const pageWidth = doc.internal.pageSize.width
    const margin = 20
    const maxWidth = pageWidth - 2 * margin

    // Helper function to add text with automatic page breaks
    const addText = (text, fontSize, isBold = false, align = 'left') => {
      doc.setFontSize(fontSize)
      doc.setFont('helvetica', isBold ? 'bold' : 'normal')
      
      if (align === 'center') {
        doc.text(text, pageWidth / 2, yPosition, { align: 'center' })
        yPosition += fontSize / 2 + 2
      } else {
        const lines = doc.splitTextToSize(text, maxWidth)
        lines.forEach(line => {
          if (yPosition > 270) {
            doc.addPage()
            yPosition = 20
          }
          doc.text(line, margin, yPosition)
          yPosition += fontSize / 2 + 2
        })
      }
    }

    const addSpace = (space = 5) => {
      yPosition += space
    }

    // Title Page
    doc.setFontSize(titleSize)
    doc.setFont('helvetica', 'bold')
    yPosition = 60
    doc.text('Final Year Project Proposal', pageWidth / 2, yPosition, { align: 'center' })
    
    addSpace(20)
    doc.setFontSize(headingSize)
    doc.text(title, pageWidth / 2, yPosition, { align: 'center', maxWidth: maxWidth })
    
    addSpace(40)
    doc.setFontSize(normalSize)
    doc.setFont('helvetica', 'normal')
    
    // Project Info
    const infoY = 140
    doc.setFont('helvetica', 'bold')
    doc.text('Student:', margin, infoY)
    doc.setFont('helvetica', 'normal')
    doc.text(studentName, margin + 30, infoY)
    
    doc.setFont('helvetica', 'bold')
    doc.text('Program:', margin, infoY + 10)
    doc.setFont('helvetica', 'normal')
    doc.text(program, margin + 30, infoY + 10)
    
    doc.setFont('helvetica', 'bold')
    doc.text('Supervisor:', margin, infoY + 20)
    doc.setFont('helvetica', 'normal')
    doc.text(supervisor, margin + 30, infoY + 20)
    
    doc.setFont('helvetica', 'bold')
    doc.text('Date:', margin, infoY + 30)
    doc.setFont('helvetica', 'normal')
    doc.text(date, margin + 30, infoY + 30)

    // New page for content
    doc.addPage()
    yPosition = 20

    // 1. Background and Motivation
    addText('1. Background and Motivation', headingSize, true)
    addSpace(5)
    addText(proposalData.background, normalSize, false)
    addSpace(10)

    // 2. Objectives
    addText('2. Objectives', headingSize, true)
    addSpace(5)
    if (Array.isArray(proposalData.objectives)) {
      proposalData.objectives.forEach((obj, idx) => {
        addText(`${idx + 1}. ${obj}`, normalSize, false)
        addSpace(3)
      })
    }
    addSpace(10)

    // 3. Scope
    addText('3. Scope', headingSize, true)
    addSpace(5)
    
    addText('In Scope', subheadingSize, true)
    addSpace(3)
    if (proposalData.scope?.inScope) {
      proposalData.scope.inScope.forEach(item => {
        addText(`• ${item}`, normalSize, false)
        addSpace(2)
      })
    }
    addSpace(5)
    
    addText('Out of Scope', subheadingSize, true)
    addSpace(3)
    if (proposalData.scope?.outScope) {
      proposalData.scope.outScope.forEach(item => {
        addText(`• ${item}`, normalSize, false)
        addSpace(2)
      })
    }
    addSpace(10)

    // 4. Methodology
    addText('4. Methodology', headingSize, true)
    addSpace(5)
    addText(proposalData.methodology, normalSize, false)
    addSpace(10)

    // 5. Project Timeline
    addText('5. Project Timeline', headingSize, true)
    addSpace(5)
    if (Array.isArray(proposalData.timeline)) {
      proposalData.timeline.forEach((phase, idx) => {
        // Check if we need a new page
        if (yPosition > 240) {
          doc.addPage()
          yPosition = 20
        }
        
        addText(`${idx + 1}. ${phase.phase} (${phase.duration})`, subheadingSize, true)
        addSpace(3)
        
        doc.setFontSize(normalSize)
        doc.setFont('helvetica', 'bold')
        if (yPosition > 270) {
          doc.addPage()
          yPosition = 20
        }
        doc.text('Activities:', margin, yPosition)
        yPosition += normalSize / 2 + 2
        
        doc.setFont('helvetica', 'normal')
        if (phase.activities) {
          phase.activities.forEach(act => {
            addText(`• ${act}`, normalSize, false)
            addSpace(2)
          })
        }
        
        addSpace(3)
        doc.setFont('helvetica', 'bold')
        if (yPosition > 270) {
          doc.addPage()
          yPosition = 20
        }
        doc.text(`Deliverable: `, margin, yPosition)
        doc.setFont('helvetica', 'normal')
        const deliverableText = doc.splitTextToSize(phase.deliverable, maxWidth - 35)
        doc.text(deliverableText, margin + 35, yPosition)
        yPosition += (deliverableText.length * (normalSize / 2 + 2))
        
        addSpace(8)
      })
    }

    return doc
  }

  downloadAsFile(content, filename, type = 'text/markdown') {
    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }
}

export default new ProposalService()
