---
name: professional-presentation
description: Professional presentation creation with beautiful design, data visualization, and export to PPTX/PDF/web
version: 1.0.0
author: OpenClaw
tags: [presentation, pptx, reveal, slidev, marp, design, deck]
---

# Professional Presentation Creation

Create stunning, professional presentations programmatically with beautiful design, data visualization, and multiple export formats.

## When to Use

- Building investor pitch decks, sales presentations, or conference talks
- Creating data-driven dashboards as slide decks
- Generating branded presentation templates
- Producing presentation content from structured data (JSON, CSV, APIs)
- Automating recurring report presentations

## Tools & Frameworks

### 1. python-pptx (Python — PPTX Generation)

Best for: Programmatic PowerPoint creation with full control.

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

class PresentationBuilder:
    """Professional presentation builder with design system support."""

    def __init__(self, theme=None):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)  # 16:9
        self.prs.slide_height = Inches(7.5)
        self.theme = theme or self._default_theme()

    def _default_theme(self):
        return {
            'bg_dark': RGBColor(0x01, 0x08, 0x25),
            'bg_light': RGBColor(0xFF, 0xFF, 0xFF),
            'accent': RGBColor(0x71, 0x5C, 0xF7),
            'accent_gradient_end': RGBColor(0x2C, 0x21, 0xFF),
            'supporting': RGBColor(0x9A, 0x8A, 0xFF),
            'text_primary': RGBColor(0xFF, 0xFF, 0xFF),
            'text_secondary': RGBColor(0xAA, 0xAA, 0xCC),
            'success': RGBColor(0x10, 0xB9, 0x81),
            'warning': RGBColor(0xF5, 0x9E, 0x0B),
            'danger': RGBColor(0xEF, 0x44, 0x44),
            'font_heading': 'Inter',
            'font_body': 'Inter',
            'font_mono': 'JetBrains Mono',
        }

    def add_slide(self, layout_index=6):
        """Blank layout by default."""
        return self.prs.slides.add_slide(self.prs.slide_layouts[layout_index])

    def set_background(self, slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_textbox(self, slide, left, top, width, height, text,
                    font_size=18, color=None, bold=False, alignment=PP_ALIGN.LEFT,
                    font_name=None):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.color.rgb = color or self.theme['text_primary']
        p.font.bold = bold
        p.font.name = font_name or self.theme['font_body']
        p.alignment = alignment
        return txBox

    def add_hero_slide(self, title, subtitle, accent_text=None):
        """Full-bleed dark hero slide with large typography."""
        slide = self.add_slide()
        self.set_background(slide, self.theme['bg_dark'])

        # Decorative accent bar
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            Inches(0.15), Inches(7.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.theme['accent']
        shape.line.fill.background()

        # Title
        self.add_textbox(slide, Inches(1.2), Inches(2),
                         Inches(10), Inches(2.5), title,
                         font_size=54, bold=True,
                         color=self.theme['text_primary'])

        # Subtitle
        self.add_textbox(slide, Inches(1.2), Inches(4.5),
                         Inches(8), Inches(1), subtitle,
                         font_size=22,
                         color=self.theme['text_secondary'])

        # Accent badge
        if accent_text:
            badge = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(1.2), Inches(5.8),
                Inches(2.5), Inches(0.5)
            )
            badge.fill.solid()
            badge.fill.fore_color.rgb = self.theme['accent']
            badge.line.fill.background()
            tf = badge.text_frame
            tf.paragraphs[0].text = accent_text
            tf.paragraphs[0].font.size = Pt(14)
            tf.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        return slide

    def add_data_slide(self, title, metrics):
        """Data-focused slide with metric cards."""
        slide = self.add_slide()
        self.set_background(slide, self.theme['bg_dark'])

        self.add_textbox(slide, Inches(1), Inches(0.5),
                         Inches(10), Inches(0.8), title,
                         font_size=32, bold=True)

        cols = min(len(metrics), 4)
        card_width = Inches(2.5)
        gap = Inches(0.4)
        total_width = cols * card_width.inches + (cols - 1) * gap.inches
        start_x = (13.333 - total_width) / 2

        for i, (label, value, change) in enumerate(metrics):
            x = Inches(start_x + i * (card_width.inches + gap.inches))
            y = Inches(2)

            card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, x, y,
                card_width, Inches(2.5)
            )
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor(0x0A, 0x12, 0x3A)
            card.line.color.rgb = RGBColor(0x1A, 0x25, 0x5A)

            self.add_textbox(slide, x + Inches(0.3), y + Inches(0.4),
                             card_width - Inches(0.6), Inches(0.4), label,
                             font_size=13, color=self.theme['text_secondary'])
            self.add_textbox(slide, x + Inches(0.3), y + Inches(0.9),
                             card_width - Inches(0.6), Inches(0.8), value,
                             font_size=36, bold=True,
                             color=self.theme['text_primary'])

            if change:
                change_color = self.theme['success'] if '+' in str(change) else self.theme['danger']
                self.add_textbox(slide, x + Inches(0.3), y + Inches(1.7),
                                 card_width - Inches(0.6), Inches(0.4), change,
                                 font_size=14, color=change_color)

        return slide

    def add_chart_slide(self, title, chart_data, chart_type='bar'):
        """Slide with embedded chart from data."""
        from pptx.chart.data import CategoryChartData
        from pptx.enum.chart import XL_CHART_TYPE

        slide = self.add_slide()
        self.set_background(slide, self.theme['bg_dark'])

        self.add_textbox(slide, Inches(1), Inches(0.5),
                         Inches(10), Inches(0.8), title,
                         font_size=32, bold=True)

        chart_type_map = {
            'bar': XL_CHART_TYPE.COLUMN_CLUSTERED,
            'line': XL_CHART_TYPE.LINE,
            'pie': XL_CHART_TYPE.PIE,
        }

        chart_data_obj = CategoryChartData()
        chart_data_obj.categories = chart_data['categories']
        for series_name, values in chart_data['series']:
            chart_data_obj.add_series(series_name, values)

        chart_frame = slide.shapes.add_chart(
            chart_type_map.get(chart_type, XL_CHART_TYPE.COLUMN_CLUSTERED),
            Inches(1), Inches(1.5),
            Inches(11), Inches(5),
            chart_data_obj
        )
        return slide

    def save(self, filename='presentation.pptx'):
        self.prs.save(filename)
        return filename

# Usage
builder = PresentationBuilder()
builder.add_hero_slide(
    'Nexara Platform',
    'AI-Powered Workflow Automation for Mid-Market Companies',
    'Series A — $5M Raise'
)
builder.add_data_slide('Q4 Traction', [
    ('Revenue', '$187K', '+81% QoQ'),
    ('Customers', '94', '+71% QoQ'),
    ('NPS Score', '67', 'Excellent'),
    ('Churn', '4.2%', 'Below Target'),
])
builder.save('investor_deck.pptx')
```

### 2. Reveal.js (Web — Interactive Presentations)

Best for: Interactive, web-based presentations with code, animations, and speaker notes.

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/moon.css">
  <style>
    :root {
      --r-background-color: #010825;
      --r-heading-color: #ffffff;
      --r-main-color: #9a8aff;
      --r-accent-color: #715cf7;
    }
    .hero-title { font-size: 3em !important; font-weight: 800 !important; }
    .metric-value { font-size: 2.5em; font-weight: 700; color: #715cf7; }
    .metric-label { font-size: 0.8em; color: #9a8aff; text-transform: uppercase; }
    .card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
    .card { background: rgba(113,92,247,0.1); border: 1px solid rgba(113,92,247,0.3);
            border-radius: 12px; padding: 1.5rem; text-align: center; }
    .highlight { color: #715cf7; font-weight: 700; }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section data-background-gradient="linear-gradient(135deg, #010825, #1a1050)">
        <h1 class="hero-title">Nexara Platform</h1>
        <p>AI-Powered Workflow Automation</p>
        <p class="fragment fade-up"><small>Series A — $5M Raise</small></p>
      </section>

      <section>
        <h2>Q4 Traction</h2>
        <div class="card-grid">
          <div class="card fragment fade-up">
            <div class="metric-value">$187K</div>
            <div class="metric-label">Revenue (+81%)</div>
          </div>
          <div class="card fragment fade-up">
            <div class="metric-value">94</div>
            <div class="metric-label">Customers (+71%)</div>
          </div>
          <div class="card fragment fade-up">
            <div class="metric-value">67</div>
            <div class="metric-label">NPS Score</div>
          </div>
          <div class="card fragment fade-up">
            <div class="metric-value">4.2%</div>
            <div class="metric-label">Churn</div>
          </div>
        </div>
      </section>

      <section data-markdown>
        ## Market Opportunity
        - $23.77B workflow automation market (2025)
        - Projected **$40.77B by 2031** (9.41% CAGR)
        - 90% of enterprises prioritize hyperautomation
      </section>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      transition: 'slide',
      backgroundTransition: 'fade',
      width: 1280, height: 720,
    });
  </script>
</body>
</html>
```

### 3. Slidev (Vue — Developer Presentations)

Best for: Developer-focused talks with live code, Vue components, and Markdown-first authoring.

```markdown
---
theme: seriph
background: https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920
class: text-center
---

# Nexara Platform
AI-Powered Workflow Automation

<div class="abs-br m-6 text-xl">
  Series A — $5M Raise
</div>

---
layout: center
class: text-center
---

# Q4 Traction

<div class="grid grid-cols-4 gap-4 mt-8">
  <div class="p-6 rounded-xl bg-purple-500/10 border border-purple-500/30">
    <div class="text-4xl font-bold text-purple-400">$187K</div>
    <div class="text-sm text-purple-300 mt-2">Revenue (+81%)</div>
  </div>
  <div class="p-6 rounded-xl bg-purple-500/10 border border-purple-500/30">
    <div class="text-4xl font-bold text-purple-400">94</div>
    <div class="text-sm text-purple-300 mt-2">Customers (+71%)</div>
  </div>
  <div class="p-6 rounded-xl bg-purple-500/10 border border-purple-500/30">
    <div class="text-4xl font-bold text-purple-400">67</div>
    <div class="text-sm text-purple-300 mt-2">NPS Score</div>
  </div>
  <div class="p-6 rounded-xl bg-purple-500/10 border border-purple-500/30">
    <div class="text-4xl font-bold text-purple-400">4.2%</div>
    <div class="text-sm text-purple-300 mt-2">Churn</div>
  </div>
</div>

---
layout: two-cols
---

<template #default>
# Market Opportunity

- **$23.77B** market (2025)
- **$40.77B** projected (2031)
- 9.41% CAGR
- 90% enterprises prioritize hyperautomation
</template>

<template #right>
# Competitive Edge

| Competitor | Segment |
|-----------|---------|
| UiPath | Enterprise RPA |
| Automation Anywhere | Cloud RPA |
| Zapier/Make | SMB No-code |
| **Nexara** | **Mid-market AI** |
</template>
```

### 4. Marp (Markdown — PDF/PPTX/HTML)

Best for: Quick, beautiful presentations from pure Markdown.

```markdown
---
marp: true
theme: uncover
paginate: true
style: |
  section { background: #010825; color: #fff; }
  h1 { color: #715cf7; }
  h2 { color: #9a8aff; }
  code { background: #1a1050; }
  table { margin: auto; }
  th { color: #715cf7; }
---

# Nexara Platform
## AI-Powered Workflow Automation

Series A — $5M Raise

---

# Q4 Traction

| Metric | Value | Change |
|--------|-------|--------|
| Revenue | $187K | +81% QoQ |
| Customers | 94 | +71% QoQ |
| NPS | 67 | Excellent |
| Churn | 4.2% | Below Target |

---

# Market Opportunity

- **$23.77B** workflow automation market (2025)
- Projected **$40.77B** by 2031 at 9.41% CAGR
- 90% enterprises list hyperautomation as strategic priority

---

# Competitive Positioning

> More affordable than UiPath
> More depth than Zapier
> AI-native, not AI-bolted

---
```

Export: `npx @marp-team/marp-cli deck.md --pptx --pdf --html`

## Design Principles

### Typography Scale
```
Hero:      54-72pt  (slide title)
Heading:   32-40pt  (section title)
Subhead:   22-28pt  (supporting text)
Body:      16-20pt  (paragraph text)
Caption:   12-14pt  (labels, footnotes)
Mono:      14-16pt  (code, data)
```

### Color System
```
Background Dark:   #010825
Background Card:   #0A123A
Accent Primary:    #715CF7
Accent Gradient:   #733CFA → #2C21FF
Supporting:        #9A8AFF
Text Primary:      #FFFFFF
Text Secondary:    #AAAACC
Success:           #10B981
Warning:           #F59E0B
Danger:            #EF4444
```

### Layout Grid
- 16:9 aspect ratio (13.333" x 7.5")
- 1" margins minimum
- 0.4" gap between cards
- 4-column max for metric grids
- 2-column for comparison layouts

### Slide Types
1. **Hero** — Title + subtitle + accent badge
2. **Data Dashboard** — Metric cards with KPIs
3. **Chart** — Bar/line/pie with data
4. **Split** — Two-column comparison
5. **Quote** — Large quote with attribution
6. **Timeline** — Chronological milestones
7. **Team** — Photo grid with roles
8. **CTA** — Call to action with contact

## Workflow

1. **Define content structure** — outline slides, data sources, key messages
2. **Choose framework** — PPTX (python-pptx), web (Reveal), dev (Slidev), or fast (Marp)
3. **Apply design system** — use theme config for consistent branding
4. **Generate slides** — build programmatically from data
5. **Export** — PPTX for delivery, PDF for sharing, HTML for interactive

## Anti-Patterns

- **Wall of text** — max 40 words per slide
- **Uniform spacing** — use intentional rhythm, not equal padding everywhere
- **Default templates** — always customize colors, fonts, and layout
- **No hierarchy** — establish clear visual hierarchy with size contrast
- **Too many bullets** — prefer cards, charts, and visual layouts
