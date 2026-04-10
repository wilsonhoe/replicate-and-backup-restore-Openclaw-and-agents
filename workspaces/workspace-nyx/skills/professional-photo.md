---
name: Professional Photo Creation
type: skill
description: Create professional photos, social media graphics, thumbnails, and marketing images programmatically
---

# Professional Photo Creation

**Use this skill when:** You need to create images, graphics, social media posts, thumbnails, marketing visuals, or photo editing.

---

## Quick Commands

### Create Social Media Card (Pillow - Python)

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Theme colors
BG_DARK = (1, 8, 37)
ACCENT = (113, 92, 247)
TEXT_WHITE = (255, 255, 255)
TEXT_SEC = (170, 170, 204)

def create_social_card(title, subtitle, output_path='card.png'):
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Accent gradient bar at top
    for x in range(W):
        r = int(115 + (44 - 115) * x / W)
        g = int(92 + (33 - 92) * x / W)
        b = int(247 + (255 - 247) * x / W)
        draw.rectangle([(x, 0), (x, 6)], fill=(r, g, b))

    # Title
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/inter/Inter-Bold.ttf', 52)
        font_sub = ImageFont.truetype('/usr/share/fonts/truetype/inter/Inter-Regular.ttf', 28)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((60, 200), title, fill=TEXT_WHITE, font=font_title)
    draw.text((60, 280), subtitle, fill=TEXT_SEC, font=font_sub)

    # Badge
    badge_text = "NEW"
    bbox = draw.textbbox((0, 0), badge_text, font=font_sub)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle([(60, 150), (60 + bw + 20, 150 + bh + 10)], radius=6, fill=ACCENT)
    draw.text((70, 153), badge_text, fill=TEXT_WHITE, font=font_sub)

    img.save(output_path, quality=95)
    print(f'Created: {output_path}')

create_social_card('Nexara Platform', 'AI-Powered Workflow Automation')
```

### Run this with:
```bash
python3 create_card.py
```

### Create Metric Dashboard Card (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont

def create_metric_card(label, value, change, output_path='metric.png'):
    W, H = 400, 280
    CARD_BG = (10, 18, 58)

    img = Image.new('RGB', (W, H), CARD_BG)
    draw = ImageDraw.Draw(img)

    # Border
    draw.rounded_rectangle([(0, 0), (W-1, H-1)], radius=16, outline=(113, 92, 247), width=2)

    try:
        font_val = ImageFont.truetype('/usr/share/fonts/truetype/inter/Inter-Bold.ttf', 48)
        font_label = ImageFont.truetype('/usr/share/fonts/truetype/inter/Inter-Regular.ttf', 16)
        font_change = ImageFont.truetype('/usr/share/fonts/truetype/inter/Inter-Regular.ttf', 14)
    except:
        font_val = font_label = font_change = ImageFont.load_default()

    # Value (centered)
    draw.text((W//2, 80), value, fill=(113, 92, 247), font=font_val, anchor='mm')
    # Label (centered)
    draw.text((W//2, 140), label, fill=(170, 170, 204), font=font_label, anchor='mm')
    # Change badge
    change_color = (16, 185, 129) if '+' in change else (239, 68, 68)
    draw.text((W//2, 200), change, fill=change_color, font=font_change, anchor='mm')

    img.save(output_path, quality=95)
    print(f'Created: {output_path}')

create_metric_card('Revenue', '$187K', '+81% QoQ')
```

### Create with Sharp (Node.js)

```javascript
const sharp = require('sharp');

async function createSocialCard({ title, subtitle, output = 'card.png' }) {
    const width = 1200;
    const height = 630;

    const svgBuffer = Buffer.from(`
    <svg width="${width}" height="${height}">
        <defs>
            <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#733CFA"/>
                <stop offset="100%" style="stop-color:#2C21FF"/>
            </linearGradient>
        </defs>
        <rect width="${width}" height="${height}" fill="#010825"/>
        <rect width="${width}" height="6" fill="url(#accent)"/>
        <text x="60" y="250" fill="white" font-size="52" font-family="Inter, sans-serif" font-weight="bold">${title}</text>
        <text x="60" y="310" fill="#AAAACC" font-size="28" font-family="Inter, sans-serif">${subtitle}</text>
        <rect x="60" y="160" width="60" height="28" rx="6" fill="#715CF7"/>
        <text x="70" y="180" fill="white" font-size="14" font-family="Inter, sans-serif">NEW</text>
    </svg>`);

    await sharp(svgBuffer)
        .png({ quality: 95 })
        .toFile(output);

    console.log(`Created: ${output}`);
}

createSocialCard({ title: 'Nexara Platform', subtitle: 'AI-Powered Workflow Automation' });
```

### Run this with:
```bash
node create_card.js
```

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
Hero:      54-72pt (bold)
Heading:   32-40pt (bold)
Subhead:   22-28pt (regular)
Body:      16-20pt (regular)
Caption:   12-14pt (regular)
Font:      Inter (fallback: system sans-serif)
```

### Composition Rules
- 1" margins minimum
- 0.4" gap between cards
- Max 4 columns for metrics
- Max 40 words per card
- Hierarchy through size contrast (3:1 minimum)
- Use accent color for emphasis, not everywhere

---

## Social Media Dimensions

| Platform | Size | Format | Notes |
|----------|------|--------|-------|
| Instagram Post | 1080x1080 | PNG/JPG | Square feed post |
| Instagram Story | 1080x1920 | PNG/JPG | Vertical full-screen |
| Twitter/X Post | 1200x675 | PNG/JPG | 16:9 landscape |
| Twitter/X Header | 1500x500 | PNG/JPG | Wide banner |
| LinkedIn Post | 1200x627 | PNG/JPG | 1.91:1 landscape |
| LinkedIn Banner | 1584x396 | PNG/JPG | Company page banner |
| YouTube Thumbnail | 1280x720 | JPG/PNG | 16:9, bold text |
| Facebook Cover | 820x312 | PNG/JPG | Desktop + mobile safe |
| TikTok | 1080x1920 | PNG/JPG | Vertical 9:16 |
| Pinterest | 1000x1500 | PNG/JPG | 2:3 tall |
| Open Graph | 1200x630 | PNG/JPG | Link preview card |

---

## Photo Types

1. **Social Card** — Branded image for Twitter/LinkedIn/Instagram posts
2. **Metric Dashboard** — KPI cards with values and change indicators
3. **Quote Card** — Large quote with attribution and accent styling
4. **Thumbnail** — Eye-catching YouTube/social thumbnail
5. **Banner** — Wide header for profiles or landing pages
6. **Announcement** — Product launch or feature reveal
7. **Comparison** — Side-by-side before/after or feature comparison
8. **Infographic** — Data visualization with icons and stats

---

## Workflow (Step by Step)

1. **Decide image type** — What are you making? (social card, metric, thumbnail, etc.)
2. **Choose framework** — Pillow (Python, quick), Sharp (Node.js, performant), Canvas/SVG (web)
3. **Set dimensions** — Pick from the social media dimensions table above
4. **Apply design system** — Use the colors, typography, and composition rules
5. **Build layers** — Background → cards → text → badges → decorations
6. **Export** — PNG for graphics (quality 95), JPG for photos (quality 85), WebP for web
7. **Verify** — Check dimensions, file size (<5MB for social), readability at small sizes

---

## When to Use Each Tool

| Tool | Best For | Output | Skill Level |
|------|----------|--------|-------------|
| Pillow (PIL) | Quick cards, batch generation, metric graphics | PNG/JPG | Python |
| Sharp | High-performance, Node.js projects, batch resize | PNG/JPG/WebP | Node.js |
| Canvas/SVG | Web-based generation, interactive graphics | PNG/SVG | JavaScript |
| fal.ai Flux | AI-generated images, concept art, photorealistic content | PNG | API |

---

## AI Image Generation (fal.ai Flux)

For photorealistic or creative images that can't be made programmatically:

```python
import fal_client

# Generate image with Flux
result = fal_client.run(
    "fal-ai/flux/schnell",
    arguments={
        "prompt": "Professional product photo of a SaaS dashboard, dark theme, purple accent lighting, clean minimal design, 4k",
        "image_size": "landscape_16_9",
        "num_images": 1,
    }
)
image_url = result["images"][0]["url"]
```

Then post-process with Pillow:
```python
from PIL import Image
import requests

img = Image.open(requests.get(image_url, stream=True).raw)
# Add brand overlay, watermark, resize for social
img.save('ai_card.png', quality=95)
```

---

## Anti-Patterns

- **Default templates** — Always customize colors, fonts, and layout
- **No hierarchy** — Use size contrast (3:1 minimum between heading and body)
- **Too much text** — Max 40 words per card, max 8 for thumbnails
- **Wrong dimensions** — Always match target platform specs exactly
- **Large file sizes** — Optimize: PNG for graphics, JPG for photos, WebP for web
- **Unreadable at small sizes** — Test at 50% zoom before publishing
- **Missing brand elements** — Include accent color, consistent font, proper spacing

---

## Memory Reminder

After creating an image, remember:
1. What image type you created
2. Which framework you used (Pillow/Sharp/Canvas/fal.ai)
3. The output file path and dimensions
4. Any issues or improvements for next time