#!/usr/bin/env python3
"""Generate OG social preview image for atlasiran.org"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

BASE = Path(__file__).parent.parent
INPUT  = Path("/Users/armantorkzaban/Downloads/LOGO1 (1).jpg")
OUTPUT = BASE / "static" / "og-image.jpg"
FONT_BOLD = BASE / "static/fonts/shabnam/Shabnam-Bold-FD.ttf"
FONT_REG  = BASE / "static/fonts/shabnam/Shabnam-FD.ttf"
VAZIR_BOLD = BASE / "static/fonts/vazirmatn/Vazirmatn-Bold.ttf"
VAZIR_REG  = BASE / "static/fonts/vazirmatn/Vazirmatn-Regular.ttf"

# Choose Vazirmatn if available, else fallback to Shabnam
font_bold_path = VAZIR_BOLD if VAZIR_BOLD.exists() else FONT_BOLD
font_reg_path  = VAZIR_REG  if VAZIR_REG.exists()  else FONT_REG

W, H = 1200, 630
NAVY   = (30, 58, 107)         # #1E3A6B
WHITE  = (244, 246, 247)       # #F4F6F7
SKY    = (140, 218, 245)       # #8CDAF5
WHITE_FAINT = (244, 246, 247, 140)

def rtl(text):
    return get_display(arabic_reshaper.reshape(text))

# --- Canvas ---
canvas = Image.new("RGBA", (W, H), (*NAVY, 255))

# --- Logo photo (right side) ---
logo = Image.open(INPUT).convert("RGBA")
lw, lh = logo.size
scale = max(700 / lw, H / lh)
logo = logo.resize((int(lw * scale), int(lh * scale)), Image.LANCZOS)
lw, lh = logo.size
# crop to 700x630 centred
left = (lw - 700) // 2
top  = (lh - H) // 2
logo = logo.crop((left, top, left + 700, top + H))

# Horizontal gradient mask: transparent on right → opaque on left
grad = Image.new("L", (700, H))
for x in range(700):
    # fade from fully transparent at x=700 to fully opaque at x=0
    alpha = int(255 * (1 - (x / 700) ** 0.5))
    for y in range(H):
        grad.putpixel((x, y), alpha)
logo.putalpha(grad)

canvas.paste(logo, (W - 700, 0), logo)

# --- Subtle vignette on right edge ---
# already handled by gradient

# --- Text ---
draw = ImageDraw.Draw(canvas)

font_title    = ImageFont.truetype(str(font_bold_path), 62)
font_subtitle = ImageFont.truetype(str(font_reg_path),  30)
font_url      = ImageFont.truetype(str(font_reg_path),  22)

title_text    = rtl("اطلس جامعه مدنی ایران")
subtitle_text = "Atlas of Iranian Civil Society"
url_text      = "atlasiran.org"

# Title — vertically centred in left panel (~560px wide), nudged up
tx, ty = 70, H // 2 - 90
draw.text((tx, ty), title_text, font=font_title, fill=WHITE)

# Subtitle
sx, sy = 70, ty + 82
draw.text((sx, sy), subtitle_text, font=font_subtitle, fill=SKY)

# URL
ux, uy = 70, sy + 52
draw.text((ux, uy), url_text, font=font_url, fill=(*WHITE, 140))

# --- Save ---
rgb = canvas.convert("RGB")
rgb.save(str(OUTPUT), "JPEG", quality=93)
print(f"Saved → {OUTPUT}")
