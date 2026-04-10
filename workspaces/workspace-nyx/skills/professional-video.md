---
name: Professional Video Creation
type: skill
description: Create professional videos programmatically — social clips, explainer videos, motion graphics, pitch videos
---

# Professional Video Creation

**Use this skill when:** You need to create videos, animations, motion graphics, social media clips, or explainer videos.

---

## Quick Commands

### Create Video from Image + Audio (FFmpeg)

```bash
ffmpeg -loop 1 -i background.png -i narration.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest -movflags +faststart \
  output.mp4
```

### Add Text Overlay (FFmpeg)

```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Nexara Platform':fontfile=/usr/share/fonts/truetype/inter/Inter-Bold.ttf:\
fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:\
borderw=2:bordercolor=black@0.5" \
  -c:a copy output_with_text.mp4
```

### Picture-in-Picture / Logo Watermark (FFmpeg)

```bash
ffmpeg -i main.mp4 -i logo.png \
  -filter_complex "[1:v]scale=120:60[logo];[0:v][logo]overlay=W-140:H-70" \
  -c:a copy output_pip.mp4
```

### Crossfade Between Clips (FFmpeg)

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4[v01];\
[v01][2:v]xfade=transition=fade:duration=0.5:offset=8[vout]" \
  -map "[vout]" merged.mp4
```

### Social Media Vertical Format (FFmpeg)

```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset medium \
  vertical_reel.mp4
```

### Create Pitch Video (MoviePy - Python)

```python
from moviepy import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
    ColorClip, concatenate_videoclips, ImageClip
)
from moviepy.video.fx import FadeIn, FadeOut

def create_pitch_video(metrics, output_path='pitch.mp4'):
    W, H = 1920, 1080
    FPS = 30
    theme = {
        'bg': (1, 8, 37),
        'accent': (113, 92, 247),
        'text': (255, 255, 255),
    }

    clips = []

    # 1. Hero slide (4 seconds)
    bg = ColorClip(size=(W, H), color=theme['bg'], duration=4)
    title = TextClip(
        text='Nexara Platform',
        font_size=72, color='white',
        font='Inter-Bold', size=(W, None)
    ).set_position(('center', 0.35), relative=True).set_duration(4)
    subtitle = TextClip(
        text='AI-Powered Workflow Automation',
        font_size=32, color='#9A8AFF',
        font='Inter', size=(W, None)
    ).set_position(('center', 0.55), relative=True).set_duration(4)
    hero = CompositeVideoClip([bg, title, subtitle])
    clips.append(hero.with_effects([FadeIn(0.5), FadeOut(0.5)]))

    # 2. Metrics slide (5 seconds)
    metrics_bg = ColorClip(size=(W, H), color=theme['bg'], duration=5)
    metric_clips = [metrics_bg]

    cols = len(metrics)
    for i, (label, value, change) in enumerate(metrics):
        x_pos = (i + 0.5) / cols
        val_clip = TextClip(
            text=value, font_size=56, color='#715CF7',
            font='Inter-Bold'
        ).set_position((x_pos, 0.45), relative=True).set_duration(5)
        label_clip = TextClip(
            text=label, font_size=20, color='#9A8AFF',
            font='Inter'
        ).set_position((x_pos, 0.58), relative=True).set_duration(5)
        metric_clips.extend([val_clip, label_clip])

    metrics_slide = CompositeVideoClip(metric_clips)
    clips.append(metrics_slide.with_effects([FadeIn(0.3), FadeOut(0.3)]))

    # Concatenate all slides
    final = concatenate_videoclips(clips, method='compose')
    final.write_videofile(output_path, fps=FPS, codec='libx264',
                          audio_codec='aac', preset='medium')

create_pitch_video([
    ('Revenue', '$187K', '+81% QoQ'),
    ('Customers', '94', '+71% QoQ'),
    ('NPS', '67', 'Excellent'),
    ('Churn', '4.2%', 'Below Target'),
])
```

### Run this with:
```bash
python3 pitch_video.py
```

---

## Design System

```
Background:     #010825 (dark) / #FAFAFA (light)
Card BG:        #0A123A
Accent:         #715CF7
Gradient:       #733CFA → #2C21FF
Supporting:     #9A8AFF
Text Primary:   #FFFFFF (on dark) / #1A1A2E (on light)
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

### Motion Principles
- Ease-in-out for most transitions (NOT linear)
- Entrance: fade-up, scale-in, slide-in (0.3-0.6s)
- Exit: fade-out, scale-down, slide-out
- Text: appear word-by-word or line-by-line (0.15-0.3s per element)
- Data: count-up animations for numbers
- Scene transitions: 1-2 seconds

---

## Video Types

1. **Pitch Video** — Hero + metrics + CTA slides with transitions
2. **Social Clip** — 9:16 vertical, 30-90 seconds, text overlays
3. **Explainer** — Animated diagrams, step-by-step walkthrough
4. **Demo** — Screen recording with annotations and zoom
5. **Motion Graphic** — Abstract animation, logo reveals, transitions
6. **Waveform** — Audio visualization with branded background

---

## Platform Specs

| Platform | Resolution | FPS | Codec | Max Duration |
|----------|-----------|-----|-------|-------------|
| YouTube | 1920x1080 | 24/30/60 | H.264 | 12h |
| TikTok | 1080x1920 | 30 | H.264 | 10min |
| Instagram Reels | 1080x1920 | 30 | H.264 | 90s |
| LinkedIn | 1920x1080 | 30 | H.264 | 10min |
| Twitter/X | 1920x1080 | 30/60 | H.264 | 2m20s |

---

## Workflow (Step by Step)

1. **Decide video type** — What are you making? (pitch, social clip, explainer, etc.)
2. **Choose framework** — FFmpeg (quick edits), MoviePy (Python assembly), Remotion (React/data), Manim (technical)
3. **Prepare assets** — Background images, audio files, logo PNGs
4. **Write the script** — Max 8 words per text overlay, max 40 words per slide
5. **Build timeline** — Assemble clips, add transitions, overlay text
6. **Add audio** — Normalize to -14 LUFS for streaming
7. **Export** — Use correct resolution/codec for target platform
8. **Verify** — Check file size (CRF 23 for web), aspect ratio, audio levels

---

## When to Use Each Tool

| Tool | Best For | Output | Skill Level |
|------|----------|--------|-------------|
| FFmpeg | Quick edits, format conversion, text overlay, compositing | .mp4, .webm | Command line |
| MoviePy | Script-driven video assembly, batch generation | .mp4 | Python |
| Remotion | Data-driven video, React components, batch rendering | .mp4 | React/Node |
| Manim | Mathematical/technical animation, diagrams | .mp4 | Python |

---

## Anti-Patterns

- **No audio normalization** — Always normalize to -14 LUFS (streaming) or -24 LUFS (broadcast)
- **Linear easing on motion** — Use ease-in-out curves
- **Wall of text on screen** — Max 8 words per text overlay
- **No lower thirds** — Always identify speakers and data sources
- **Oversized files** — Use CRF 23 for web, CRF 18 for archival
- **Wrong aspect ratio** — Always match target platform specs
- **Missing subtitles** — Add SRT subtitles for accessibility

---

## Memory Reminder

After creating a video, remember:
1. What video type you created
2. Which framework you used
3. The output file path
4. Any issues or improvements for next time