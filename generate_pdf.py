import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        
        # Header (Pages 2 & 3)
        if self._pageNumber > 1:
            self.drawString(36, 756, "IDEONIX WEBSITE — UI/UX & STRATEGIC AUDIENCE REACH")
            self.drawRightString(576, 756, "EXECUTIVE BRIEF")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.75)
            self.line(36, 748, 576, 748)
            
        # Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.75)
        self.line(36, 42, 576, 42)
        
        self.setFont("Helvetica", 8)
        self.drawString(36, 28, "Ideonix — Innovation for Community")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 28, page_str)
        self.restoreState()

def build_pdf(filename="Ideonix_Website_Design_and_UX.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_orange = colors.HexColor("#F58220")
    c_dark = colors.HexColor("#111827")
    c_blue = colors.HexColor("#2563EB")
    c_gray = colors.HexColor("#4B5563")
    c_bg_light = colors.HexColor("#F9FAFB")
    c_border = colors.HexColor("#E5E7EB")
    
    # Custom Styles
    style_doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_dark,
        spaceAfter=4
    )
    
    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_orange,
        spaceAfter=10
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_dark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
        leftIndent=10,
        spaceAfter=3
    )
    
    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1F2937")
    )
    
    story = []

    # =========================================================================
    # PAGE 1: Strategic Purpose, Design Theme & Brand Perception
    # =========================================================================
    story.append(Paragraph("IDEONIX DIGITAL ECOSYSTEM", style_subtitle))
    story.append(Paragraph("How UI/UX & Visual Theme Amplify Ideonix's Reach", style_doc_title))
    
    meta_data = [
        [
            Paragraph("<b>Core Focus:</b> Mission Amplification & Audience Growth", style_body),
            Paragraph("<b>Primary Audience:</b> Colleges, Students & Partners", style_body),
            Paragraph("<b>Purpose:</b> Strategic UX Analysis", style_body)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[220, 200, 120])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary & Purpose", style_h1))
    story.append(Paragraph(
        "Ideonix's core mission is to transform higher education by developing <b>Compassionate, Creative Problem Solvers</b> "
        "through community-centric innovation. To achieve this at scale, the organization requires a digital gateway that instantly "
        "communicates its vision, earns trust from institutional stakeholders, and engages diverse audiences.",
        style_body
    ))
    story.append(Paragraph(
        "The website's design, user interface (UI), and user experience (UX) serve as a strategic communication multiplier. "
        "By translating complex academic methodologies into intuitive, visually compelling experiences, the platform allows "
        "Ideonix to articulate its value proposition clearly, inspire prospective partners, and expand its regional impact.",
        style_body
    ))

    story.append(Paragraph("2. Strategic Visual Theme: Bridging Rigor & Innovation", style_h1))
    story.append(Paragraph(
        "The visual theme is deliberately crafted to balance <b>academic authority</b> with <b>vibrant entrepreneurial energy</b>:",
        style_body
    ))

    theme_data = [
        [Paragraph("<b>Theme Element</b>", style_body), Paragraph("<b>Visual Choice</b>", style_body), Paragraph("<b>Strategic Contribution to Mission & Outreach</b>", style_body)],
        [Paragraph("High-Contrast Palette", style_body), Paragraph("Obsidian Black (<code>#111827</code>) & Pure White", style_body), Paragraph("Establishes technical seriousness and premium quality, assuring college chairmen and deans of institutional credibility.", style_body)],
        [Paragraph("Brand Action Color", style_body), Paragraph("Vibrant Orange (<code>#F58220</code>)", style_body), Paragraph("Energizes the visual flow, guiding user attention toward key call-to-actions, partnership buttons, and program downloads.", style_body)],
        [Paragraph("Modern Typography", style_body), Paragraph("Inter (Google Fonts)", style_body), Paragraph("Ensures flawless readability across all devices, maintaining sharp typographic clarity from mobile screens to presentation displays.", style_body)],
        [Paragraph("Glassmorphism Panels", style_body), Paragraph("Backdrop Blur & Subtle Borders", style_body), Paragraph("Gives the digital platform a state-of-the-art feel, signaling forward-thinking innovation to tech-savvy students.", style_body)]
    ]
    t_theme = Table(theme_data, colWidths=[110, 120, 310])
    t_theme.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_theme)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Multi-Audience Engagement Strategy", style_h1))
    story.append(Paragraph("• <b>For Institution Leadership (Deans & Principals):</b> Clean layout of program models, institutional outcome structures, and NAAC/NIRF accreditation support via InPulse ERP.", style_bullet))
    story.append(Paragraph("• <b>For Faculty & Coordinators:</b> Clear 12-week syllabi breakdowns, case study structures, and pre-requisite guidance for easy integration into existing curricula.", style_bullet))
    story.append(Paragraph("• <b>For Engineering Students:</b> Dynamic 3D flip cards, maker space equipment showcases, real student success stories, and career development roadmaps.", style_bullet))
    story.append(Paragraph("• <b>For Ecosystem Partners & Govt:</b> Transparent community engagement models, governance collaboration reviews (Solve4DC), and corporate partner endorsements.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: How UI/UX Architecture Contributes to Ideonix's Work
    # =========================================================================
    story.append(Paragraph("4. Translating Complex Work into Interactive UX", style_h1))
    story.append(Paragraph(
        "Abstract educational concepts can be difficult to convey through text alone. The website uses specialized UX components "
        "to make Ideonix's methodology tangible, understandable, and memorable:",
        style_body
    ))

    ux_contrib_data = [
        [Paragraph("<b>Ideonix Work Area</b>", style_body), Paragraph("<b>Interactive UI/UX Solution</b>", style_body), Paragraph("<b>How It Contributes to Work & Engagement</b>", style_body)],
        [Paragraph("<b>Community Innovation Model</b>", style_body), Paragraph("Interactive Venn Diagram (Community + Technocrats + Mentors)", style_body), Paragraph("Visually demonstrates how Ideonix brings diverse stakeholders together to solve regional problems, instantly clarifying the model.", style_body)],
        [Paragraph("<b>Design Thinking Methodology</b>", style_body), Paragraph("5-Stage Process Visualizer (Empathize to Test)", style_body), Paragraph("Breaks down the 12-week IDT framework into simple, step-by-step visual milestones that faculty can evaluate effortlessly.", style_body)],
        [Paragraph("<b>Hardware & Prototyping</b>", style_body), Paragraph("Interactive 3D Hover Cards & Equipment Grids", style_body), Paragraph("Encourages active exploration; visitors flip cards to see circuit prototyping, 3D printing, and robotics lab capabilities.", style_body)],
        [Paragraph("<b>InPulse Digital Platform</b>", style_body), Paragraph("Live-Style Student Dashboard & Skill Tracker Widget", style_body), Paragraph("Demonstrates how the software tracks student CGPA, skills, and projects, proving Ideonix's technology capability.", style_body)],
        [Paragraph("<b>Program Inquiries</b>", style_body), Paragraph("Interactive FAQ Accordion", style_body), Paragraph("Proactively answers institutional onboarding questions, reducing sales friction and accelerating partner decision-making.", style_body)]
    ]
    t_ux_contrib = Table(ux_contrib_data, colWidths=[120, 160, 260])
    t_ux_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ux_contrib)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Expanding Outreach with the Full-Page Article Reader", style_h1))
    story.append(Paragraph(
        "To reach a broader audience — including industry leaders, media, policy advisors, and community members — the website "
        "features a dedicated <b>Full-Page Article Reader System</b> (<code>#page-article</code>).",
        style_body
    ))

    callout_data = [[
        Paragraph(
            "<b>How the Article Reader Expands Reach & Thought Leadership:</b><br/>"
            "• <b>Distraction-Free Immersion:</b> Clicking any news item, blog, or report opens a clean full-page editorial view, allowing visitors to deeply engage with Ideonix's philosophy.<br/>"
            "• <b>Sticky Navigation & Share Triggers:</b> Features an instant '<i>← Back to Resources</i>' return bar alongside social sharing links (Twitter, LinkedIn) so readers can easily broadcast Ideonix articles.<br/>"
            "• <b>Complete Storytelling:</b> Pre-loaded with comprehensive articles on civic innovation (Solve4DC), student mindset growth, NASSCOM achievements, and Annual Impact Reports.<br/>"
            "• <b>Establishes Policy & Industry Authority:</b> Positions Ideonix not just as a service provider, but as a thought leader shaping the future of Indian engineering education.",
            style_callout
        )
    ]]
    t_callout = Table(callout_data, colWidths=[540])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF7F0")),
        ('BOX', (0,0), (-1,-1), 1, c_orange),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_callout)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Frictionless Experience, Conversion & Audience Expansion
    # =========================================================================
    story.append(Paragraph("6. Universal Accessibility & Mobile-First Outreach", style_h1))
    story.append(Paragraph(
        "A website can only expand its audience if it works seamlessly across all devices and network conditions. "
        "The website's UX architecture ensures zero technical barriers to entry:",
        style_body
    ))

    reach_data = [
        [Paragraph("<b>UX Architecture Element</b>", style_body), Paragraph("<b>Implementation & Design Standard</b>", style_body), Paragraph("<b>Audience Expansion Benefit</b>", style_body)],
        [Paragraph("Single-Page Router (SPA)", style_body), Paragraph("Instant section switching via client-side JavaScript without page reloads.", style_body), Paragraph("Keeps visitors engaged; zero lag when exploring programs, syllabi, or reports.", style_body)],
        [Paragraph("Mobile-First Responsive Layout", style_body), Paragraph("Collapsible drawer navigation, touch-friendly buttons (44px min tap area).", style_body), Paragraph("Allows college chairmen and students to explore the site seamlessly on smartphones.", style_body)],
        [Paragraph("Lightweight Performance", style_body), Paragraph("Zero heavy framework overhead; fast asset loading via optimized CDN networks.", style_body), Paragraph("Ensures swift access even in Tier-2/Tier-3 regions with lower internet bandwidth.", style_body)],
        [Paragraph("Intuitive Content Filtering", style_body), Paragraph("One-click category filter tabs (All / News / Events) in Resources.", style_body), Paragraph("Allows journalists, partners, and students to quickly find relevant news items.", style_body)]
    ]
    t_reach = Table(reach_data, colWidths=[120, 210, 210])
    t_reach.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_dark),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_reach)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Frictionless Action Pathways (Turning Visitors into Partners)", style_h1))
    story.append(Paragraph("• <b>Contextual Call-to-Actions:</b> Every program page features relevant action triggers ('<i>Request Free Assessment</i>', '<i>Partner with Us</i>', '<i>Download Syllabus</i>'), maintaining clear next steps.", style_bullet))
    story.append(Paragraph("• <b>Polished User Feedback:</b> Replaced harsh browser popups with elegant, branded success dialogs when users request brochures or submit forms, leaving a positive impression.", style_bullet))
    story.append(Paragraph("• <b>Direct Communication Channels:</b> Direct contact email, office campus address (Sahyadri Campus, Mangaluru), phone numbers, and social links are visible on every major page footer.", style_bullet))

    story.append(Paragraph("8. Summary: How the Website Propels Ideonix Forward", style_h1))
    story.append(Paragraph(
        "By combining a modern aesthetic with thoughtful user experience design, the Ideonix website accomplishes three strategic objectives:",
        style_body
    ))
    story.append(Paragraph("1. <b>Articulates Mission & Vision:</b> Turns abstract educational ideas into tangible, visual learning journeys that resonate with college leadership.", style_bullet))
    story.append(Paragraph("2. <b>Builds Trust & Credibility:</b> Uses high-contrast design, clean typography, and authentic storytelling to project institutional quality.", style_bullet))
    story.append(Paragraph("3. <b>Expands Community & Reach:</b> Provides a frictionless, accessible digital platform that invites colleges, students, mentors, and government leaders to join the movement.", style_bullet))
    story.append(Spacer(1, 6))

    summary_data = [[
        Paragraph(
            "<b>Strategic Conclusion:</b> The Ideonix website's UI/UX is not merely decorative — it is a functional "
            "growth driver that amplifies Ideonix's work, enhances brand perception, and enables the organization "
            "to reach and inspire a significantly wider audience.",
            style_callout
        )
    ]]
    t_summary = Table(summary_data, colWidths=[540])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_summary)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Audience-focused PDF successfully generated: {filename}")

if __name__ == '__main__':
    build_pdf()
