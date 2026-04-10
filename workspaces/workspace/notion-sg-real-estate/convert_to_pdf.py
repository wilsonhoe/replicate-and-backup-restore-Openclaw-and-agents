#!/usr/bin/env python3
"""
Convert USER_GUIDE.md to a styled PDF
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

# Read the markdown file
md_content = Path('/home/wls/.openclaw/workspace/notion-sg-real-estate/USER_GUIDE.md').read_text()

# Convert markdown to HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Add CSS styling for a professional PDF look
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            margin: 2.5cm 2cm;
            @bottom-center {{
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: Georgia, "Times New Roman", serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }}

        h1 {{
            font-size: 24pt;
            color: #1a5490;
            border-bottom: 3px solid #1a5490;
            padding-bottom: 10px;
            margin-top: 0;
            page-break-before: always;
        }}

        h1:first-of-type {{
            page-break-before: avoid;
            text-align: center;
            border-bottom: none;
            font-size: 28pt;
            margin-top: 3cm;
            color: #1a5490;
        }}

        h2 {{
            font-size: 16pt;
            color: #2d6da3;
            margin-top: 25px;
            margin-bottom: 12px;
            border-left: 4px solid #2d6da3;
            padding-left: 10px;
        }}

        h3 {{
            font-size: 13pt;
            color: #3a7ab5;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        p {{
            margin: 10px 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}

        li {{
            margin: 5px 0;
        }}

        code {{
            font-family: "Courier New", monospace;
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 10pt;
        }}

        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #1a5490;
            font-size: 10pt;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }}

        th {{
            background-color: #1a5490;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }}

        td {{
            padding: 8px 10px;
            border-bottom: 1px solid #ddd;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        blockquote {{
            border-left: 4px solid #2d6da3;
            margin: 15px 0;
            padding: 10px 20px;
            background-color: #f0f7ff;
            font-style: italic;
        }}

        .cover {{
            text-align: center;
            margin-top: 4cm;
        }}

        .cover h1 {{
            font-size: 32pt;
            color: #1a5490;
            margin-bottom: 1cm;
        }}

        .cover p {{
            font-size: 14pt;
            color: #555;
        }}

        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 20px 0;
        }}

        strong {{
            color: #1a5490;
        }}

        em {{
            color: #555;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Save HTML first (for debugging if needed)
html_path = '/home/wls/.openclaw/workspace/notion-sg-real-estate/USER_GUIDE.html'
Path(html_path).write_text(html_template)
print(f"HTML version created: {html_path}")

# Convert to PDF
pdf_path = '/home/wls/.openclaw/workspace/notion-sg-real-estate/Singapore_Real_Estate_User_Guide.pdf'
HTML(string=html_template).write_pdf(pdf_path)

print(f"PDF created successfully: {pdf_path}")
print(f"File size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")
