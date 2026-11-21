#!/usr/bin/env python3
"""Composite the gta6-meme-x-01 meme:
- base scene (AI-generated, no text) -> meme.png
- make.fun press-kit ghost mark pasted in the room (upper-left, floating)
- on-screen download joke drawn on the monitor: GTA VI + 99% bar + TIME REMAINING: 13 YEARS
All text drawn with PIL (guaranteed spelling), all coordinates as fractions of image size.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/hatch/workspace/makefun/gta6-meme-x-01/media-generation-meme-base-0-827b678e-a77a-4aa1-9f98-c82256668ad7.webp"
MARK = "/home/hatch/workspace/makefun/gta6-meme-x-01/press-mark-1024.png"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme.png"
OUT480 = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-480.png"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.open(BASE).convert("RGB")
W, H = img.size
print("base size:", W, H)

# --- ghost mark, upper-left in the room, floating over the dark window ---
# (clear of the monitor bezel and the lamp so it reads as in the room, not a sticker)
mark = Image.open(MARK).convert("RGBA")
ghost_size = int(0.175 * W)  # ~280px on 1600 -> ~84px at 480, clearly recognisable
mark = mark.resize((ghost_size, ghost_size), Image.LANCZOS)
gx, gy = int(0.055 * W), int(0.025 * H)  # top-left corner of the mark
# soft drop shadow for depth
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([gx + 10, gy + ghost_size - 28, gx + ghost_size - 6, gy + ghost_size + 6], fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(10))
img = Image.alpha_composite(img.convert("RGBA"), shadow)
img.paste(mark, (gx, gy), mark)

d = ImageDraw.Draw(img)
cx = 0.46 * W  # monitor screen centre (approx)

def text_center(y, s, font_size, fill="white", stroke=2, center_x=None):
    f = ImageFont.truetype(FONT_BOLD, int(font_size))
    d.text((cx if center_x is None else center_x, y), s, font=f, fill=fill,
           anchor="ma", stroke_width=stroke, stroke_fill="black")

# --- on-screen download joke (all kept inside the monitor screen, clear of the hair) ---
text_center(0.228 * H, "GTA VI", 0.053 * W)                       # title, top of screen
bar_x0, bar_x1 = 0.29 * W, 0.58 * W
bar_y0, bar_y1 = 0.485 * H, 0.512 * H
d.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=8,
                    outline="white", width=3)
fill_x1 = bar_x0 + 0.99 * (bar_x1 - bar_x0)
d.rounded_rectangle([bar_x0 + 3, bar_y0 + 3, fill_x1, bar_y1 - 3], radius=6,
                    fill="#38bdf8")
f99 = ImageFont.truetype(FONT_BOLD, int(0.019 * W))
d.text((bar_x1 - 12, (bar_y0 + bar_y1) / 2), "99%", font=f99, fill="#0b2537",
       anchor="rm")
text_center(0.525 * H, "TIME REMAINING: 13 YEARS", 0.025 * W, stroke=1,
            center_x=0.44 * W)  # punchline, shifted left clear of the hair

img.convert("RGB").save(OUT, "PNG")
img.convert("RGB").resize((480, 480), Image.LANCZOS).save(OUT480, "PNG")
print("saved", OUT, "and", OUT480)
