#!/usr/bin/env python3
"""
Convert USER_GUIDE.md to a beautiful, visually designed PDF with graphics
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import re

# Read the markdown file
md_content = Path('/home/wls/.openclaw/workspace/notion-sg-real-estate/USER_GUIDE.md').read_text()

# Process markdown content to enhance structure
# Split into sections for better handling
sections = md_content.split('\n# ')

# Create enhanced HTML content with visual design
enhanced_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

        @page {
            margin: 0;
            size: A4;
            @bottom-center {
                content: counter(page);
                font-family: 'Inter', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        @page:first {
            @bottom-center { content: none; }
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 10.5pt;
            line-height: 1.7;
            color: #2d3748;
        }

        /* Cover Page */
        .cover-page {
            width: 210mm;
            height: 297mm;
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #2b6cb0 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }

        .cover-page::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -30%;
            width: 600px;
            height: 600px;
            background: rgba(255,255,255,0.03);
            border-radius: 50%;
        }

        .cover-page::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -20%;
            width: 400px;
            height: 400px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        }

        .cover-icon {
            font-size: 80pt;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        .cover-title {
            font-family: 'Playfair Display', serif;
            font-size: 36pt;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
            z-index: 1;
        }

        .cover-subtitle {
            font-size: 14pt;
            font-weight: 300;
            opacity: 0.9;
            margin-bottom: 40px;
            z-index: 1;
        }

        .cover-divider {
            width: 100px;
            height: 3px;
            background: rgba(255,255,255,0.5);
            margin: 30px auto;
        }

        .cover-info {
            position: absolute;
            bottom: 60px;
            font-size: 11pt;
            opacity: 0.8;
        }

        /* Section Pages */
        .section-page {
            width: 210mm;
            min-height: 297mm;
            padding: 25mm 20mm;
            page-break-after: always;
            position: relative;
        }

        /* Section Header with Graphic */
        .section-header {
            background: linear-gradient(135deg, #2b6cb0 0%, #1a365d 100%);
            color: white;
            padding: 25px 30px;
            margin: -25mm -20mm 30px -20mm;
            padding-left: 40px;
            position: relative;
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .section-number {
            font-size: 48pt;
            font-weight: 700;
            opacity: 0.3;
            line-height: 1;
        }

        .section-title-group {
            flex: 1;
        }

        .section-icon {
            font-size: 36pt;
            margin-bottom: 5px;
        }

        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 22pt;
            font-weight: 700;
            margin: 0;
        }

        .section-subtitle {
            font-size: 10pt;
            opacity: 0.8;
            margin-top: 5px;
        }

        /* Content Styles */
        h1 {
            display: none; /* Hide original h1, using custom headers */
        }

        h2 {
            font-family: 'Playfair Display', serif;
            font-size: 16pt;
            color: #2b6cb0;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }

        h3 {
            font-size: 12pt;
            color: #1a365d;
            margin: 20px 0 12px 0;
            font-weight: 600;
        }

        p {
            margin: 12px 0;
            text-align: justify;
        }

        /* Visual Callout Boxes */
        .tip-box {
            background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
            border-left: 5px solid #3182ce;
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            position: relative;
        }

        .tip-box::before {
            content: '💡';
            font-size: 20pt;
            position: absolute;
            top: 15px;
            right: 20px;
            opacity: 0.3;
        }

        .tip-box strong {
            color: #2b6cb0;
            display: block;
            margin-bottom: 8px;
            font-size: 11pt;
        }

        .warning-box {
            background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%);
            border-left: 5px solid #ed8936;
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }

        .warning-box::before {
            content: '⚠️';
            font-size: 20pt;
            position: absolute;
            top: 15px;
            right: 20px;
        }

        .info-box {
            background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
            border-left: 5px solid #38a169;
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }

        .info-box strong {
            color: #276749;
        }

        /* Step Cards */
        .step-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin: 20px 0;
        }

        .step-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            display: flex;
            gap: 15px;
            align-items: flex-start;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .step-number {
            background: linear-gradient(135deg, #2b6cb0 0%, #1a365d 100%);
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14pt;
            flex-shrink: 0;
        }

        .step-content {
            flex: 1;
        }

        .step-title {
            font-weight: 600;
            color: #1a365d;
            margin-bottom: 5px;
        }

        /* Graphic Placeholder Areas */
        .graphic-placeholder {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border: 2px dashed #cbd5e0;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            position: relative;
        }

        .graphic-placeholder-icon {
            font-size: 48pt;
            margin-bottom: 15px;
            opacity: 0.4;
        }

        .graphic-placeholder-text {
            color: #718096;
            font-size: 10pt;
            font-style: italic;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            font-size: 10pt;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        th {
            background: linear-gradient(135deg, #2b6cb0 0%, #1a365d 100%);
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 9.5pt;
        }

        td {
            padding: 10px 15px;
            border-bottom: 1px solid #e2e8f0;
            background: white;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:nth-child(even) td {
            background: #f7fafc;
        }

        /* Checklist Style */
        .checklist {
            list-style: none;
            padding: 0;
            margin: 15px 0;
        }

        .checklist li {
            padding: 10px 0 10px 35px;
            position: relative;
            border-bottom: 1px solid #e2e8f0;
        }

        .checklist li:before {
            content: '☐';
            position: absolute;
            left: 0;
            font-size: 16pt;
            color: #2b6cb0;
        }

        /* Lists */
        ul, ol {
            margin: 12px 0;
            padding-left: 25px;
        }

        li {
            margin: 8px 0;
        }

        /* Code */
        code {
            font-family: 'SF Mono', Monaco, monospace;
            background: #edf2f7;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 9.5pt;
            color: #2d3748;
        }

        pre {
            background: #1a202c;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 9pt;
            margin: 15px 0;
        }

        /* Stats Box */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .stat-icon {
            font-size: 28pt;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 20pt;
            font-weight: 700;
            color: #2b6cb0;
        }

        .stat-label {
            font-size: 9pt;
            color: #718096;
            margin-top: 5px;
        }

        /* Workflow Diagram */
        .workflow {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 25px 0;
            padding: 20px 0;
        }

        .workflow-step {
            text-align: center;
            flex: 1;
        }

        .workflow-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #2b6cb0 0%, #1a365d 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-size: 24pt;
        }

        .workflow-label {
            font-size: 9pt;
            font-weight: 600;
            color: #2d3748;
        }

        .workflow-arrow {
            font-size: 20pt;
            color: #cbd5e0;
            padding: 0 10px;
        }

        /* Page Break */
        .page-break {
            page-break-before: always;
        }

        /* Strong emphasis */
        strong {
            color: #1a365d;
            font-weight: 600;
        }
    </style>
</head>
<body>
"""

# Add cover page
enhanced_html += """
<div class="cover-page">
    <div class="cover-icon">🏠</div>
    <div class="cover-title">Singapore Real Estate<br>Command Center</div>
    <div class="cover-subtitle">Complete User Guide for Door Knocking Mastery & Property CRM</div>
    <div class="cover-divider"></div>
    <div class="cover-info">
        <div style="font-size: 14pt; margin-bottom: 10px;">📱 Mobile-First System</div>
        <div>Designed for Real Estate Agents on the Move</div>
    </div>
</div>
"""

# Parse and enhance markdown sections
section_count = 0
for section in sections:
    if not section.strip():
        continue

    section_count += 1
    lines = section.strip().split('\n')
    title = lines[0].strip()
    content = '\n'.join(lines[1:])

    # Define icons for each section
    section_icons = {
        'Cover Page': '📘',
        'Introduction': '👋',
        'Getting Started with Notion': '🚀',
        'System Overview': '🏗️',
        'Before You Go Door Knocking': '📝',
        'Using the System During Door Knocking': '📱',
        'After Your Session': '✅',
        'Managing Your Leads': '👥',
        'Following Up with Leads': '📞',
        'Understanding Your Performance': '📊',
        'Your Daily Routine': '☀️',
        'Weekly Review': '📅',
        'Tips for Success': '💡',
        'Quick Reference': '📋'
    }

    icon = section_icons.get(title, '📄')

    # Convert section content
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])

    # Enhance content with visual elements
    # Convert blockquotes to styled boxes
    html_content = re.sub(
        r'<blockquote>\s*<p><strong>(.*?)</strong>',
        r'<div class="tip-box"><strong>\1</strong>',
        html_content
    )
    html_content = html_content.replace('</blockquote>', '</div>')

    # Add section page
    enhanced_html += f"""
    <div class="section-page">
        <div class="section-header">
            <div class="section-number">{section_count:02d}</div>
            <div class="section-title-group">
                <div class="section-icon">{icon}</div>
                <div class="section-title">{title}</div>
            </div>
        </div>
        {html_content}
    </div>
    """

enhanced_html += """
</body>
</html>
"""

# Save enhanced HTML
html_path = '/home/wls/.openclaw/workspace/notion-sg-real-estate/USER_GUIDE_enhanced.html'
Path(html_path).write_text(enhanced_html)
print(f"Enhanced HTML created: {html_path}")

# Convert to PDF
pdf_path = '/home/wls/.openclaw/workspace/notion-sg-real-estate/Singapore_Real_Estate_User_Guide_Beautiful.pdf'
HTML(string=enhanced_html).write_pdf(pdf_path)

print(f"Beautiful PDF created successfully!")
print(f"Location: {pdf_path}")
print(f"File size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")
