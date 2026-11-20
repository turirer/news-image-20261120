#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261120.

A newspaper front page for Friday 20 November 2026, drawn with PIL:
masthead, one hero story, then eight panels in a 2x4 grid.
1024x1024 PNG, no network, no AI image generation (so the text is crisp).
Run: python3 build_image.py  ->  writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
NAVY = (15, 42, 74)
NAVY2 = (23, 64, 110)
INK = (20, 20, 20)
MUTED = (70, 70, 70)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)
RED = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(d, cx, cy, kind, color):
    """A coloured disc with a white pictogram, centred at (cx, cy)."""
    r = 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    w = WHITE
    if kind == "scales":  # justice / court
        d.line([cx, cy - 18, cx, cy + 18], fill=w, width=3)
        d.line([cx - 18, cy - 12, cx + 18, cy - 12], fill=w, width=3)
        d.polygon([(cx - 22, cy - 2), (cx - 14, cy - 2), (cx - 18, cy + 8)],
                  outline=w, width=2)
        d.polygon([(cx + 14, cy - 2), (cx + 22, cy - 2), (cx + 18, cy + 8)],
                  outline=w, width=2)
    elif kind == "globe":  # summit / world leaders
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=w, width=3)
        d.ellipse([cx - 8, cy - 20, cx + 8, cy + 20], outline=w, width=2)
        d.line([cx - 20, cy, cx + 20, cy], fill=w, width=2)
    elif kind == "chart":  # stock debut / rising market
        d.line([cx - 20, cy + 18, cx - 20, cy - 18], fill=w, width=3)
        d.line([cx - 20, cy + 18, cx + 22, cy + 18], fill=w, width=3)
        d.line([cx - 16, cy + 8, cx - 4, cy - 2, cx + 4, cy + 4, cx + 20, cy - 14],
               fill=w, width=4)
        d.polygon([(cx + 20, cy - 14), (cx + 12, cy - 14), (cx + 20, cy - 6)], fill=w)
    elif kind == "dome":  # diplomacy / government talks
        d.arc([cx - 16, cy - 16, cx + 16, cy + 6], 180, 360, fill=w, width=3)
        d.line([cx, cy - 22, cx, cy - 16], fill=w, width=3)
        d.rectangle([cx - 20, cy + 6, cx + 20, cy + 10], fill=w)
        for dx in (-14, -5, 4, 13):
            d.line([cx + dx, cy + 10, cx + dx, cy + 20], fill=w, width=3)
        d.line([cx - 22, cy + 20, cx + 22, cy + 20], fill=w, width=3)
    elif kind == "ship":  # tanker / gulf
        d.polygon([(cx - 22, cy + 2), (cx + 22, cy + 2), (cx + 16, cy + 18),
                   (cx - 16, cy + 18)], fill=w)
        d.rectangle([cx - 6, cy - 12, cx + 8, cy + 2], fill=w)
        d.line([cx - 24, cy + 24, cx + 24, cy + 24], fill=w, width=3)
    elif kind == "fall":  # sliding markets
        d.line([cx - 20, cy - 18, cx - 20, cy + 18], fill=w, width=3)
        d.line([cx - 20, cy + 18, cx + 22, cy + 18], fill=w, width=3)
        d.line([cx - 16, cy - 8, cx - 4, cy + 2, cx + 4, cy - 4, cx + 20, cy + 14],
               fill=w, width=4)
        d.polygon([(cx + 20, cy + 14), (cx + 12, cy + 14), (cx + 20, cy + 6)], fill=w)
    elif kind == "leaf":  # climate / COP
        d.ellipse([cx - 18, cy - 14, cx + 14, cy + 16], outline=w, width=3)
        d.line([cx - 14, cy + 12, cx + 18, cy - 14], fill=w, width=3)
        d.line([cx - 2, cy + 2, cx - 2, cy + 20], fill=w, width=3)
    elif kind == "bridge":  # Crimean Bridge
        d.arc([cx - 22, cy - 6, cx + 22, cy + 26], 180, 360, fill=w, width=4)
        d.line([cx - 22, cy + 14, cx - 22, cy + 24], fill=w, width=3)
        d.line([cx + 22, cy + 14, cx + 22, cy + 24], fill=w, width=3)
        d.line([cx, cy + 4, cx, cy + 24], fill=w, width=3)
    elif kind == "storm":  # tropical storm
        d.ellipse([cx - 20, cy - 12, cx + 2, cy + 8], outline=w, width=3)
        d.ellipse([cx - 6, cy - 18, cx + 20, cy + 6], outline=w, width=3)
        for dx in (-12, 0, 12):
            d.line([cx + dx, cy + 12, cx + dx - 3, cy + 22], fill=w, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((28, 14), "THE WORLD IN ONE DAY", font=fnt(SANS_B, 24), fill=GOLD)
    d.text((26, 44), "FRIDAY 20 NOVEMBER 2026", font=fnt(SERIF_B, 48), fill=WHITE)
    d.text((28, 112), "Nine stories from one day  •  courts, summits, markets, war, climate",
           font=fnt(SANS, 21), fill=(200, 210, 225))

    # ---- Hero: ICJ genocide ruling ----
    hx, hy, hw, hh = 24, 168, 976, 168
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(226, 236, 247),
                outline=NAVY, width=3)
    badge(d, hx + 62, hy + 84, "scales", NAVY2)
    tx = hx + 118
    d.text((tx, hy + 14), "LAW  •  THE HAGUE", font=fnt(SANS_B, 17), fill=RED)
    head = fnt(SERIF_B, 31)
    lines = wrap(d, "UN court: Myanmar committed genocide against the Rohingya",
                 head, hw - 140)
    y = block(d, tx, hy + 38, lines, head, INK, 36)
    d.text((tx, y + 4), "ICJ rules on the Rohingya case; a landmark genocide verdict.",
           font=fnt(SANS, 20), fill=MUTED)

    # ---- Grid: 8 panels, 2 cols x 4 rows ----
    stories = [
        ("SUMMIT  •  SHENZHEN", "globe", NAVY2,
         "Trump, Putin and Xi hold first three-way summit",
         "A joint 'peace declaration' from Shenzhen."),
        ("TECH  •  MARKETS", "chart", (0, 110, 70),
         "Anthropic lists — first purely AI company on the stock market",
         "Shares soar on day one; valued near $2 trillion."),
        ("DIPLOMACY  •  BERLIN", "dome", (120, 40, 90),
         "Europe ready for talks with Russia to end the Ukraine war",
         "Leaders signal talks after the Berlin meeting."),
        ("CONFLICT  •  GULF", "ship", (140, 40, 40),
         "Tanker burns after hitting a mine east of the Strait of Hormuz",
         "Houthi missile hits Riyadh's tallest tower."),
        ("MARKETS  •  SLIDE", "fall", (178, 34, 34),
         "S&P 500 falls 2% for a fifth straight loss",
         "Japan's Nikkei drops 4.68%."),
        ("CLIMATE  •  COP31", "leaf", (0, 100, 60),
         "Fossil fuels dropped from COP31 draft deal",
         "Final deadline nears as talks enter the endgame."),
        ("WAR  •  UKRAINE", "bridge", NAVY2,
         "Ukraine hits Crimean Bridge for a third time in four days",
         "Kyiv hit by ballistic missiles."),
        ("WEATHER  •  INDIA", "storm", (40, 90, 140),
         "India evacuates 80,000+ as tropical storm Dana nears",
         "Storm Dana approaches the coast."),
    ]
    gx, gy = 24, 348
    pw, ph, gap = 482, 152, 10
    f_tag = fnt(SANS_B, 15)
    f_head = fnt(SANS_B, 21)
    f_cap = fnt(SANS, 16)
    for i, (tag, kind, color, head_txt, cap) in enumerate(stories):
        col, row = i % 2, i // 2
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=WHITE,
                    outline=(180, 175, 160), width=2)
        d.rectangle([x, y, x + 8, y + ph], fill=color)
        badge(d, x + 48, y + 44, kind, color)
        tx = x + 88
        d.text((tx, y + 10), tag, font=f_tag, fill=color)
        lines = wrap(d, head_txt, f_head, pw - 110)
        yy = block(d, tx, y + 32, lines[:2], f_head, INK, 25)
        clines = wrap(d, cap, f_cap, pw - 110)
        block(d, tx, yy + 4, clines[:2], f_cap, MUTED, 19)

    # ---- Footer ----
    d.text((28, 992), "All events reported on Friday 20 November 2026.",
           font=fnt(SANS, 15), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
