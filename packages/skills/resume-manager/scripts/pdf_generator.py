#!/usr/bin/env python3
"""
Resume PDF Generator

Generates styled PDF resumes from resume data.
Requires: reportlab (pip install reportlab)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from resume_db import (
    get_personal_info, get_experiences, get_projects,
    get_education, get_skills, get_certifications,
    get_relevant_experiences, get_relevant_projects,
    get_relevant_skills
)

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab not installed. Install with: pip install reportlab")
    sys.exit(1)

from typing import Dict, Any, List, Optional
from datetime import datetime


class ResumeGenerator:
    """Generate styled PDF resumes."""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Name style
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Contact style
        self.styles.add(ParagraphStyle(
            name='Contact',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#4a4a4a'),
            alignment=TA_CENTER,
            spaceAfter=12
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=colors.HexColor('#2c3e50'),
            borderPadding=0,
            leftIndent=0
        ))

        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))

        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))

        # Date style
        self.styles.add(ParagraphStyle(
            name='Date',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        ))

        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='Bullet',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            leftIndent=15,
            spaceAfter=3,
            bulletIndent=5,
            bulletFontName='Helvetica',
            bulletFontSize=10
        ))

        # Skills style
        self.styles.add(ParagraphStyle(
            name='Skills',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=4
        ))

    def add_header(self, personal_info: Dict[str, Any]):
        """Add resume header with personal info."""
        # Name
        name = personal_info.get('name', 'Your Name')
        self.story.append(Paragraph(name, self.styles['Name']))

        # Contact info
        contact_parts = []
        if personal_info.get('email'):
            contact_parts.append(personal_info['email'])
        if personal_info.get('phone'):
            contact_parts.append(personal_info['phone'])
        if personal_info.get('location'):
            contact_parts.append(personal_info['location'])
        if personal_info.get('linkedin'):
            contact_parts.append(f"LinkedIn: {personal_info['linkedin']}")
        if personal_info.get('github'):
            contact_parts.append(f"GitHub: {personal_info['github']}")
        if personal_info.get('website'):
            contact_parts.append(personal_info['website'])

        contact_line = " • ".join(contact_parts)
        self.story.append(Paragraph(contact_line, self.styles['Contact']))

        # Professional summary if available
        if personal_info.get('summary'):
            self.story.append(Paragraph(personal_info['summary'], self.styles['Normal']))
            self.story.append(Spacer(1, 0.1*inch))

    def add_section_header(self, title: str):
        """Add a section header with underline."""
        self.story.append(Paragraph(f"<b>{title.upper()}</b>", self.styles['SectionHeader']))
        # Add a line under the section
        line_table = Table([['']], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#2c3e50')),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        self.story.append(line_table)
        self.story.append(Spacer(1, 0.05*inch))

    def add_experience(self, exp: Dict[str, Any]):
        """Add a work experience entry."""
        # Position and Company on same line
        position = exp.get('position', 'Position')
        company = exp.get('company', 'Company')
        self.story.append(Paragraph(f"<b>{position}</b> at {company}", self.styles['JobTitle']))

        # Location and date
        location = exp.get('location', '')
        start_date = exp.get('start_date', '')
        end_date = exp.get('end_date', 'Present')
        date_line = f"{start_date} - {end_date}"
        if location:
            date_line = f"{location} | {date_line}"
        self.story.append(Paragraph(date_line, self.styles['Date']))

        # Highlights/bullet points
        highlights = exp.get('highlights', [])
        if highlights:
            for highlight in highlights[:4]:  # Limit to 4 bullet points
                bullet_text = f"• {highlight}"
                self.story.append(Paragraph(bullet_text, self.styles['Bullet']))

        self.story.append(Spacer(1, 0.1*inch))

    def add_project(self, proj: Dict[str, Any]):
        """Add a project entry."""
        # Project name
        name = proj.get('name', 'Project')
        self.story.append(Paragraph(f"<b>{name}</b>", self.styles['JobTitle']))

        # Technologies and date
        technologies = proj.get('technologies', [])
        date = proj.get('date', '')
        tech_line = f"{', '.join(technologies[:5])}"  # Limit technologies shown
        if date:
            tech_line += f" | {date}"
        if tech_line:
            self.story.append(Paragraph(tech_line, self.styles['Date']))

        # Project description and highlights
        if proj.get('description'):
            self.story.append(Paragraph(proj['description'], self.styles['Normal']))

        highlights = proj.get('highlights', [])
        if highlights:
            for highlight in highlights[:3]:  # Limit to 3 bullet points
                bullet_text = f"• {highlight}"
                self.story.append(Paragraph(bullet_text, self.styles['Bullet']))

        self.story.append(Spacer(1, 0.1*inch))

    def add_education(self, edu: Dict[str, Any]):
        """Add an education entry."""
        degree = edu.get('degree', 'Degree')
        school = edu.get('school', 'School')
        self.story.append(Paragraph(f"<b>{degree}</b>, {school}", self.styles['JobTitle']))

        # Location and date
        location = edu.get('location', '')
        graduation = edu.get('graduation_date', '')
        date_line = graduation
        if location:
            date_line = f"{location} | {date_line}"
        if date_line:
            self.story.append(Paragraph(date_line, self.styles['Date']))

        # GPA, honors, relevant coursework
        details = []
        if edu.get('gpa'):
            details.append(f"GPA: {edu['gpa']}")
        if edu.get('honors'):
            details.append(edu['honors'])
        if details:
            self.story.append(Paragraph(", ".join(details), self.styles['Normal']))

        if edu.get('relevant_coursework'):
            coursework = ", ".join(edu['relevant_coursework'][:6])
            self.story.append(Paragraph(f"Relevant Coursework: {coursework}", self.styles['Normal']))

        self.story.append(Spacer(1, 0.1*inch))

    def add_skills(self, skills: Dict[str, List[str]]):
        """Add skills section."""
        for category, skill_list in skills.items():
            skills_text = ", ".join(skill_list)
            self.story.append(Paragraph(f"<b>{category}:</b> {skills_text}", self.styles['Skills']))

    def add_certifications(self, certs: List[Dict[str, Any]]):
        """Add certifications section."""
        for cert in certs:
            name = cert.get('name', 'Certification')
            issuer = cert.get('issuer', '')
            date = cert.get('date', '')

            cert_line = f"<b>{name}</b>"
            if issuer:
                cert_line += f" - {issuer}"
            if date:
                cert_line += f" ({date})"

            self.story.append(Paragraph(cert_line, self.styles['Normal']))
            self.story.append(Spacer(1, 0.05*inch))

    def generate(self, data: Dict[str, Any], job_keywords: Optional[List[str]] = None):
        """Generate the PDF resume."""
        # Header
        personal_info = data.get('personal_info', {})
        self.add_header(personal_info)

        # If job keywords provided, filter relevant content
        if job_keywords:
            experiences = get_relevant_experiences(job_keywords, limit=3)
            projects = get_relevant_projects(job_keywords, limit=2)
            skills = get_relevant_skills(job_keywords)
        else:
            experiences = data.get('experiences', [])[:3]
            projects = data.get('projects', [])[:2]
            skills = data.get('skills', {})

        # Work Experience
        if experiences:
            self.add_section_header("Experience")
            for exp in experiences:
                self.add_experience(exp)

        # Projects
        if projects:
            self.add_section_header("Projects")
            for proj in projects:
                self.add_project(proj)

        # Education
        education = data.get('education', [])
        if education:
            self.add_section_header("Education")
            for edu in education:
                self.add_education(edu)

        # Skills
        if skills:
            self.add_section_header("Technical Skills")
            self.add_skills(skills)

        # Certifications
        certifications = data.get('certifications', [])
        if certifications:
            self.add_section_header("Certifications")
            self.add_certifications(certifications)

        # Build PDF
        self.doc.build(self.story)


def generate_resume(output_path: str, job_title: Optional[str] = None,
                    job_keywords: Optional[List[str]] = None) -> str:
    """
    Generate a tailored resume PDF.

    Args:
        output_path: Path to save the PDF
        job_title: Job title for filename
        job_keywords: Keywords to filter relevant experience/projects

    Returns:
        Path to generated PDF
    """
    from resume_db import export_all

    # Load all resume data
    data = export_all()

    # Create generator
    generator = ResumeGenerator(output_path)

    # Generate PDF
    generator.generate(data, job_keywords)

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate a tailored resume PDF')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--title', help='Job title for tailoring')
    parser.add_argument('--keywords', nargs='+', help='Keywords for relevance filtering')

    args = parser.parse_args()

    try:
        result = generate_resume(args.output, args.title, args.keywords)
        print(f"✓ Resume generated: {result}")
    except Exception as e:
        print(f"✗ Error generating resume: {e}")
        sys.exit(1)
