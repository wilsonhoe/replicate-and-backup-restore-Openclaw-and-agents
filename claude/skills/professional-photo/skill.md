---
name: professional-photo
description: Professional photo creation, editing, compositing, and generation with Pillow, Sharp, Canvas/SVG, and AI APIs
version: 1.0.0
author: OpenClaw
tags: [photo, image, pillow, sharp, canvas, svg, ai-generation, compositing, design]
---

# Professional Photo Creation

Create professional photos and images programmatically — from social media graphics to product shots to branded visuals.

## When to Use

- Creating social media graphics (Instagram, Twitter/X headers, LinkedIn banners)
- Generating branded marketing visuals at scale
- Building product mockups and composite images
- Automating image processing pipelines (resize, watermark, optimize)
- Creating AI-generated imagery with professional post-processing
- Producing print-ready graphics (business cards, flyers, posters)

## Tools & Frameworks

### 1. Pillow / PIL (Python — Image Processing)

Best for: Programmatic image creation, manipulation, compositing, and batch processing.

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math

# ── Design System ──
theme = {
    'bg_dark': (1, 8, 37),
    'bg_card': (10, 18, 58),
    'accent': (113, 92, 247),
    'gradient_start': (115, 60, 250),
    'gradient_end': (44, 33, 255),
    'text_primary': (255, 255, 255),
    'text_secondary': (170, 170, 204),
    'success': (16, 185, 129),
    'warning': (245, 158, 11),
    'danger': (239, 68, 68),
}


class PhotoBuilder:
    """Professional image builder with design system support."""

    def __init__(self, width=1920, height=1080, bg_color=None):
        self.width = width
        self.height = height
        self.img = Image.new('RGB', (width, height), bg_color or theme['bg_dark'])
        self.draw = ImageDraw.Draw(self.img)
        self._load_fonts()

    def _load_fonts(self):
        """Load fonts with fallbacks."""
        font_paths = [
            '/usr/share/fonts/Inter-Bold.ttf',
            '/usr/share/fonts/truetype/inter/Inter-Bold.ttf',
        ]
        self.fonts = {}
        for path in font_paths:
            try:
                self.fonts['heading'] = ImageFont.truetype(path, 54)
                self.fonts['subhead'] = ImageFont.truetype(path, 28)
                self.fonts['body'] = ImageFont.truetype(path, 20)
                self.fonts['caption'] = ImageFont.truetype(path, 14)
                self.fonts['metric'] = ImageFont.truetype(path, 48)
                break
            except OSError:
                continue
        if not self.fonts:
            self.fonts = {
                'heading': ImageFont.load_default(),
                'subhead': ImageFont.load_default(),
                'body': ImageFont.load_default(),
                'caption': ImageFont.load_default(),
                'metric': ImageFont.load_default(),
            }

    def gradient_bg(self, color_start, color_end, direction='diagonal'):
        """Draw gradient background."""
        for y in range(self.height):
            for x in range(self.width):
                if direction == 'diagonal':
                    ratio = (x / self.width + y / self.height) / 2
                elif direction == 'horizontal':
                    ratio = x / self.width
                else:  # vertical
                    ratio = y / self.height
                r = int(color_start[0] + ratio * (color_end[0] - color_start[0]))
                g = int(color_start[1] + ratio * (color_end[1] - color_start[1]))
                b = int(color_start[2] + ratio * (color_end[2] - color_start[2]))
                self.draw.point((x, y), fill=(r, g, b))
        return self

    def gradient_bg_fast(self, color_start, color_end):
        """Fast gradient using numpy (10x faster)."""
        import numpy as np
        arr = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for c in range(3):
            row = np.linspace(color_start[c], color_end[c], self.width)
            arr[:, :, c] = np.tile(row, (self.height, 1))
        # Blend vertically
        for c in range(3):
            col = np.linspace(color_start[c], color_end[c], self.height)
            vertical = np.tile(col.reshape(-1, 1), (1, self.width))
            arr[:, :, c] = (arr[:, :, c].astype(float) * 0.5 + vertical * 0.5).astype(np.uint8)
        self.img = Image.fromarray(arr)
        self.draw = ImageDraw.Draw(self.img)
        return self

    def rounded_rect(self, bbox, radius=16, fill=None, outline=None, width=1):
        """Draw a rounded rectangle."""
        fill = fill or theme['bg_card']
        x1, y1, x2, y2 = bbox
        self.draw.rounded_rectangle(bbox, radius=radius, fill=fill,
                                     outline=outline, width=width)

    def text_centered(self, text, y, font_key='heading', color=None):
        """Draw centered text."""
        color = color or theme['text_primary']
        font = self.fonts.get(font_key, self.fonts['body'])
        bbox = self.draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (self.width - tw) // 2
        self.draw.text((x, y), text, fill=color, font=font)

    def accent_bar(self, x=0, y=0, width=8, height=None, color=None):
        """Decorative accent bar (left edge or top)."""
        color = color or theme['accent']
        height = height or self.height
        self.draw.rectangle([x, y, x + width, y + height], fill=color)

    def badge(self, text, x, y, padding=(16, 8), bg_color=None,
              text_color=None, radius=8):
        """Draw a pill-shaped badge."""
        bg_color = bg_color or theme['accent']
        text_color = text_color or (255, 255, 255)
        font = self.fonts['caption']
        bbox = self.draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pw, ph = padding
        rect = [x, y, x + tw + pw * 2, y + th + ph * 2]
        self.draw.rounded_rectangle(rect, radius=radius, fill=bg_color)
        self.draw.text((x + pw, y + ph), text, fill=text_color, font=font)

    def watermark(self, text='OpenClaw', opacity=80):
        """Add diagonal watermark."""
        txt = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        font = self.fonts['subhead']
        # Draw repeated diagonal text
        for y in range(-self.height, self.height * 2, 200):
            for x in range(-self.width, self.width * 2, 600):
                d.text((x, y), text, fill=(255, 255, 255, opacity), font=font)
        # Rotate overlay
        txt = txt.rotate(25, expand=False, center=(self.width // 2, self.height // 2))
        self.img = Image.alpha_composite(self.img.convert('RGBA'), txt).convert('RGB')
        self.draw = ImageDraw.Draw(self.img)
        return self

    def save(self, path, quality=92, optimize=True):
        """Save with optimization."""
        kwargs = {'quality': quality, 'optimize': optimize}
        if path.endswith('.webp'):
            kwargs['method'] = 4  # balance speed/quality
        elif path.endswith('.png'):
            kwargs = {'optimize': True}
        self.img.save(path, **kwargs)
        return path


# ── Usage: Hero Social Graphic ──
def create_hero_graphic(title, subtitle, accent_text=None, output='hero.png'):
    builder = PhotoBuilder(1920, 1080)
    builder.gradient_bg_fast(theme['gradient_start'], theme['gradient_end'])
    builder.accent_bar(x=60, y=300, width=4, height=200)
    builder.text_centered(title, y=320, font_key='heading')
    builder.text_centered(subtitle, y=400, font_key='subhead',
                          color=theme['text_secondary'])
    if accent_text:
        builder.badge(accent_text, x=860, y=500)
    builder.save(output)
    return output


# ── Usage: Metric Dashboard Graphic ──
def create_metrics_graphic(title, metrics, output='metrics.png'):
    builder = PhotoBuilder(1920, 1080)
    builder.text_centered(title, y=60, font_key='subhead',
                          color=theme['text_secondary'])

    cols = min(len(metrics), 4)
    card_w, card_h = 380, 220
    gap = 30
    total_w = cols * card_w + (cols - 1) * gap
    start_x = (builder.width - total_w) // 2

    for i, (label, value, change) in enumerate(metrics):
        x = start_x + i * (card_w + gap)
        y = 200
        builder.rounded_rect([x, y, x + card_w, y + card_h], radius=16,
                             fill=theme['bg_card'],
                             outline=(26, 37, 90), width=1)
        # Label
        builder.draw.text((x + 24, y + 20), label,
                          fill=theme['text_secondary'], font=builder.fonts['caption'])
        # Value
        builder.draw.text((x + 24, y + 60), value,
                          fill=theme['text_primary'], font=builder.fonts['metric'])
        # Change
        change_color = theme['success'] if '+' in str(change) else theme['danger']
        builder.draw.text((x + 24, y + 140), change,
                          fill=change_color, font=builder.fonts['body'])

    builder.save(output)
    return output
```

### 2. Sharp (Node.js — High-Performance Image Processing)

Best for: Server-side image processing, resizing, compositing, and web optimization.

```javascript
const sharp = require('sharp');
const fs = require('fs');

// ── Design System ──
const theme = {
  bgDark: { r: 1, g: 8, b: 37 },
  accent: { r: 113, g: 92, b: 247 },
  gradientStart: { r: 115, g: 60, b: 250 },
  gradientEnd: { r: 44, g: 33, b: 255 },
};

// ── Resize for social platforms ──
async function resizeForSocial(inputPath, platform) {
  const specs = {
    'instagram-post': { width: 1080, height: 1080 },
    'instagram-story': { width: 1080, height: 1920 },
    'twitter-header': { width: 1500, height: 500 },
    'linkedin-banner': { width: 1584, height: 396 },
    'og-image': { width: 1200, height: 630 },
    'youtube-thumb': { width: 1280, height: 720 },
  };

  const { width, height } = specs[platform] || specs['instagram-post'];

  return sharp(inputPath)
    .resize(width, height, { fit: 'cover', position: 'attention' })
    .webp({ quality: 85, effort: 4 })
    .toFile(`${platform}-${Date.now()}.webp`);
}

// ── Composite with text overlay using SVG ──
async function createBrandedImage(bgPath, title, subtitle, output) {
  const svgText = `
  <svg width="1920" height="1080">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:rgb(1,8,37);stop-opacity:1"/>
        <stop offset="100%" style="stop-color:rgb(26,16,80);stop-opacity:1"/>
      </linearGradient>
      <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#715CF7;stop-opacity:1"/>
        <stop offset="100%" style="stop-color:#2C21FF;stop-opacity:1"/>
      </linearGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#bg)"/>
    <rect x="60" y="300" width="4" height="200" fill="url(#accent)"/>
    <text x="100" y="380" font-family="Inter, sans-serif" font-size="54"
          font-weight="bold" fill="white">${title}</text>
    <text x="100" y="440" font-family="Inter, sans-serif" font-size="28"
          fill="#AAAACC">${subtitle}</text>
  </svg>`;

  return sharp(Buffer.from(svgText))
    .composite([
      { input: bgPath, blend: 'over', top: 0, left: 0 },
    ])
    .png({ quality: 92, effort: 7 })
    .toFile(output);
}

// ── Batch watermark ──
async function batchWatermark(inputDir, watermarkPath, outputDir) {
  const files = fs.readdirSync(inputDir).filter(f =>
    /\.(jpg|jpeg|png|webp)$/i.test(f)
  );

  const watermark = await sharp(watermarkPath)
    .resize(200, 80, { fit: 'inside' })
    .png()
    .toBuffer();

  for (const file of files) {
    const meta = await sharp(`${inputDir}/${file}`).metadata();
    await sharp(`${inputDir}/${file}`)
      .composite([{
        input: watermark,
        blend: 'over',
        top: meta.height - 100,
        left: meta.width - 220,
      }])
      .toFile(`${outputDir}/${file}`);
  }
}

// ── Multi-format export ──
async function exportForWeb(inputPath, name) {
  const img = sharp(inputPath);
  await Promise.all([
    img.clone().webp({ quality: 85 }).toFile(`${name}.webp`),
    img.clone().avif({ quality: 80 }).toFile(`${name}.avif`),
    img.clone().jpeg({ quality: 90 }).toFile(`${name}.jpg`),
  ]);
}
```

### 3. Canvas / SVG (Node.js — Programmatic Graphics)

Best for: Generating complex vector-based graphics, charts, and infographics.

```javascript
const { createCanvas, registerFont } = require('canvas');
const fs = require('fs');

// Register fonts
try {
  registerFont('/usr/share/fonts/Inter-Bold.ttf', { family: 'Inter', weight: 'bold' });
} catch (e) { /* fallback to default */ }

// ── Social media card generator ──
function createSocialCard({ title, subtitle, accent, metrics, outputPath }) {
  const W = 1200, H = 630; // OG image size
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  // Background gradient
  const grad = ctx.createLinearGradient(0, 0, W, H);
  grad.addColorStop(0, '#010825');
  grad.addColorStop(1, '#1a1050');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // Accent bar
  ctx.fillStyle = '#715CF7';
  ctx.fillRect(50, 180, 4, 140);

  // Title
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 42px Inter, sans-serif';
  ctx.fillText(title, 80, 240);

  // Subtitle
  ctx.fillStyle = '#AAAACC';
  ctx.font = '22px Inter, sans-serif';
  ctx.fillText(subtitle, 80, 280);

  // Accent badge
  if (accent) {
    ctx.fillStyle = '#715CF7';
    const badgeX = 80, badgeY = 320;
    roundRect(ctx, badgeX, badgeY, 180, 36, 8);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 14px Inter, sans-serif';
    ctx.fillText(accent, badgeX + 14, badgeY + 24);
  }

  // Metrics (right side)
  if (metrics) {
    const startX = 680;
    metrics.forEach((m, i) => {
      const y = 160 + i * 100;
      ctx.fillStyle = '#0A123A';
      roundRect(ctx, startX, y, 460, 80, 12);
      ctx.fill();
      ctx.strokeStyle = '#1A255A';
      ctx.lineWidth = 1;
      roundRect(ctx, startX, y, 460, 80, 12);
      ctx.stroke();

      ctx.fillStyle = '#715CF7';
      ctx.font = 'bold 32px Inter, sans-serif';
      ctx.fillText(m.value, startX + 20, y + 40);

      ctx.fillStyle = '#AAAACC';
      ctx.font = '14px Inter, sans-serif';
      ctx.fillText(m.label, startX + 20, y + 65);

      if (m.change) {
        ctx.fillStyle = m.change.startsWith('+') ? '#10B981' : '#EF4444';
        ctx.font = '14px Inter, sans-serif';
        ctx.fillText(m.change, startX + 340, y + 40);
      }
    });
  }

  fs.writeFileSync(outputPath, canvas.toBuffer('image/png'));
  return outputPath;
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

// ── Batch social cards from data ──
function batchSocialCards(data, outputDir) {
  return data.map(item => createSocialCard({
    title: item.title,
    subtitle: item.subtitle,
    accent: item.accent,
    metrics: item.metrics,
    outputPath: `${outputDir}/${item.slug}.png`,
  }));
}
```

### 4. AI Image Generation (API — fal.ai, Replicate, Stability)

Best for: AI-generated imagery with professional post-processing.

```python
import requests
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ── fal.ai Flux generation ──
def generate_with_fal(prompt, output_path='generated.png',
                       width=1024, height=1024, num_images=1):
    """Generate images using fal.ai Flux model."""
    import fal_client

    result = fal_client.submit(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": f"{width}x{height}",
            "num_images": num_images,
        }
    ).get()

    images = []
    for i, img_data in enumerate(result['images']):
        img_url = img_data['url']
        resp = requests.get(img_url)
        path = output_path.replace('.png', f'_{i}.png') if num_images > 1 else output_path
        with open(path, 'wb') as f:
            f.write(resp.content)
        images.append(path)
    return images


# ── Professional post-processing pipeline ──
def professional_post_process(image_path, output_path='final.png',
                                brand_overlay=None, watermark_text=None):
    """Apply professional post-processing to AI-generated images."""
    img = Image.open(image_path).convert('RGB')

    # 1. Color correction
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)  # slight saturation boost

    # 2. Contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)

    # 3. Sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    # 4. Add subtle vignette
    vignette = create_vignette(img.size)
    img = Image.composite(img, Image.new('RGB', img.size, (0, 0, 0)),
                          vignette.split()[3])

    # 5. Brand overlay (logo watermark)
    if brand_overlay:
        logo = Image.open(brand_overlay).convert('RGBA')
        logo = logo.resize((int(img.width * 0.12), int(img.height * 0.06)),
                           Image.Resampling.LANCZOS)
        img.paste(logo, (img.width - logo.width - 30,
                         img.height - logo.height - 30), logo)

    # 6. Text watermark
    if watermark_text:
        txt_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt_layer)
        font = ImageFont.truetype('/usr/share/fonts/Inter-Bold.ttf', 16)
        d.text((20, img.height - 30), watermark_text,
               fill=(255, 255, 255, 60), font=font)
        img = Image.alpha_composite(img.convert('RGBA'), txt_layer).convert('RGB')

    img.save(output_path, quality=92, optimize=True)
    return output_path


def create_vignette(size, intensity=0.4):
    """Create a vignette overlay."""
    import numpy as np
    w, h = size
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    radius = np.sqrt(X**2 + Y**2)
    vignette = 1 - np.clip(radius * intensity, 0, 1)
    arr = (vignette * 255).astype(np.uint8)
    return Image.fromarray(arr).convert('RGBA')


# ── Prompt engineering for professional results ──
PROFESSIONAL_PROMPTS = {
    'product_shot': (
        'Professional product photography, {subject}, studio lighting, '
        'clean white background, soft shadows, 85mm lens, f/2.8, '
        'high-end commercial style, 8K detail'
    ),
    'social_hero': (
        'Dynamic hero image for {brand}, modern gradient background '
        '{gradient_colors}, abstract geometric shapes, professional '
        'motion graphics style, ultra clean, 4K'
    ),
    'portrait': (
        'Professional headshot, {subject}, Rembrandt lighting, '
        'shallow depth of field, neutral background, corporate style, '
        'photorealistic, 8K'
    ),
    'infographic_bg': (
        'Abstract technology background for infographic, dark navy '
        'blue {hex_bg}, subtle circuit patterns, gradient accent '
        '{hex_accent}, clean minimal, data visualization style'
    ),
}
```

## Image Production Standards

### Social Media Dimensions
| Platform | Format | Size (px) | Aspect Ratio |
|----------|--------|-----------|-------------|
| Instagram Post | Square | 1080x1080 | 1:1 |
| Instagram Portrait | Portrait | 1080x1350 | 4:5 |
| Instagram Story/Reel | Vertical | 1080x1920 | 9:16 |
| Twitter/X Post | Landscape | 1600x900 | 16:9 |
| Twitter/X Header | Banner | 1500x500 | 3:1 |
| LinkedIn Post | Landscape | 1200x627 | 1.91:1 |
| LinkedIn Banner | Banner | 1584x396 | 4:1 |
| Facebook Cover | Banner | 1640x856 | 1.91:1 |
| YouTube Thumbnail | Landscape | 1280x720 | 16:9 |
| OG Image | Landscape | 1200x630 | 1.91:1 |
| Pinterest Pin | Portrait | 1000x1500 | 2:3 |

### Export Settings
| Format | Use Case | Quality | Notes |
|--------|----------|---------|-------|
| WebP | Web delivery | 80-85 | Best compression, wide support |
| AVIF | Modern web | 75-80 | Smallest files, limited browser support |
| JPEG | Photos/Universal | 88-92 | Universal compatibility |
| PNG | Graphics/Transparent | Optimize | Lossless, larger files |
| SVG | Logos/Icons | N/A | Vector, infinite scale |

### Color & Style
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

### Typography for Graphics
```
Hero Title:    42-54pt  Bold
Section Head:  28-36pt  Bold
Body Text:     18-22pt  Regular
Caption:       12-16pt  Regular
Metric Value:  36-48pt  Bold
Metric Label:  12-14pt  Regular, uppercase
```

### Composition Principles
- Rule of thirds for focal points
- Negative space: 30-40% minimum
- Visual hierarchy through scale contrast
- Max 8 words per text overlay
- Accent bar or gradient for branding consistency
- Rounded corners (8-16px) for card elements
- Subtle shadows for depth (2-4px offset, 8-12px blur)

## Workflow

1. **Define purpose** — social post, hero banner, OG image, print material
2. **Choose framework** — Pillow (Python/batch), Sharp (Node/perf), Canvas (vector), AI API (generation)
3. **Set dimensions** — match target platform specs exactly
4. **Apply design system** — use theme colors, typography, spacing
5. **Build graphic** — layout, text, imagery, overlays
6. **Post-process** — color correction, sharpening, vignette if needed
7. **Export** — multi-format for web (WebP + AVIF + JPEG fallback)
8. **Optimize** — check file size, verify readability at target size

## Batch Production

For creating multiple images from data:

```python
# batch_graphics.py
import json
from PIL import Image, ImageDraw, ImageFont

def batch_social_cards(template_config_path, output_dir='output/'):
    with open(template_config_path) as f:
        items = json.load(f)

    for item in items:
        builder = PhotoBuilder(item.get('width', 1200),
                               item.get('height', 630))
        builder.gradient_bg_fast(
            theme['gradient_start'], theme['gradient_end']
        )
        builder.text_centered(item['title'], y=240, font_key='heading')
        builder.text_centered(item['subtitle'], y=320, font_key='subhead',
                              color=theme['text_secondary'])
        if item.get('accent'):
            builder.badge(item['accent'], x=500, y=400)
        builder.save(f"{output_dir}{item['slug']}.png")
        print(f"Created: {output_dir}{item['slug']}.png")

# Sharp batch equivalent:
# node batch-sharp.js --input data.json --output ./output/
```

## Anti-Patterns

- **Wrong dimensions** — always match target platform specs exactly
- **Text on busy backgrounds** — use overlays or blur for readability
- **Low contrast text** — ensure 4.5:1 minimum contrast ratio
- **Oversized files** — use WebP/AVIF, target <200KB for social, <500KB for web
- **No alt text consideration** — design for accessibility from the start
- **JPEG for graphics** — use PNG/WebP for sharp text and logos
- **Unoptimized PNG** — always use `optimize=True` and consider quantization
- **Skipping color profiles** — embed sRGB for consistent display across devices
- **AI images without post-processing** — always color-correct and sharpen AI output