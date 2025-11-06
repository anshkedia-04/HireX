from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, List

class InterviewPDFGenerator:
    """Generate professional PDF reports for interviews"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5276'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2874a6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1a5276'),
            spaceAfter=6,
            fontName='Helvetica-Bold',
            leftIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='AnswerStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=15,
            alignment=TA_JUSTIFY,
            leftIndent=40
        ))
    
    def generate_pdf(self, interview_data: Dict, output_path: str):
        """Generate PDF report from interview data"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        story = []
        
        # Title
        story.append(Paragraph("AI Interview Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Candidate Information Section
        story.append(Paragraph("Candidate Information", self.styles['SectionHeader']))
        
        candidate_info = [
            ['<b>Candidate Name:</b>', interview_data.get('candidate_name', 'N/A')],
            ['<b>Interview ID:</b>', interview_data.get('interview_id', 'N/A')],
            ['<b>Date:</b>', self._format_date(interview_data.get('timestamp', ''))],
            ['<b>Total Questions:</b>', str(len(interview_data.get('qa_pairs', [])))]
        ]
        
        info_table = Table(candidate_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Technical Introduction Section
        story.append(Paragraph("Technical Introduction", self.styles['SectionHeader']))
        intro_text = interview_data.get('introduction', 'N/A')
        story.append(Paragraph(intro_text, self.styles['AnswerStyle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Q&A Section
        story.append(Paragraph("Interview Questions & Answers", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.1*inch))
        
        for qa in interview_data.get('qa_pairs', []):
            # Question
            q_text = f"Q{qa['question_number']}: {qa['question']}"
            story.append(Paragraph(q_text, self.styles['QuestionStyle']))
            
            # Answer
            a_text = f"<b>Answer:</b> {qa['answer']}"
            story.append(Paragraph(a_text, self.styles['AnswerStyle']))
            story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            "--- End of Interview Report ---",
            self.styles['CustomTitle']
        ))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        doc.build(story)
    
    def _format_date(self, timestamp: str) -> str:
        """Format ISO timestamp to readable date"""
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime('%B %d, %Y at %I:%M %p')
        except:
            return timestamp
