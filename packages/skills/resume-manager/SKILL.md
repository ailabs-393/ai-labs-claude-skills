---
name: resume-manager
description: This skill should be used whenever users need help with resume creation, updating professional profiles, tracking career experiences, managing projects portfolio, or generating tailored resumes for job applications. On first use, extracts data from user's existing resume and maintains a structured database of experiences, projects, education, and skills. Generates professionally styled one-page PDF resumes customized for specific job roles by selecting only the most relevant information from the database.
---

# Resume Manager

## Overview

This skill transforms Claude into a comprehensive resume management system that maintains a structured database of your professional profile and generates tailored, professionally styled PDF resumes for specific job applications. The skill intelligently selects and highlights the most relevant experiences, projects, and skills based on the target role.

## When to Use This Skill

Invoke this skill for resume-related tasks:
- Creating tailored resumes for job applications
- Updating professional experiences and projects
- Managing skills and certifications
- Tracking career progression
- Generating role-specific resumes
- Maintaining a comprehensive career portfolio
- Optimizing resume content for ATS systems

## Workflow

### Step 1: Check for Existing Data

Before any resume operations, check if the database is initialized:

```bash
python3 scripts/resume_db.py is_initialized
```

If output is "false", proceed to Step 2 (Initial Setup). If "true", proceed to Step 3 (Resume Operations).

### Step 2: Initial Setup - Extract from Existing Resume

When no data exists, ask the user to provide their existing resume.

**Prompt the User:**

```
To help you create tailored resumes, I need to build a database of your professional
profile. Please provide your existing resume in one of these ways:

1. Upload your resume file (PDF, DOCX, or TXT)
2. Paste the content of your resume
3. Provide a link to your online resume/LinkedIn profile

I'll extract all the information and organize it in a structured database that I can
use to generate customized resumes for different job applications.
```

**Extracting Data from Resume:**

Once the user provides their resume, extract the following information:

**1. Personal Information:**
- Full name
- Email address
- Phone number
- Location (city, state/country)
- LinkedIn profile URL
- GitHub profile URL
- Personal website
- Professional summary/objective

**2. Work Experience:**
For each role, extract:
- Position/Job title
- Company name
- Location
- Start date (format: "Mon YYYY" like "Jan 2022")
- End date (or "Present")
- Brief description
- Key highlights/achievements (bullet points)
- Technologies/tools used

**3. Projects:**
For each project, extract:
- Project name
- Date or time period
- Description
- Key highlights/achievements
- Technologies used
- Link (if available)

**4. Education:**
For each degree, extract:
- Degree name (e.g., "Bachelor of Science in Computer Science")
- School/University name
- Location
- Graduation date
- GPA (if mentioned)
- Honors (if any)
- Relevant coursework

**5. Skills:**
Extract and categorize skills:
- Programming Languages
- Frameworks & Libraries
- Tools & Technologies
- Practices & Methodologies
- Soft skills

**6. Additional Sections:**
- Certifications (name, issuer, date)
- Awards & Honors
- Publications
- Volunteer work
- Languages spoken

**Saving the Extracted Data:**

After extraction, save to the database using Python:

```python
import sys
import json
sys.path.append('[SKILL_DIR]/scripts')
from resume_db import initialize_from_data

resume_data = {
    "personal_info": {
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "+1 (555) 123-4567",
        "location": "City, State",
        "linkedin": "linkedin.com/in/username",
        "github": "github.com/username",
        "website": "website.com",
        "summary": "Professional summary..."
    },
    "experiences": [
        {
            "position": "Senior Software Engineer",
            "company": "Company Name",
            "location": "City, State",
            "start_date": "Jan 2022",
            "end_date": "Present",
            "description": "Brief description",
            "highlights": [
                "Achievement 1 with quantifiable results",
                "Achievement 2 with impact metrics",
                "Achievement 3 with technologies used"
            ],
            "technologies": ["Python", "AWS", "Docker"]
        }
    ],
    "projects": [
        {
            "name": "Project Name",
            "date": "2023",
            "description": "Project description",
            "highlights": [
                "Key achievement or feature",
                "Impact or result"
            ],
            "technologies": ["React", "Node.js", "PostgreSQL"],
            "link": "github.com/username/project"
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "school": "University Name",
            "location": "City, State",
            "graduation_date": "May 2019",
            "gpa": "3.8/4.0",
            "honors": "Magna Cum Laude",
            "relevant_coursework": ["Data Structures", "Algorithms", "Machine Learning"]
        }
    ],
    "skills": {
        "Languages": ["Python", "JavaScript", "Java"],
        "Frameworks": ["React", "Django", "Spring"],
        "Tools": ["Docker", "AWS", "Git"],
        "Practices": ["Agile", "CI/CD", "TDD"]
    },
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect",
            "issuer": "Amazon Web Services",
            "date": "2023"
        }
    ],
    "awards": [],
    "publications": [],
    "volunteer": [],
    "languages": ["English (Native)", "Spanish (Fluent)"],
    "interests": []
}

initialize_from_data(resume_data)
```

Replace `[SKILL_DIR]` with the actual skill directory path.

**Confirmation:**

```
Perfect! I've extracted and saved your professional profile:

• Personal Information: ✓
• Work Experience: X positions
• Projects: X projects
• Education: X degrees
• Skills: X categories
• Certifications: X certifications

Your resume database is now ready. I can generate customized resumes for any job
you're applying to. Just tell me the job title or description, and I'll create a
tailored one-page PDF highlighting your most relevant experience and skills.
```

### Step 3: Generate Tailored Resume for Job Application

When a user requests a resume for a specific role:

**Step 3.1: Understand the Target Role**

Ask the user about the role:
```
To create the perfect resume for this position, I need to understand the role better.

1. What's the job title?
2. Can you share the job description or key requirements?
3. What are the must-have skills or technologies mentioned?
```

**Step 3.2: Extract Keywords and Requirements**

From the job description, identify:
- Required technical skills
- Preferred technologies
- Key responsibilities
- Important keywords for ATS
- Industry-specific terms
- Experience level indicators

**Step 3.3: Generate Tailored Resume**

Use the PDF generator to create a customized resume:

```python
import sys
sys.path.append('[SKILL_DIR]/scripts')
from pdf_generator import generate_resume

# Keywords from job description
job_keywords = [
    "python", "aws", "kubernetes", "microservices",
    "agile", "rest api", "postgresql", "docker"
]

job_title = "Senior Backend Engineer"

# Output path
output_path = f"~/Downloads/{job_title.replace(' ', '_')}_Resume.pdf"

# Generate resume
generate_resume(
    output_path=output_path,
    job_title=job_title,
    job_keywords=job_keywords
)
```

The generator will:
- Filter experiences relevant to the keywords
- Select projects that match the role
- Highlight applicable skills
- Keep it to one page
- Use professional styling
- Optimize for ATS parsing

**Step 3.4: Review and Iterate**

After generating:
1. Inform the user where the PDF was saved
2. Offer to make adjustments
3. Suggest additional highlights if space allows
4. Recommend customizations for specific requirements

### Step 4: Update Resume Database

When users want to add or update information:

**Adding New Experience:**

```python
from resume_db import add_experience

new_exp = {
    "position": "Lead Software Engineer",
    "company": "New Company",
    "location": "Remote",
    "start_date": "Mar 2024",
    "end_date": "Present",
    "description": "Leading backend infrastructure team",
    "highlights": [
        "Scaled services to handle 50M+ daily requests",
        "Reduced infrastructure costs by 30% through optimization",
        "Built CI/CD pipeline improving deployment speed by 10x"
    ],
    "technologies": ["Go", "Kubernetes", "PostgreSQL", "AWS"]
}

add_experience(new_exp)
```

**Adding New Project:**

```python
from resume_db import add_project

new_project = {
    "name": "Real-time Analytics Dashboard",
    "date": "2024",
    "description": "Built real-time analytics platform processing 1M+ events/minute",
    "highlights": [
        "Implemented using streaming architecture with Kafka and Redis",
        "Created interactive visualizations with React and D3.js",
        "Achieved sub-second query latency on complex aggregations"
    ],
    "technologies": ["React", "Kafka", "Redis", "Python", "TimescaleDB"],
    "link": "github.com/username/analytics-dashboard"
}

add_project(new_project)
```

**Updating Skills:**

```python
from resume_db import add_skill, update_skills

# Add individual skill
add_skill("Languages", "Rust")
add_skill("Tools", "Terraform")

# Or update entire skills dictionary
skills = {
    "Languages": ["Python", "Go", "JavaScript", "Rust", "SQL"],
    "Frameworks": ["Django", "FastAPI", "React", "Next.js"],
    "Cloud & DevOps": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD"],
    "Databases": ["PostgreSQL", "MongoDB", "Redis", "Elasticsearch"],
    "Practices": ["Microservices", "TDD", "Agile", "System Design"]
}

update_skills(skills)
```

**Adding Certification:**

```python
from resume_db import add_certification

cert = {
    "name": "Google Cloud Professional Architect",
    "issuer": "Google Cloud",
    "date": "2024",
    "credential_id": "ABC123",
    "link": "credentials.google.com/..."
}

add_certification(cert)
```

### Step 5: View and Manage Resume Data

**View Summary:**

```bash
python3 scripts/resume_db.py summary
```

**View Specific Sections:**

```bash
# Personal info
python3 scripts/resume_db.py get_personal_info

# All experiences
python3 scripts/resume_db.py get_experiences

# All projects
python3 scripts/resume_db.py get_projects

# Education
python3 scripts/resume_db.py get_education

# Skills
python3 scripts/resume_db.py get_skills
```

**Search Across All Data:**

```bash
python3 scripts/resume_db.py search "machine learning"
```

**Export All Data:**

```bash
python3 scripts/resume_db.py export > resume_backup.json
```

### Step 6: Resume Optimization Tips

When generating resumes, provide these optimization tips:

**Content Optimization:**
- Use action verbs (Led, Built, Architected, Improved, Reduced)
- Include quantifiable metrics (X% improvement, Y users, Z revenue)
- Tailor highlights to match job requirements
- Keep bullet points concise (1-2 lines max)
- Focus on impact, not just responsibilities

**ATS Optimization:**
- Use standard section headers (Experience, Education, Skills)
- Include keywords from job description naturally
- Avoid tables, columns, headers/footers
- Use standard fonts (which the PDF generator does)
- Spell out acronyms once: "Application Programming Interface (API)"

**One-Page Strategy:**
- Prioritize recent and relevant experience (last 5-7 years)
- Include 3-4 bullet points per role
- Limit to 2-3 projects maximum
- Condense older or less relevant experience
- Remove outdated technologies unless specifically required

## Best Practices

1. **Keep Data Current**
   - Update experiences as projects complete
   - Add new skills as you learn them
   - Maintain quantifiable achievements
   - Record certifications immediately

2. **Write Effective Bullet Points**
   - Start with action verbs
   - Include metrics and outcomes
   - Show progression and impact
   - Use the STAR method (Situation, Task, Action, Result)

3. **Organize Skills Strategically**
   - Group by category for clarity
   - Put most relevant skills first
   - Remove outdated technologies
   - Be honest about proficiency levels

4. **Tailor Every Resume**
   - Match keywords to job description
   - Emphasize relevant experience
   - Reorder bullet points by relevance
   - Adjust technical skills section

5. **Maintain Professional Tone**
   - Use third-person implied (no "I")
   - Keep language concise and clear
   - Avoid jargon unless industry-standard
   - Proofread for errors

## Example Interactions

**Example 1: Initial Setup**
```
User: "Help me create a resume for job applications"

Claude: [Checks database - finds not initialized]

To help you create tailored resumes, I need to build a database of your professional
profile. Please provide your existing resume in one of these ways:

1. Upload your resume file (PDF, DOCX, or TXT)
2. Paste the content of your resume
3. Provide a link to your online resume/LinkedIn profile

[User provides resume]

Claude: [Extracts data and initializes database]

Perfect! I've extracted and saved your professional profile:
• Personal Information: ✓
• Work Experience: 3 positions
• Projects: 2 projects
• Education: 1 degree
• Skills: 4 categories
• Certifications: 2 certifications

Your resume database is ready! Tell me about a job you're applying to and I'll
generate a customized one-page PDF resume.
```

**Example 2: Generate Resume for Specific Role**
```
User: "I need a resume for a Senior Backend Engineer position at a fintech startup"

Claude: [Database initialized]

Great! To create the perfect resume for this Senior Backend Engineer role, can you
share the job description or tell me about the key requirements?

User: [Shares job description mentioning Python, AWS, microservices, PostgreSQL, etc.]

Claude: [Extracts keywords: python, aws, microservices, postgresql, fintech, api]

[Generates PDF using relevant experiences and projects]

I've created your tailored resume: ~/Downloads/Senior_Backend_Engineer_Resume.pdf

The resume highlights:
✓ Your 5 years of backend experience with Python and microservices
✓ AWS and Kubernetes expertise from your current role
✓ PostgreSQL and database optimization achievements
✓ Your fintech-relevant project on payment processing
✓ All technical skills matching the job requirements

The resume is optimized for ATS systems and kept to exactly one page. Would you
like me to adjust anything?
```

**Example 3: Update Experience**
```
User: "I just completed a major project - built a real-time analytics system processing 1M events per minute using Kafka"

Claude: [Loads resume data]

Excellent achievement! Let me add this to your profile. A few questions:

1. Should I add this as a new bullet point to your current role, or as a separate project?
2. What technologies did you use besides Kafka?
3. What was the business impact or outcome?

User: "Add it to my current role. Used Kafka, Redis, Python, and TimescaleDB. Reduced report generation time from hours to seconds."

Claude: [Updates experience]

✓ Updated your current role with this achievement:

"Built real-time analytics system processing 1M+ events/minute using Kafka, Redis, and TimescaleDB, reducing report generation time from hours to seconds"

This will now appear in future resumes, especially for roles requiring streaming
data, Kafka, or analytics experience.
```

**Example 4: Multiple Resume Versions**
```
User: "I'm applying to both backend and full-stack positions. Can you create resumes for both?"

Claude: Sure! Let's create two targeted versions.

[Generates backend-focused resume emphasizing API development, microservices, databases]
✓ Backend Engineer Resume: Emphasizes your Python/Go backend work, API design, and infrastructure scaling

[Generates full-stack resume including both backend and frontend projects]
✓ Full-Stack Engineer Resume: Balances your backend expertise with React projects and full-stack achievements

Both resumes are one page and optimized for their respective roles. The main
differences are:
- Backend version: More emphasis on system design, performance, and infrastructure
- Full-stack version: Includes your React projects and mentions end-to-end ownership

Which one would you like to review first?
```

**Example 5: Resume Review and Optimization**
```
User: "Can you review my resume data and suggest improvements?"

Claude: [Analyzes resume database]

I've reviewed your profile. Here are my recommendations:

**Strengths:**
✓ Good mix of quantifiable achievements
✓ Recent experience with in-demand technologies
✓ Clear progression in roles and responsibilities

**Areas for Improvement:**

1. **Add Metrics** to these bullet points:
   - "Improved API performance" → Add percentage improvement
   - "Led team of engineers" → Specify team size and outcomes

2. **Update Skills** section:
   - Remove outdated: jQuery, Bower (unless specifically needed)
   - Add trending: TypeScript, Next.js (if you've used them)

3. **Expand Recent Project**:
   - Your latest project mentions "built authentication system"
   - Add: number of users, security standards followed, or technologies used

4. **Certifications**:
   - Your AWS cert expires soon - plan to renew
   - Consider adding Kubernetes cert you mentioned pursuing

Would you like me to help update any of these areas?
```

## Technical Notes

**Data Storage:**
- Location: `~/.claude/resume_data.json`
- Format: Structured JSON
- Backup: Use `python3 scripts/resume_db.py export`

**PDF Generation:**
- Library: reportlab (requires: `pip install reportlab`)
- Page size: US Letter (8.5" x 11")
- Margins: 0.75 inches all sides
- Font: Helvetica family
- Optimized for: One-page resumes, ATS compatibility

**Resume Styling:**
- Professional color scheme (blues and grays)
- Clear section headers with underlines
- Consistent spacing and formatting
- Bullet points for achievements
- Contact info in header
- Technical skills as comma-separated lists

**Database Commands:**
```bash
# Check initialization
python3 scripts/resume_db.py is_initialized

# View data
python3 scripts/resume_db.py summary
python3 scripts/resume_db.py get_experiences
python3 scripts/resume_db.py get_projects
python3 scripts/resume_db.py get_education
python3 scripts/resume_db.py get_skills

# Search
python3 scripts/resume_db.py search "keyword"

# Export/Backup
python3 scripts/resume_db.py export > backup.json

# Reset (caution!)
python3 scripts/resume_db.py reset
```

**PDF Generation Commands:**
```bash
# Generate general resume
python3 scripts/pdf_generator.py output.pdf

# Generate with job title
python3 scripts/pdf_generator.py output.pdf --title "Senior Software Engineer"

# Generate with keyword filtering
python3 scripts/pdf_generator.py output.pdf --keywords python aws kubernetes docker
```

**Data Structure Example:**
```json
{
  "initialized": true,
  "personal_info": {
    "name": "Your Name",
    "email": "email@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "City, State",
    "linkedin": "linkedin.com/in/username",
    "github": "github.com/username",
    "summary": "Professional summary"
  },
  "experiences": [
    {
      "id": 1234567890.123,
      "position": "Senior Engineer",
      "company": "Company Name",
      "location": "City, State",
      "start_date": "Jan 2022",
      "end_date": "Present",
      "highlights": ["Achievement 1", "Achievement 2"],
      "technologies": ["Python", "AWS"]
    }
  ],
  "skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["Django", "React"]
  }
}
```

## Resources

### scripts/resume_db.py

Complete database management system providing:
- Data initialization and persistence
- CRUD operations for all resume sections
- Relevance-based filtering for experiences/projects
- Keyword-based skill matching
- Search functionality across all data
- Data export and backup
- CLI interface for all operations

### scripts/pdf_generator.py

Professional PDF generation engine:
- ReportLab-based PDF creation
- Custom styling matching professional standards
- One-page optimization
- Keyword-based content filtering
- Relevance scoring for experiences/projects
- ATS-friendly formatting
- Command-line interface

### assets/resume_template.json

Sample resume data structure showing:
- Complete data format
- Best practices for content
- Example bullet points with metrics
- Proper date formatting
- Skill categorization
- All supported sections