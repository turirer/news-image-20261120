#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Written from scratch for the make.fun news-image-20261120 bounty.
No network, no AI image generation: every pixel is drawn here with PIL.
Run: python3 build_image.py  ->  writes entry.png next to this file.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"

# Palette: paper, navy masthead, gold rule, ink, muted grey.
PAPER = (247, 243, 233)
NAVY = (13, 32, 66)
NAVY2 = (28, 58, 112)
GOLD = (198, 152, 48)
INK = (24, 24, 24)
MUTED = (96, 96, 96)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
RULE = (178, 172, 156)
RED = (158, 28, 28)

STORIES = [
    # (kicker, headline, deck, accent colour, icon key)
    ("SUMMIT  •  SHENZHEN",
     "Trump, Putin and Xi hold first three-way summit",
     "A joint \u2018peace declaration\u2019 from Shenzhen.",
     NAVY2, "globe"),
    ("TECH  •  MARKETS",
     "Anthropic lists \u2014 first purely AI company on the stock market",
     "Shares soar on day one; valued near $2 trillion.",
     (0, 110, 70), "bars"),
    ("DIPLOMACY  •  BERLIN",
     "Europe ready for talks with Russia to end the Ukraine war",
     "Leaders signal talks after the Berlin meeting.",
     (120, 40, 90), "dome"),
    ("CONFLICT  •  GULF",
     "Tanker hit by mine east of the Strait of Hormuz",
     "Houthi missile hits Riyadh\u2019s tallest tower.",
     (140, 40, 40), "ship"),
    ("MARKETS  •  SLIDE",
     "S&P 500 falls 2% for a fifth straight loss",
     "Japan\u2019s Nikkei drops 4.68%.",
     (178, 34, 34), "down"),
    ("CLIMATE  •  COP31",
     "Fossil fuels dropped from COP31 draft deal",
     "Final deadline nears as talks enter the endgame.",
     (0, 100, 60), "leaf"),
    ("WAR  •  UKRAINE",
     "Ukraine hits Crimean Bridge for a third time in four days",
     "Kyiv hit by ballistic missiles.",
     NAVY2, "bridge"),
    ("WEATHER  •  INDIA",
     "India evacuates 80,000+ as tropical storm Dana nears",
     "Storm Dana approaches the coast.",
     (40, 90, 140), "storm"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, max_px):
    """Wrap text to the given pixel width using stdlib textwrap."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_px or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def icon(draw, key, cx, cy, colour):
    """Minimal geometric mark for a story, centred on (cx, cy)."""
    if key == "globe":
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=colour, width=3)
        draw.line([cx - 20, cy, cx + 20, cy], fill=colour, width=2)
        draw.arc([cx - 9, cy - 20, cx + 9, cy + 20], 270, 90, fill=colour, width=2)
        draw.arc([cx - 9, cy - 20, cx + 9, cy + 20], 90, 270, fill=colour, width=2)
    elif key == "bars":
        for i, h in enumerate((12, 22, 16, 28)):
            x0 = cx - 20 + i * 11
            draw.rectangle([x0, cy + 14 - h, x0 + 7, cy + 14], fill=colour)
    elif key == "dome":
        draw.arc([cx - 20, cy - 6, cx + 20, cy + 26], 180, 360, fill=colour, width=3)
        draw.line([cx - 22, cy + 10, cx + 22, cy + 10], fill=colour, width=3)
        draw.line([cx, cy - 16, cx, cy - 6], fill=colour, width=3)
    elif key == "ship":
        draw.polygon([(cx - 22, cy + 2), (cx + 22, cy + 2),
                      (cx + 14, cy + 16), (cx - 14, cy + 16)], fill=colour)
        draw.line([cx - 2, cy - 18, cx - 2, cy + 2], fill=colour, width=3)
        draw.polygon([(cx - 2, cy - 18), (cx + 12, cy - 10), (cx - 2, cy - 6)],
                     fill=colour)
    elif key == "down":
        draw.line([cx, cy - 18, cx, cy + 14], fill=colour, width=4)
        draw.polygon([(cx - 10, cy + 2), (cx + 10, cy + 2), (cx, cy + 18)],
                     fill=colour)
    elif key == "leaf":
        draw.ellipse([cx - 16, cy - 18, cx + 16, cy + 14], outline=colour, width=3)
        draw.line([cx, cy + 14, cx, cy - 18], fill=colour, width=2)
    elif key == "bridge":
        draw.arc([cx - 22, cy - 14, cx + 22, cy + 18], 180, 360, fill=colour, width=3)
        draw.line([cx - 22, cy + 2, cx - 22, cy + 16], fill=colour, width=3)
        draw.line([cx + 22, cy + 2, cx + 22, cy + 16], fill=colour, width=3)
    elif key == "storm":
        draw.ellipse([cx - 20, cy - 8, cx + 2, cy + 10], outline=colour, width=3)
        draw.ellipse([cx - 4, cy - 16, cx + 20, cy + 4], outline=colour, width=3)
        for dx in (-12, 0, 12):
            draw.line([cx + dx, cy + 14, cx + dx - 3, cy + 22], fill=colour, width=3)
    elif key == "scales":
        draw.line([cx, cy - 20, cx, cy + 18], fill=colour, width=3)
        draw.line([cx - 18, cy - 14, cx + 18, cy - 14], fill=colour, width=3)
        draw.polygon([(cx - 22, cy - 6), (cx - 14, cy - 6), (cx - 18, cy + 4)],
                     outline=colour)
        draw.polygon([(cx + 14, cy - 6), (cx + 22, cy - 6), (cx + 18, cy + 4)],
                     outline=colour)


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, SIZE, 148], fill=NAVY)
    d.rectangle([0, 148, SIZE, 154], fill=GOLD)
    d.text((28, 14), "THE WORLD IN ONE DAY", font=font(SANS_B, 24), fill=GOLD)
    d.text((26, 44), "FRIDAY 20 NOVEMBER 2026", font=font(SERIF_B, 48), fill=WHITE)
    d.text((28, 112), "Nine stories from one day  \u2022  courts, summits, markets, war, climate",
           font=font(SANS, 21), fill=(200, 210, 225))

    # Hero story: the ICJ genocide ruling.
    hx, hy, hw, hh = 24, 168, 976, 168
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(226, 236, 247),
                outline=NAVY, width=3)
    icon(d, "scales", hx + 62, hy + 84, NAVY2)
    tx = hx + 118
    d.text((tx, hy + 14), "LAW  \u2022  THE HAGUE", font=font(SANS_B, 17), fill=RED)
    head_f = font(SERIF_B, 31)
    lines = fit_lines(d, "UN court: Myanmar committed genocide against the Rohingya",
                      head_f, hw - 140)
    y = draw_lines(d, tx, hy + 38, lines, head_f, INK, 36)
    d.text((tx, y + 4), "ICJ rules on the Rohingya case; a landmark genocide verdict.",
           font=font(SANS, 20), fill=MUTED)

    # Grid of the other eight stories: 2 columns x 4 rows.
    gx, gy = 24, 348
    pw, ph, gap = 482, 152, 10
    tag_f = font(SANS_B, 15)
    head_f = font(SANS_B, 21)
    cap_f = font(SANS, 16)
    for i, (kicker, headline, deck, accent, key) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=CARD, outline=RULE, width=2)
        d.rectangle([x, y, x + 8, y + ph], fill=accent)
        icon(d, key, x + 48, y + 44, accent)
        tx = x + 88
        d.text((tx, y + 10), kicker, font=tag_f, fill=accent)
        lines = fit_lines(d, headline, head_f, pw - 110)
        yy = draw_lines(d, tx, y + 32, lines, head_f, INK, 25)
        d.text((tx, yy + 3), deck, font=cap_f, fill=MUTED)

    # Footer.
    d.text((SIZE // 2, 994), "Compiled from wire reports  \u2022  20 November 2026",
           font=font(SANS, 16), fill=MUTED, anchor="ma")

    img.save(OUT)
    print(f"saved {OUT} ({SIZE}, {SIZE})")


if __name__ == "__main__":
    main()
