---
name: Professional Presentation Creation
type: skill
description: Create stunning presentations programmatically — pitch decks, data dashboards, slide decks
---

# Professional Presentation Creation

**Use this skill when:** You need to create presentations, pitch decks, slide decks, or data dashboards.

---

## Quick Commands

### Create a Pitch Deck (python-pptx)

```bash
python3 -c "
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Theme colors
BG_DARK = RGBColor(0x01, 0x08, 0x25)
ACCENT = RGBColor(0x71, 0x5C, 0xF7)
TEXT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_SEC = RGBColor(0xAA, 0xAA, 0xCC)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Hero slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = BG_DARK

txBox = slide.shapes.add_textbox(Inches(1.2), Inches(2), Inches(10), Inches(2.5))
p = txBox.text_frame.paragraphs[0]
p.text = 'YOUR TITLE HERE'
p.font.size = Pt(54)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

prs.save('deck.pptx')
print('Created: deck.pptx')
"
```

### Create Web Presentation (Reveal.js)

Create `index.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/moon.css">
  <style>
    :root { --r-background-color: #010825; --r-heading-color: #fff; --r-accent-color: #715cf7; }
    .metric-value { font-size: 2.5em; font-weight: 700; color: #715cf7; }
  </style>
</head>
<body>
  <div class="reveal"><div class="slides">
    <section><h1>YOUR TITLE</h1><p>Subtitle</p></section>
    <section><h2>Metrics</h2><p class="metric-value">$187K</p></section>
  </div></div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script>Reveal.initialize({hash:true});</script>
</body>
</html>
```

### Create Markdown Presentation (Marp)

Create `deck.md`:

```markdown
---
marp: true
theme: uncover
style: |
  section { background: #010825; color: #fff; }
  h1 { color: #715cf7; }
---

# YOUR TITLE
## Subtitle

---

# Metrics

| Metric | Value | Change |
|--------|-------|--------|
| Revenue | $187K | +81% |

---

# Thank You
```

Export: `npx @marp-team/marp-cli deck.md --pptx --pdf --html`

---

## Design System

```
Background:     #010825 (dark)
Card BG:        #0A123A
Accent:         #715CF7
Gradient:       #733CFA → #2C21FF
Supporting:     #9A8AFF
Text Primary:   #FFFFFF
Text Secondary: #AAAACC
Success:        #10B981
Warning:        #F59E0B
Danger:         #EF4444
```

### Typography
```
Hero:      54-72pt
Heading:   32-40pt
Subhead:   22-28pt
Body:      16-20pt
Caption:   12-14pt
```

### Layout
- 16:9 ratio (13.333" x 7.5")
- 1" margins minimum
- 0.4" gap between cards
- Max 4 columns for metrics
- Max 40 words per slide

---

## Slide Types

1. **Hero** — Title + subtitle + accent badge
2. **Data Dashboard** — Metric cards with KPIs
3. **Chart** — Bar/line/pie with data
4. **Split** — Two-column comparison
5. **Quote** — Large quote with attribution
6. **Timeline** — Milestones
7. **Team** — Photo grid with roles
8. **CTA** — Call to action

---

## Anti-Patterns

- **Wall of text** — max 40 words per slide
- **No hierarchy** — use size contrast
- **Default templates** — always customize
- **Too many bullets** — prefer cards and visuals

---

## When to Use Each Tool

| Tool | Best For | Output |
|------|----------|--------|
| python-pptx | Data-driven decks, batch generation | .pptx |
| Reveal.js | Interactive web presentations | .html |
| Slidev | Developer talks with code | .html |
| Marp | Quick Markdown decks | .pptx, .pdf, .html |