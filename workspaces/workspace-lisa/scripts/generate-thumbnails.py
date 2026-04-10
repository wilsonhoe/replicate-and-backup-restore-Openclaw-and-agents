#!/usr/bin/env python3
"""Generate product thumbnails for Gumroad store using PIL/Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace-lisa/assets/thumbnails")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG_COLOR = (1, 8, 37)        # #010825
ACCENT = (113, 92, 247)      # #715CF7
ACCENT_LIGHT = (140, 120, 255)
WHITE = (255, 255, 255)
GRAY = (180, 180, 200)
DARK_ACCENT = (60, 50, 160)

SIZE = (1024, 1024)


def get_font(size, bold=False):
    """Try to load a nice font, fallback to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    if fill:
        draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
        draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
        draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
        draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
        draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=width)
        draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=width)
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline, width=width)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline, width=width)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline, width=width)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline, width=width)


def draw_dashboard_widgets(draw, center_x, center_y):
    """Draw stylized dashboard widgets for Finance Dashboard."""
    # Chart area (bar chart)
    chart_x, chart_y = center_x - 200, center_y - 80
    draw_rounded_rect(draw, (chart_x, chart_y, chart_x + 180, chart_y + 120), 8, fill=(20, 25, 60))
    # Bars
    bar_heights = [40, 65, 50, 80, 55, 70]
    bar_w = 18
    for i, h in enumerate(bar_heights):
        bx = chart_x + 15 + i * 27
        by = chart_y + 110 - h
        color = ACCENT if i % 2 == 0 else ACCENT_LIGHT
        draw_rounded_rect(draw, (bx, by, bx + bar_w, chart_y + 110), 3, fill=color)
    
    # Metric cards
    for j, (label, val) in enumerate([("Net Worth", "$124K"), ("Savings", "$8.2K"), ("ROI", "+18%")]):
        cx = center_x + 10 + j * 70
        cy = center_y - 90
        draw_rounded_rect(draw, (cx, cy, cx + 60, cy + 50), 6, fill=(20, 25, 60))
        font_s = get_font(9)
        font_v = get_font(11, bold=True)
        draw.text((cx + 5, cy + 5), label, fill=GRAY, font=font_s)
        draw.text((cx + 5, cy + 22), val, fill=WHITE, font=font_v)
    
    # Pie chart
    pie_x, pie_y = center_x + 120, center_y + 20
    draw_rounded_rect(draw, (pie_x, pie_y, pie_x + 100, pie_y + 80), 6, fill=(20, 25, 60))
    draw.ellipse([pie_x + 15, pie_y + 10, pie_x + 65, pie_y + 60], fill=ACCENT, outline=ACCENT_LIGHT)
    draw.pieslice([pie_x + 15, pie_y + 10, pie_x + 65, pie_y + 60], 0, 130, fill=ACCENT_LIGHT)
    draw.pieslice([pie_x + 15, pie_y + 10, pie_x + 65, pie_y + 60], 130, 200, fill=(80, 70, 200))


def draw_calendar_widgets(draw, center_x, center_y):
    """Draw stylized calendar widgets for Content Calendar."""
    # Calendar grid
    cal_x, cal_y = center_x - 180, center_y - 80
    draw_rounded_rect(draw, (cal_x, cal_y, cal_x + 200, cal_y + 160), 8, fill=(20, 25, 60))
    
    font_s = get_font(9)
    # Days header
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for i, d in enumerate(days):
        dx = cal_x + 12 + i * 26
        draw.text((dx, cal_y + 10), d, fill=GRAY, font=font_s)
    
    # Calendar cells with some highlighted
    for row in range(4):
        for col in range(7):
            cx = cal_x + 12 + col * 26
            cy = cal_y + 30 + row * 28
            cell_num = row * 7 + col + 1
            if cell_num <= 28:
                if cell_num in [3, 7, 12, 18, 22, 25]:
                    draw_rounded_rect(draw, (cx - 2, cy - 2, cx + 22, cy + 22), 4, fill=ACCENT)
                    draw.text((cx + 4, cy + 2), str(cell_num), fill=WHITE, font=font_s)
                else:
                    draw.text((cx + 4, cy + 2), str(cell_num), fill=GRAY, font=font_s)
    
    # Post cards
    for i, (platform, time) in enumerate([("Twitter", "9:00 AM"), ("LinkedIn", "12:00 PM"), ("IG", "6:00 PM")]):
        cx = center_x + 50
        cy = center_y - 70 + i * 55
        draw_rounded_rect(draw, (cx, cy, cx + 130, cy + 45), 6, fill=(20, 25, 60))
        draw.ellipse((cx + 8, cy + 8, cx + 30, cy + 30), fill=ACCENT if i != 1 else ACCENT_LIGHT)
        font_b = get_font(11, bold=True)
        font_s2 = get_font(9)
        draw.text((cx + 36, cy + 5), platform, fill=WHITE, font=font_b)
        draw.text((cx + 36, cy + 24), time, fill=GRAY, font=font_s2)


def draw_bundle_icons(draw, center_x, center_y):
    """Draw two template icons connected for Business Bundle."""
    # Left card (Finance)
    lx = center_x - 140
    draw_rounded_rect(draw, (lx, center_y - 50, lx + 120, center_y + 50), 10, fill=(20, 25, 60), outline=ACCENT, width=2)
    font_icon = get_font(28, bold=True)
    draw.text((lx + 40, center_y - 25), "📊", fill=WHITE, font=get_font(24))
    font_label = get_font(10, bold=True)
    draw.text((lx + 15, center_y + 10), "Finance", fill=WHITE, font=font_label)
    
    # Right card (Calendar)
    rx = center_x + 20
    draw_rounded_rect(draw, (rx, center_y - 50, rx + 120, center_y + 50), 10, fill=(20, 25, 60), outline=ACCENT_LIGHT, width=2)
    draw.text((rx + 40, center_y - 25), "📅", fill=WHITE, font=get_font(24))
    draw.text((rx + 12, center_y + 10), "Calendar", fill=WHITE, font=font_label)
    
    # Connection line
    draw.line([(lx + 120, center_y), (rx, center_y)], fill=ACCENT, width=3)
    # Bundle badge
    bx = center_x - 30
    by = center_y - 70
    draw_rounded_rect(draw, (bx, by, bx + 60, by + 24), 12, fill=ACCENT)
    draw.text((bx + 6, by + 3), "BUNDLE", fill=WHITE, font=get_font(12, bold=True))


def create_thumbnail(name, title, subtitle, price, draw_func):
    img = Image.new("RGB", SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Background accent glow (top-right)
    for r in range(300, 0, -3):
        alpha = max(0, min(60, 60 - r // 5))
        color = (ACCENT[0] * alpha // 100, ACCENT[1] * alpha // 100, ACCENT[2] * alpha // 100)
        draw.ellipse([724 - r, -100 - r, 724 + r, -100 + r], fill=color)
    
    # Background accent glow (bottom-left)
    for r in range(200, 0, -3):
        alpha = max(0, min(40, 40 - r // 5))
        color = (ACCENT[0] * alpha // 100, ACCENT[1] * alpha // 100, ACCENT[2] * alpha // 100)
        draw.ellipse([-50 - r, 900 - r, -50 + r, 900 + r], fill=color)
    
    # Top bar
    draw_rounded_rect(draw, (40, 30, 984, 80), 10, fill=(20, 25, 60))
    draw.text((60, 40), "✨ NOTION TEMPLATE", fill=ACCENT, font=get_font(22, bold=True))
    draw.text((780, 42), price, fill=WHITE, font=get_font(24, bold=True))
    
    # Title
    font_title = get_font(52, bold=True)
    # Word wrap for title
    words = title.split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        bbox = draw.textbbox((0, 0), test, font=font_title)
        if bbox[2] - bbox[0] > 900:
            lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)
    
    y = 120
    for line in lines:
        draw.text((60, y), line, fill=WHITE, font=font_title)
        y += 65
    
    # Subtitle
    draw.text((60, y + 10), subtitle, fill=GRAY, font=get_font(20))
    
    # Central widget area
    draw_func(draw, 512, 520)
    
    # Bottom features bar
    draw_rounded_rect(draw, (40, 870, 984, 990), 10, fill=(20, 25, 60))
    features = ["✓ Instant Download", "✓ Lifetime Updates", "✓ Mobile Friendly"]
    font_feat = get_font(16)
    for i, feat in enumerate(features):
        fx = 70 + i * 310
        draw.text((fx, 905), feat, fill=GRAY, font=font_feat)
    
    # Bottom CTA
    draw_rounded_rect(draw, (340, 930, 684, 978), 12, fill=ACCENT)
    draw.text((370, 938), "Get Template →", fill=WHITE, font=get_font(22, bold=True))
    
    filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(filepath, "PNG", quality=95)
    print(f"✅ Saved: {filepath}")
    return filepath


if __name__ == "__main__":
    create_thumbnail(
        "finance-dashboard",
        "Finance Dashboard",
        "Automated Wealth Tracking System",
        "$39",
        draw_dashboard_widgets
    )
    
    create_thumbnail(
        "content-calendar",
        "Content Calendar",
        "Social Media Planning System",
        "$29",
        draw_calendar_widgets
    )
    
    create_thumbnail(
        "business-bundle",
        "Business Bundle",
        "Dashboard + Calendar — Save $9",
        "$59",
        draw_bundle_icons
    )
    
    print("\n🎨 All thumbnails generated!")