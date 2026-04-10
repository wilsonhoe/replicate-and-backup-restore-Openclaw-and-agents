---
name: professional-video
description: Professional video creation, editing, and production with FFmpeg, Remotion, MoviePy, and Manim
version: 1.0.0
author: OpenClaw
tags: [video, ffmpeg, remotion, moviepy, manim, motion-graphics, production]
---

# Professional Video Creation

Create professional videos programmatically — from social media clips to explainer videos to motion graphics.

## When to Use

- Creating social media video content (TikTok, YouTube Shorts, Instagram Reels)
- Building product demo or explainer videos
- Generating branded motion graphics and intros
- Automating video production pipelines at scale
- Creating educational or tutorial videos

## Tools & Frameworks

### 1. FFmpeg (CLI — The Foundation)

Best for: Encoding, transcoding, compositing, and all video manipulation.

```bash
# Create video from image + audio
ffmpeg -loop 1 -i background.png -i narration.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest -movflags +faststart \
  output.mp4

# Add text overlay with styling
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Nexara Platform':fontfile=/usr/share/fonts/Inter-Bold.ttf:\
fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:\
borderw=2:bordercolor=black@0.5" \
  -c:a copy output_with_text.mp4

# Picture-in-picture (logo watermark)
ffmpeg -i main.mp4 -i logo.png \
  -filter_complex "[1:v]scale=120:60[logo];[0:v][logo]overlay=W-140:H-70" \
  -c:a copy output_pip.mp4

# Concatenate clips with crossfade
ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4[v01];\
[v01][2:v]xfade=transition=fade:duration=0.5:offset=8[vout]" \
  -map "[vout]" merged.mp4

# Social media formats
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset medium \
  vertical_reel.mp4

# Generate waveform video from audio
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x720:mode=cline:colors=0x715cf7:\
rate=25[v]" \
  -map "[v]" -map 0:a -c:a aac waveform_video.mp4

# Speed ramp (slowmo effect)
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
  -map "[v]" -map "[a]" slowmo.mp4

# Burn subtitles
ffmpeg -i input.mp4 -i subs.srt \
  -vf "subtitles=subs.srt:force_style='FontSize=20,PrimaryColour=&Hffffff'" \
  -c:a copy output_subtitled.mp4
```

### 2. Remotion (React — Programmatic Video)

Best for: Data-driven video generation with React components, batch rendering.

```tsx
// src/Composition.tsx
import { useCurrentFrame, useVideoConfig, interpolate, Sequence } from 'remotion';

const theme = {
  bg: '#010825',
  accent: '#715CF7',
  supporting: '#9A8AFF',
  text: '#FFFFFF',
  textSecondary: '#AAAACC',
};

export const MetricCard: React.FC<{
  label: string;
  value: string;
  change?: string;
  delay: number;
}> = ({ label, value, change, delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = interpolate(
    frame - delay * fps,
    [0, fps * 0.6],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  const y = interpolate(progress, [0, 1], [40, 0]);
  const opacity = progress;

  return (
    <div style={{
      background: 'rgba(113,92,247,0.08)',
      border: '1px solid rgba(113,92,247,0.3)',
      borderRadius: 16,
      padding: '2rem',
      textAlign: 'center',
      transform: `translateY(${y}px)`,
      opacity,
    }}>
      <div style={{ fontSize: 14, color: theme.textSecondary, textTransform: 'uppercase' }}>
        {label}
      </div>
      <div style={{ fontSize: 48, fontWeight: 800, color: theme.accent, marginTop: 8 }}>
        {value}
      </div>
      {change && (
        <div style={{ fontSize: 14, color: '#10B981', marginTop: 4 }}>{change}</div>
      )}
    </div>
  );
};

export const PitchDeck: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  return (
    <div style={{
      width, height,
      background: `linear-gradient(135deg, ${theme.bg}, #1a1050)`,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      fontFamily: 'Inter, sans-serif',
    }}>
      <Sequence from={0} durationInFrames={fps * 4}>
        <HeroSlide frame={frame} fps={fps} />
      </Sequence>
      <Sequence from={fps * 4} durationInFrames={fps * 5}>
        <MetricsSlide />
      </Sequence>
    </div>
  );
};

// Render to video
// npx remotion render src/index.ts PitchDeck output.mp4
// Batch render: npx remotion render src/index.ts PitchDeck --frames=0-270 --output=out.mp4
```

### 3. MoviePy (Python — Quick Video Assembly)

Best for: Script-driven video editing, combining clips, adding text and effects.

```python
from moviepy import (
    VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
    ColorClip, concatenate_videoclips, ImageClip
)
from moviepy.video.fx import FadeIn, FadeOut

def create_pitch_video(metrics, output_path='pitch.mp4'):
    """Create a professional pitch video from metrics data."""
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

### 4. Manim (Python — Mathematical & Technical Animation)

Best for: Technical explainers, mathematical visualizations, animated diagrams.

```python
from manim import *

class ProductExplainer(Scene):
    """Animated product explainer with professional motion graphics."""

    def construct(self):
        # Dark background
        self.camera.background_color = '#010825'

        # Animated title
        title = Text('Nexara Platform', font_size=48, color='#715CF7')
        subtitle = Text('AI-Powered Workflow Automation', font_size=24, color='#9A8AFF')
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Animated pipeline diagram
        nodes = ['Input', 'Process', 'AI Engine', 'Output']
        colors = ['#9A8AFF', '#715CF7', '#2C21FF', '#10B981']
        mobjects = []

        for i, (label, color) in enumerate(zip(nodes, colors)):
            rect = RoundedRectangle(
                corner_radius=0.2, height=1, width=2,
                fill_opacity=0.3, fill_color=color,
                stroke_color=color, stroke_width=2
            )
            text = Text(label, font_size=18, color='#FFFFFF')
            text.move_to(rect.get_center())
            group = VGroup(rect, text)
            group.shift(RIGHT * (i * 3 - 4.5))
            mobjects.append(group)

        # Animate nodes appearing one by one
        for obj in mobjects:
            self.play(
                GrowFromCenter(obj),
                run_time=0.6,
                rate_func=smooth
            )

        # Animate connections
        for i in range(len(mobjects) - 1):
            arrow = Arrow(
                mobjects[i].get_right(),
                mobjects[i + 1].get_left(),
                color='#715CF7', stroke_width=3,
                buff=0.2
            )
            self.play(GrowArrow(arrow), run_time=0.4)

        self.wait(2)
```

Render: `manim -pql scene.py ProductExplainer` (lq) or `manim -pqh scene.py ProductExplainer` (hq)

## Video Production Standards

### Resolution & Format Guide
| Platform | Resolution | FPS | Codec | Max Duration |
|----------|-----------|-----|-------|-------------|
| YouTube | 1920x1080 / 3840x2160 | 24/30/60 | H.264/H.265 | 12h |
| TikTok | 1080x1920 | 30 | H.264 | 10min |
| Instagram Reels | 1080x1920 | 30 | H.264 | 90s |
| LinkedIn | 1920x1080 | 30 | H.264 | 10min |
| Twitter/X | 1920x1080 | 30/60 | H.264 | 2m20s |
| Web/Embed | 1920x1080 | 30 | H.264/VP9 | Unlimited |

### Audio Standards
- Sample rate: 44100 Hz or 48000 Hz
- Codec: AAC (libvo_aacenc or native)
- Bitrate: 192-320 kbps for final, 128 kbps for web
- Loudness: -14 LUFS (streaming), -24 LUFS (broadcast)
- Always normalize audio before mixing

### Color & Style
```
Background:     #010825 (dark) / #FAFAFA (light)
Accent:         #715CF7
Gradient:       #733CFA → #2C21FF
Text:           #FFFFFF (on dark) / #1A1A2E (on light)
Lower thirds:   Semi-transparent dark with accent border
Transitions:    Fade (0.3-0.5s), Cross-dissolve, Slide
```

### Motion Principles
- Ease-in-out for most transitions (not linear)
- Entrance animations: fade-up, scale-in, slide-in
- Exit animations: fade-out, scale-down, slide-out
- Text: appear word-by-word or line-by-line (0.15-0.3s per element)
- Data: count-up animations for numbers
- Duration: 0.3-0.6s for micro-animations, 1-2s for scene transitions

## Workflow

1. **Script & storyboard** — write narration, plan visuals per section
2. **Choose framework** — FFmpeg (quick edits), Remotion (React/data), MoviePy (Python/assembly), Manim (technical)
3. **Create assets** — backgrounds, images, audio
4. **Build timeline** — assemble clips, add transitions, overlay text
5. **Add audio** — narration, music, sound effects
6. **Export** — encode for target platform with correct specs
7. **Optimize** — check file size, quality, and platform compliance

## Batch Production

For creating multiple videos from data:

```python
# batch_videos.py
import json
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip

def batch_render(template_data_path, output_dir='output/'):
    with open(template_data_path) as f:
        items = json.load(f)

    for item in items:
        output = f"{output_dir}{item['slug']}.mp4"
        # Build video from template + item data
        # ... render logic ...
        print(f"Rendered: {output}")

# Use Remotion for React-based batch:
# npx remotion batch src/index.ts --config batch-config.json
```

## Anti-Patterns

- **No audio normalization** — always normalize to target LUFS
- **Linear easing on all motion** — use ease-in-out curves
- **Wall of text on screen** — max 8 words per text overlay
- **No lower thirds** — always identify speakers and data sources
- **Oversized files** — use CRF 23 for web, CRF 18 for archival
- **Wrong aspect ratio** — always match target platform specs