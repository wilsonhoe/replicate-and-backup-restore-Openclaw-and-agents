#!/usr/bin/env python3
"""
LeadFlow Pro - PDF User Guide Generator
Creates a beautiful, professional PDF guide for customers
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# Brand Colors
PRIMARY_COLOR = HexColor('#2563EB')  # Blue
SECONDARY_COLOR = HexColor('#10B981')  # Green
ACCENT_COLOR = HexColor('#F59E0B')  # Amber
BG_COLOR = HexColor('#F8FAFC')  # Light gray
TEXT_COLOR = HexColor('#1E293B')  # Dark slate


def create_leadflow_guide(output_path="LeadFlow_Pro_User_Guide.pdf"):
    """Generate the complete PDF guide"""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    # Container for elements
    elements = []

    # Custom styles
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=PRIMARY_COLOR,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    # Heading styles
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY_COLOR,
        spaceAfter=20,
        spaceBefore=30,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=SECONDARY_COLOR,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )

    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=16
    )

    # Callout style (for tips, warnings)
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontSize=10,
        textColor=TEXT_COLOR,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        backColor=HexColor('#DBEAFE'),
        borderPadding=10
    )

    # === COVER PAGE ===
    elements.append(Spacer(1, 2*inch))

    # Main title
    elements.append(Paragraph("LeadFlow Pro", title_style))

    # Subtitle
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=SECONDARY_COLOR,
        spaceAfter=10,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Complete User Guide", subtitle_style))

    elements.append(Spacer(1, 0.5*inch))

    # Tagline
    tagline_style = ParagraphStyle(
        'Tagline',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_COLOR,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Automated Real Estate Lead Generation System", tagline_style))

    elements.append(Spacer(1, 1*inch))

    # Version info
    version_style = ParagraphStyle(
        'Version',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Version 1.0 | April 2026", version_style))

    elements.append(PageBreak())

    # === TABLE OF CONTENTS ===
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.3*inch))

    toc_items = [
        "1. Welcome to LeadFlow Pro",
        "2. System Overview",
        "3. Quick Start Guide",
        "4. Setting Up Your Notion CRM",
        "5. Installing the Scraper",
        "6. Running Your First Scrape",
        "7. Managing Leads",
        "8. Email Templates & Follow-ups",
        "9. Automation Workflows",
        "10. Troubleshooting",
        "11. Advanced Tips",
        "12. Support & Resources"
    ]

    for item in toc_items:
        elements.append(Paragraph(item, body_style))

    elements.append(PageBreak())

    # === CHAPTER 1: WELCOME ===
    elements.append(Paragraph("1. Welcome to LeadFlow Pro", heading1_style))

    welcome_text = """
    Welcome to LeadFlow Pro, the complete lead generation system designed specifically
    for real estate professionals. This guide will walk you through everything you need
    to know to start generating qualified leads on autopilot.
    """
    elements.append(Paragraph(welcome_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("What You'll Learn:", heading2_style))

    learn_items = [
        "• How to set up your automated lead scraper",
        "• Configuring your Notion CRM for optimal lead management",
        "• Best practices for lead follow-up and conversion",
        "• Automation workflows that save hours every week",
        "• Advanced techniques for scaling your lead generation"
    ]

    for item in learn_items:
        elements.append(Paragraph(item, body_style))

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph(
        "💡 Tip: Bookmark this guide! You'll want to reference it as you set up your system.",
        callout_style
    ))

    elements.append(PageBreak())

    # === CHAPTER 2: SYSTEM OVERVIEW ===
    elements.append(Paragraph("2. System Overview", heading1_style))

    overview_text = """
    LeadFlow Pro consists of three main components that work together to create a
    seamless lead generation pipeline:
    """
    elements.append(Paragraph(overview_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    # Component table
    component_data = [
        ['Component', 'Purpose', 'Time to Setup'],
        ['Python Scraper', 'Automatically extracts leads from property listings', '15 min'],
        ['Notion CRM', 'Organizes and tracks all your leads', '10 min'],
        ['Email Templates', 'Follow-up sequences that convert', '5 min'],
    ]

    component_table = Table(component_data, colWidths=[2*inch, 3*inch, 1.2*inch])
    component_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(component_table)

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("How It Works:", heading2_style))

    workflow_text = """
    <b>Step 1:</b> The scraper runs automatically (every 6 hours by default) and extracts
    lead information from property listings in your target cities.<br/><br/>

    <b>Step 2:</b> New leads are exported to your Notion CRM with all relevant details
    (name, phone, email, budget, property interest).<br/><br/>

    <b>Step 3:</b> You receive notifications (optional) when new leads arrive.<br/><br/>

    <b>Step 4:</b> Use the provided email templates to follow up with leads and move
    them through your sales pipeline.<br/><br/>

    <b>Step 5:</b> Close more deals with a consistent flow of qualified leads!
    """
    elements.append(Paragraph(workflow_text, body_style))

    elements.append(PageBreak())

    # === CHAPTER 3: QUICK START ===
    elements.append(Paragraph("3. Quick Start Guide", heading1_style))

    elements.append(Paragraph("Prerequisites", heading2_style))

    prereq_text = """
    Before you begin, ensure you have:<br/><br/>
    • Python 3.8 or higher installed<br/>
    • A Notion account (free tier works fine)<br/>
    • Notion integration token (we'll show you how to get this)<br/>
    • Basic understanding of your computer's command line<br/>
    """
    elements.append(Paragraph(prereq_text, body_style))

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("Quick Start Checklist", heading2_style))

    checklist_data = [
        ['☐', 'Install Python dependencies', '5 min'],
        ['☐', 'Create Notion integration', '5 min'],
        ['☐', 'Set up databases using setup script', '10 min'],
        ['☐', 'Configure scraper settings', '5 min'],
        ['☐', 'Run first scrape', '2 min'],
        ['☐', 'Review and customize email templates', '10 min'],
    ]

    checklist_table = Table(checklist_data, colWidths=[0.5*inch, 3.5*inch, 1.5*inch])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_COLOR),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    elements.append(checklist_table)

    elements.append(PageBreak())

    # === CHAPTER 4: NOTION SETUP ===
    elements.append(Paragraph("4. Setting Up Your Notion CRM", heading1_style))

    elements.append(Paragraph("Step 1: Create a Notion Integration", heading2_style))

    step1_text = """
    1. Go to <a href="https://www.notion.so/my-integrations" color="blue">notion.so/my-integrations</a><br/>
    2. Click "New integration"<br/>
    3. Give it a name (e.g., "LeadFlow Pro")<br/>
    4. Select your workspace<br/>
    5. Copy the "Internal Integration Token"<br/>
    6. Save this token - you'll need it for the setup script
    """
    elements.append(Paragraph(step1_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Step 2: Run the Setup Script", heading2_style))

    step2_text = """
    1. Open your terminal/command prompt<br/>
    2. Navigate to the NOTION_TEMPLATE folder<br/>
    3. Set your Notion API key as an environment variable:<br/>
    &nbsp;&nbsp;&nbsp;• Mac/Linux: <code>export NOTION_API_KEY=your_token_here</code><br/>
    &nbsp;&nbsp;&nbsp;• Windows: <code>set NOTION_API_KEY=your_token_here</code><br/>
    4. Run: <code>python setup_notion_crm.py</code><br/>
    5. The script will create your complete CRM structure!
    """
    elements.append(Paragraph(step2_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "⚠️ Important: Keep your API key secure! Never share it or commit it to public repositories.",
        callout_style
    ))

    elements.append(PageBreak())

    # === CHAPTER 5: INSTALLING SCRAPER ===
    elements.append(Paragraph("5. Installing the Scraper", heading1_style))

    elements.append(Paragraph("Installation Steps", heading2_style))

    install_text = """
    <b>Step 1:</b> Navigate to the SCRAPER folder in your terminal<br/><br/>

    <b>Step 2:</b> Install Python dependencies:<br/>
    <code>pip install -r requirements.txt</code><br/><br/>

    <b>Step 3:</b> Copy the environment template:<br/>
    • Mac/Linux: <code>cp .env.example .env</code><br/>
    • Windows: <code>copy .env.example .env</code><br/><br/>

    <b>Step 4:</b> Edit the .env file with your Notion API key<br/><br/>

    <b>Step 5:</b> Configure your scraper settings in config.json<br/><br/>

    <b>Step 6:</b> Test the installation:<br/>
    <code>python scraper.py --run-once</code>
    """
    elements.append(Paragraph(install_text, body_style))

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("Configuration Options", heading2_style))

    config_table = Table([
        ['Setting', 'Description', 'Example'],
        ['cities', 'List of cities to scrape', '["New York", "LA"]'],
        ['property_types', 'Types of properties', '["house", "condo"]'],
        ['price_range', 'Min/max price filter', '{"min": 200000}'],
        ['schedule.interval_hours', 'How often to run', '6'],
    ], colWidths=[1.5*inch, 3*inch, 1.5*inch])

    config_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(config_table)

    elements.append(PageBreak())

    # === CHAPTER 6: FIRST SCRAPE ===
    elements.append(Paragraph("6. Running Your First Scrape", heading1_style))

    elements.append(Paragraph("Manual Run", heading2_style))

    manual_text = """
    To run the scraper once and see the results:<br/><br/>

    <code>python scraper.py --run-once</code><br/><br/>

    This will:<br/>
    • Scrape all configured cities<br/>
    • Extract lead information<br/>
    • Save results to leads.csv<br/>
    • Show you a summary in the terminal
    """
    elements.append(Paragraph(manual_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Scheduled Mode (Recommended)", heading2_style))

    scheduled_text = """
    To run the scraper continuously on autopilot:<br/><br/>

    <code>python scraper.py --daemon</code><br/><br/>

    This will:<br/>
    • Run immediately on start<br/>
    • Automatically repeat every 6 hours (configurable)<br/>
    • Continue running until you stop it (Ctrl+C)<br/><br/>

    <b>Pro Tip:</b> Run this on a computer that stays on (like an old laptop or
    cloud server) for 24/7 lead generation!
    """
    elements.append(Paragraph(scheduled_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Expected Output", heading2_style))

    output_text = """
    After running, you'll see a file called <b>leads.csv</b> with columns:<br/><br/>
    • <b>name</b> - Contact name<br/>
    • <b>phone</b> - Phone number<br/>
    • <b>email</b> - Email address<br/>
    • <b>budget</b> - Stated budget<br/>
    • <b>property_interest</b> - What they're looking for<br/>
    • <b>source</b> - Where the lead came from<br/>
    • <b>scraped_date</b> - When you found them<br/>
    • <b>status</b> - New (ready for follow-up!)
    """
    elements.append(Paragraph(output_text, body_style))

    elements.append(PageBreak())

    # === CHAPTER 7: MANAGING LEADS ===
    elements.append(Paragraph("7. Managing Leads", heading1_style))

    elements.append(Paragraph("Importing to Notion", heading2_style))

    import_text = """
    To import your CSV leads into Notion:<br/><br/>

    <b>Option 1: Manual Import</b><br/>
    1. Open your Notion Leads Database<br/>
    2. Click the "..." menu → "Merge with CSV"<br/>
    3. Select your leads.csv file<br/>
    4. Map the columns<br/>
    5. Import!<br/><br/>

    <b>Option 2: Automated (Pro Package)</b><br/>
    Use the included Zapier workflow for automatic import.
    """
    elements.append(Paragraph(import_text, body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Lead Status Workflow", heading2_style))

    workflow_items = [
        ("New", "Just imported - needs first contact"),
        ("Contacted", "You've reached out - waiting for response"),
        ("Qualified", "They're interested and have budget"),
        ("Proposal Sent", "You've sent property suggestions"),
        ("Negotiating", "Discussing terms and options"),
        ("Closed Won", "Deal signed! 🎉"),
        ("Closed Lost", "Not moving forward - note why"),
        ("Nurture", "Not ready now - follow up later")
    ]

    for status, description in workflow_items:
        elements.append(Paragraph(f"<b>{status}:</b> {description}", body_style))

    elements.append(PageBreak())

    # === CHAPTER 8: EMAIL TEMPLATES ===
    elements.append(Paragraph("8. Email Templates & Follow-ups", heading1_style))

    elements.append(Paragraph("The 5-Email Sequence", heading2_style))

    email_intro = """
    The included email templates follow a proven sequence designed to nurture
    leads from initial contact to closed deal. Here's the strategy:
    """
    elements.append(Paragraph(email_intro, body_style))

    elements.append(Spacer(1, 0.1*inch))

    email_data = [
        ['Email', 'When to Send', 'Goal'],
        ['1. Welcome', 'Immediately', 'Build rapport'],
        ['2. Value Add', 'Day 2', 'Demonstrate expertise'],
        ['3. Social Proof', 'Day 5', 'Build trust'],
        ['4. Urgency', 'Day 7', 'Create action'],
        ['5. Breakup', 'Day 14', 'Final attempt'],
    ]

    email_table = Table(email_data, colWidths=[1.3*inch, 1.7*inch, 2.5*inch])
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(email_table)

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph(
        "💡 Tip: Personalize each email with the lead's name and specific property interests for best results.",
        callout_style
    ))

    elements.append(PageBreak())

    # === CHAPTER 9: AUTOMATION ===
    elements.append(Paragraph("9. Automation Workflows", heading1_style))

    elements.append(Paragraph("Zapier Integration (Pro Package)", heading2_style))

    zapier_text = """
    The Pro and Agency packages include pre-built Zapier workflows for:<br/><br/>

    • <b>Auto-Import:</b> New CSV leads → Notion automatically<br/>
    • <b>Email Notifications:</b> Get notified when hot leads arrive<br/>
    • <b>CRM Updates:</b> Sync lead status across platforms<br/>
    • <b>Task Creation:</b> Auto-create follow-up tasks<br/><br/>

    To set up:<br/>
    1. Log into Zapier<br/>
    2. Import the included workflow JSON<br/>
    3. Connect your Notion account<br/>
    4. Configure triggers<br/>
    5. Turn on!
    """
    elements.append(Paragraph(zapier_text, body_style))

    elements.append(PageBreak())

    # === CHAPTER 10: TROUBLESHOOTING ===
    elements.append(Paragraph("10. Troubleshooting", heading1_style))

    elements.append(Paragraph("Common Issues", heading2_style))

    issues = [
        ("Scraper returns 0 leads",
         "Check your target cities in config.json. Verify the websites haven't changed their structure."),
        ("Notion import fails",
         "Verify your API key has database permissions. Check the database ID is correct."),
        ("Permission denied errors",
         "Make sure your Notion integration has been added to the databases as a connection."),
        ("Emails not sending",
         "Check your SMTP settings in .env. Gmail requires an App Password, not your regular password."),
    ]

    for issue, solution in issues:
        elements.append(Paragraph(f"<b>❌ {issue}</b>", body_style))
        elements.append(Paragraph(f"✅ Solution: {solution}", body_style))
        elements.append(Spacer(1, 0.1*inch))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Getting Help", heading2_style))

    help_text = """
    • <b>Basic Package:</b> Refer to this guide and the README files<br/>
    • <b>Pro Package:</b> Email support at support@leadflowpro.com<br/>
    • <b>Agency Package:</b> Priority support + community access
    """
    elements.append(Paragraph(help_text, body_style))

    elements.append(PageBreak())

    # === CHAPTER 11: ADVANCED TIPS ===
    elements.append(Paragraph("11. Advanced Tips", heading1_style))

    tips = [
        ("Run 24/7 on Raspberry Pi",
         "A $35 Raspberry Pi can run the scraper continuously using minimal electricity."),
        ("Customize for Your Market",
         "Edit the scraper to target local listing sites specific to your area."),
        ("A/B Test Email Subject Lines",
         "Try different subject lines to improve open rates. Track what works."),
        ("Set Up Lead Scoring",
         "Add custom properties to prioritize high-budget, ready-to-move leads."),
        ("Integrate with Your CRM",
         "If you use Salesforce, HubSpot, or Pipedrive, adapt the export script."),
        ("Create Location-Specific Sequences",
         "Different cities may respond better to different messaging. Customize!"),
    ]

    for tip_title, tip_desc in tips:
        elements.append(Paragraph(f"<b>💡 {tip_title}</b>", body_style))
        elements.append(Paragraph(tip_desc, body_style))
        elements.append(Spacer(1, 0.1*inch))

    elements.append(PageBreak())

    # === CHAPTER 12: RESOURCES ===
    elements.append(Paragraph("12. Support & Resources", heading1_style))

    elements.append(Paragraph("Quick Reference", heading2_style))

    resources = [
        ("Documentation", "Full setup guides and tutorials"),
        ("Video Tutorials", "Walkthroughs for each component"),
        ("Email Templates", "Ready-to-use follow-up sequences"),
        ("Community", "Connect with other LeadFlow Pro users"),
        ("Updates", "Latest features and improvements"),
    ]

    for resource, desc in resources:
        elements.append(Paragraph(f"<b>{resource}:</b> {desc}", body_style))

    elements.append(Spacer(1, 0.3*inch))

    elements.append(Paragraph("Thank You!", heading1_style))

    thankyou_text = """
    Thank you for choosing LeadFlow Pro! We're excited to help you grow your
    real estate business with automated lead generation.<br/><br/>

    Remember: Consistency is key. Set up your scraper, follow up with leads
    promptly, and watch your pipeline grow!<br/><br/>

    To your success,<br/>
    <b>The LeadFlow Pro Team</b>
    """
    elements.append(Paragraph(thankyou_text, body_style))

    # Build the PDF
    doc.build(elements)
    print(f"✅ PDF Guide generated: {output_path}")


if __name__ == "__main__":
    create_leadflow_guide()