#!/usr/bin/env python3
"""
Generate per-org OG social preview images (1200×630) for atlasiran.org.

Reads all .md frontmatter from src/content/org-pages/ and outputs
static/og/op/{slug}.jpg for each.

Usage:
    python3 deploy/gen_org_og_images.py              # all orgs
    python3 deploy/gen_org_og_images.py Hengaw        # single slug (no extension)
"""

import sys
import yaml
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import arabic_reshaper
from bidi.algorithm import get_display

BASE     = Path(__file__).parent.parent
ORG_DIR  = BASE / "src/content/org-pages"
LOGO_DIR = BASE / "static/logos"
OUT_DIR  = BASE / "static/og/op"

FONT_BOLD = BASE / "static/fonts/vazirmatn/Vazirmatn-Bold.ttf"
FONT_REG  = BASE / "static/fonts/vazirmatn/Vazirmatn-Regular.ttf"
if not FONT_BOLD.exists():
    FONT_BOLD = BASE / "static/fonts/shabnam/Shabnam-Bold-FD.ttf"
    FONT_REG  = BASE / "static/fonts/shabnam/Shabnam-FD.ttf"

W, H = 1200, 630

NAVY      = (30,  58,  107)
NAVY_DARK = (18,  36,  72)
WHITE     = (244, 246, 247)
SKY       = (140, 218, 245)
GOLD      = (237, 227, 199)


# ── helpers ────────────────────────────────────────────────────────────────

def is_rtl(text: str) -> bool:
    if not text:
        return False
    rtl = sum(1 for c in text if '\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F')
    return rtl > len(text) * 0.25


def rtl_render(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


def wrap_ltr(text: str, font, max_w: int, draw: ImageDraw.ImageDraw, max_lines=2):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        if draw.textlength(test, font=font) <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(' '.join(cur))
            cur = [w]
        if len(lines) == max_lines:
            cur = []
            break
    if cur:
        lines.append(' '.join(cur))
    return lines[:max_lines]


def wrap_rtl(text: str, font, max_w: int, draw: ImageDraw.ImageDraw, max_lines=2):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test_raw = ' '.join(cur + [w])
        test_rnd = rtl_render(test_raw)
        if draw.textlength(test_rnd, font=font) <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(rtl_render(' '.join(cur)))
            cur = [w]
        if len(lines) == max_lines:
            cur = []
            break
    if cur:
        line = rtl_render(' '.join(cur))
        if len(lines) < max_lines:
            lines.append(line)
        else:
            lines[-1] = lines[-1].rstrip() + '…'
    return lines[:max_lines]


def wrap_text(text: str, font, max_w: int, draw, max_lines=2) -> list[str]:
    if is_rtl(text):
        return wrap_rtl(text, font, max_w, draw, max_lines)
    return wrap_ltr(text, font, max_w, draw, max_lines)


def render(text: str) -> str:
    if is_rtl(text):
        return rtl_render(text)
    return text


def defined(v) -> bool:
    return bool(v and str(v).strip() and str(v).strip().lower() != 'none')


def circle_logo(path: Path, size: int):
    try:
        img = Image.open(path).convert("RGBA")
        img = ImageOps.fit(img, (size, size), method=Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return img
    except Exception:
        return None


def building_icon_circle(size: int) -> Image.Image:
    """Render a building silhouette (matching the UI Building2 icon) in a circle."""
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # circle background — same muted navy-blue as the UI placeholder
    BG   = (168, 178, 200, 255)   # ~#A8B2C8
    ICON = (255, 255, 255, 220)

    draw.ellipse([0, 0, size - 1, size - 1], fill=BG)

    # scale-independent drawing grid
    m  = size * 0.18   # margin
    cx = size / 2

    # main building body (tall rectangle)
    bx0 = cx - size * 0.20
    bx1 = cx + size * 0.20
    by0 = m + size * 0.08
    by1 = size - m - size * 0.15  # leave room for ground line
    draw.rectangle([bx0, by0, bx1, by1], fill=ICON)

    # left wing (shorter)
    wx0 = m
    wx1 = bx0 - size * 0.02
    wy0 = m + size * 0.25
    wy1 = by1
    draw.rectangle([wx0, wy0, wx1, wy1], fill=ICON)

    # ground line
    gl_y = by1 + size * 0.04
    draw.rectangle([m, gl_y, size - m, gl_y + size * 0.04], fill=ICON)

    # door (cut out dark rect at bottom of main body)
    dw = size * 0.12
    dh = size * 0.16
    dx0 = cx - dw / 2
    draw.rectangle([dx0, by1 - dh, dx0 + dw, by1], fill=BG)

    # windows on main body: 2 columns × 2 rows
    ww = size * 0.09
    wh = size * 0.09
    for col_x in [cx - size * 0.12, cx + size * 0.03]:
        for row_y in [by0 + size * 0.06, by0 + size * 0.22]:
            draw.rectangle([col_x, row_y, col_x + ww, row_y + wh], fill=BG)

    # windows on left wing: 1 column × 1 row
    wlx = wx0 + (wx1 - wx0) / 2 - ww / 2
    wly = wy0 + size * 0.06
    draw.rectangle([wlx, wly, wlx + ww, wly + wh], fill=BG)

    return img


def parse_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


# ── image generator ────────────────────────────────────────────────────────

def generate(m: dict, out_path: Path) -> None:
    slug     = out_path.stem
    org_name = (m.get('name_fa') or m.get('name_en') or
                m.get('name_short') or m.get('title') or slug)
    location   = str(m.get('location',   '') or '')
    org_type   = str(m.get('org_type',   '') or '')
    expertise  = str(m.get('expertise',  '') or '')
    about      = str(m.get('about',      '') or '')
    logo_file  = str(m.get('logo',       '') or '')

    description = ''
    if defined(about):
        description = about
    else:
        seen = set()
        parts = []
        for s in [expertise, location]:
            if defined(s) and s.strip() not in seen:
                seen.add(s.strip())
                parts.append(s)
        description = ' · '.join(parts)

    # ── canvas ──────────────────────────────────────────────────
    canvas = Image.new("RGB", (W, H), NAVY)
    draw   = ImageDraw.Draw(canvas)

    # subtle right-side darkening
    for x in range(W // 2, W):
        alpha = int(40 * ((x - W // 2) / (W // 2)))
        draw.line([(x, 0), (x, H)], fill=tuple(max(0, c - alpha) for c in NAVY))

    # decorative concentric arcs top-right
    arc_cx, arc_cy = 1050, -60
    for radius, opacity in [(420, 12), (310, 18), (200, 22), (110, 28)]:
        arc_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(arc_layer).ellipse(
            [arc_cx - radius, arc_cy - radius, arc_cx + radius, arc_cy + radius],
            outline=(*GOLD, opacity), width=2
        )
        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), arc_layer).convert("RGB"))

    draw = ImageDraw.Draw(canvas)

    # gold accent bar left edge
    draw.rectangle([56, 64, 62, H - 64], fill=GOLD)

    # ── fonts ────────────────────────────────────────────────────
    f_name_lg  = ImageFont.truetype(str(FONT_BOLD), 64)
    f_name_sm  = ImageFont.truetype(str(FONT_BOLD), 44)
    f_meta     = ImageFont.truetype(str(FONT_REG),  28)
    f_desc     = ImageFont.truetype(str(FONT_REG),  24)
    f_brand_b  = ImageFont.truetype(str(FONT_BOLD), 22)
    f_brand    = ImageFont.truetype(str(FONT_REG),  21)

    # ── org logo ─────────────────────────────────────────────────
    LOGO_SIZE = 220
    LOGO_PAD  = 18
    logo_img  = None

    PLACEHOLDER = "temporary.png"
    is_real_logo = (defined(logo_file)
                    and Path(logo_file).name.lower() != PLACEHOLDER)

    if is_real_logo:
        lp = LOGO_DIR / Path(logo_file).name
        if lp.exists():
            logo_img = circle_logo(lp, LOGO_SIZE)

    if logo_img is None:
        logo_img = building_icon_circle(LOGO_SIZE)

    if logo_img:
        bg_sz = LOGO_SIZE + LOGO_PAD * 2
        bg    = Image.new("RGBA", (bg_sz, bg_sz), (0, 0, 0, 0))
        ImageDraw.Draw(bg).ellipse([0, 0, bg_sz, bg_sz], fill=(255, 255, 255, 220))
        canvas.paste(bg.convert("RGB"), (862 - LOGO_PAD, 150 - LOGO_PAD),
                     bg.split()[3])
        canvas.paste(logo_img.convert("RGB"), (862, 150),
                     logo_img.split()[3])
        draw = ImageDraw.Draw(canvas)

    # ── text layout ──────────────────────────────────────────────
    TEXT_X   = 90
    TEXT_MAX = 720 if logo_img else 1040

    name_font  = f_name_lg if len(org_name) <= 32 else f_name_sm
    name_lines = wrap_text(org_name, name_font, TEXT_MAX, draw, max_lines=2)

    LINE_NAME  = 80 if name_font == f_name_lg else 60
    LINE_META  = 42
    LINE_DESC  = 36

    has_meta = defined(location)
    has_desc = defined(description)

    total_h = (len(name_lines) * LINE_NAME
               + (LINE_META + 10 if has_meta else 0)
               + (LINE_DESC * 2 + 8 if has_desc else 0))
    y = (H - 70 - total_h) // 2   # 70 = brand bar height

    # org name
    for line in name_lines:
        draw.text((TEXT_X, y), line, font=name_font, fill=WHITE)
        y += LINE_NAME
    y += 6

    # location
    if has_meta:
        meta_parts = [render(s) for s in [location] if defined(s)]
        draw.text((TEXT_X, y), '  ·  '.join(meta_parts),
                  font=f_meta, fill=(*SKY, 210))
        y += LINE_META + 10

    # description (max 2 lines)
    if has_desc:
        desc_lines = wrap_text(description, f_desc, TEXT_MAX, draw, max_lines=2)
        for dl in desc_lines:
            draw.text((TEXT_X, y), dl, font=f_desc, fill=(*WHITE, 175))
            y += LINE_DESC

    # ── brand bar ────────────────────────────────────────────────
    bar_y = H - 68
    draw.rectangle([0, bar_y, W, H], fill=NAVY_DARK)

    site_label = rtl_render("اطلس جامعه مدنی ایران")
    draw.text((TEXT_X, bar_y + 18), site_label, font=f_brand_b, fill=(*GOLD, 220))

    url_text = "atlasiran.org"
    url_w    = draw.textlength(url_text, font=f_brand)
    draw.text((W - 60 - url_w, bar_y + 20), url_text,
              font=f_brand, fill=(*WHITE, 140))

    # ── save ─────────────────────────────────────────────────────
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(out_path), "JPEG", quality=92, optimize=True)


# ── main ───────────────────────────────────────────────────────────────────

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    if target:
        md_files = [ORG_DIR / f"{target}.md"]
        if not md_files[0].exists():
            print(f"Not found: {md_files[0]}")
            sys.exit(1)
    else:
        md_files = sorted(ORG_DIR.glob("*.md"))

    print(f"Generating {len(md_files)} OG image(s) → {OUT_DIR}/")
    errors = []

    for i, md in enumerate(md_files, 1):
        slug = md.stem
        out  = OUT_DIR / f"{slug}.jpg"
        m    = parse_frontmatter(md)
        if not m:
            print(f"  skip (no frontmatter): {slug}")
            continue
        try:
            generate(m, out)
            print(f"  [{i}/{len(md_files)}] ✓  {slug}")
        except Exception as e:
            print(f"  [{i}/{len(md_files)}] ✗  {slug}: {e}")
            errors.append((slug, str(e)))

    print(f"\nDone — {len(md_files) - len(errors)} generated, {len(errors)} errors.")
    for s, e in errors:
        print(f"  ERROR: {s}: {e}")


if __name__ == "__main__":
    main()
