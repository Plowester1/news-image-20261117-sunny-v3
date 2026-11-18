#!/usr/bin/env python3
"""Build entry.png for the sunny v3 variant of news-image-20261117.

A 1024x1024 vertical-list front page: dark teal/slate page, serif masthead,
one hero card (Gaza) on top, then seven full-width rows, each with a
coloured left bar and a small drawn icon. All eight stories are verified
17 November 2026 news (see the story pool); only layout, palette and
order differ from other variants. Pure PIL, fully deterministic.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAGE = (11, 32, 38)        # deep teal-slate page
PANEL = (19, 47, 55)       # row fill
PANEL_EDGE = (46, 92, 102)
HERO_FILL = (16, 58, 66)   # hero card, a touch lighter
INK = (240, 246, 246)      # headline ink
SUBINK = (178, 198, 202)   # subhead ink
TEAL = (45, 190, 178)      # accent teal
MUTED = (128, 152, 158)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

# (kicker, accent, headline, subhead, icon key) — lead story first.
ITEMS = [
    ("GAZA", (52, 196, 150),
     "West presses Israel to open Gaza aid crossings",
     "UK, Australia, Canada and Italy call the situation catastrophic.",
     "aid"),
    ("MIDDLE EAST", (235, 94, 64),
     "US strikes Iran as tankers burn in Hormuz",
     "US jets hit missile sites after a fourth tanker struck a mine; "
     "Tehran warns of a \u2018huge price\u2019.",
     "flame"),
    ("EUROPE", (84, 164, 224),
     "Ukraine hits Crimean Bridge, Russia replies",
     "Kerch link closed after overnight strike; Moscow hits Kyiv bridges "
     "in reply.",
     "bridge"),
    ("HEALTH", (240, 150, 48),
     "US loses measles elimination status",
     "First time since 2000, after the worst caseload in three decades.",
     "shield"),
    ("HEALTH", (110, 200, 120),
     "WHO validates Eritrea\u2019s trachoma elimination",
     "Two-decade campaign ends trachoma as a public-health problem.",
     "eye"),
    ("ECONOMY", (196, 164, 60),
     "Japan\u2019s economy unexpectedly contracts",
     "Q3 shrinks an annualized 0.1%, surprising markets.",
     "chart"),
    ("CULTURE", (186, 124, 214),
     "Depardieu admits sexual assault, drops appeal",
     "French actor withdraws his challenge before a Paris court.",
     "gavel"),
    ("SPORTS", (232, 184, 76),
     "Tiger Woods to return in December",
     "Comeback set for the Hero World Challenge in the Bahamas.",
     "trophy"),
]


def fit_lines(draw, text, font, width, limit):
    """Greedy word wrap, capped at `limit` lines."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:limit]


def _flame(d, cx, cy, r, main, inner):
    d.polygon([
        (cx, cy - r), (cx + 0.42 * r, cy - 0.38 * r),
        (cx + 0.68 * r, cy + 0.10 * r), (cx + 0.55 * r, cy + 0.62 * r),
        (cx + 0.18 * r, cy + 0.92 * r), (cx - 0.18 * r, cy + 0.92 * r),
        (cx - 0.55 * r, cy + 0.62 * r), (cx - 0.68 * r, cy + 0.10 * r),
        (cx - 0.42 * r, cy - 0.38 * r),
    ], fill=main)
    d.polygon([
        (cx, cy - 0.35 * r), (cx + 0.30 * r, cy + 0.05 * r),
        (cx + 0.22 * r, cy + 0.55 * r), (cx, cy + 0.68 * r),
        (cx - 0.22 * r, cy + 0.55 * r), (cx - 0.30 * r, cy + 0.05 * r),
    ], fill=inner)


def _aid(d, cx, cy, r, main, inner):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=main)
    d.rectangle([cx - 0.17 * r, cy - 0.58 * r, cx + 0.17 * r, cy + 0.58 * r],
                fill=(255, 255, 255))
    d.rectangle([cx - 0.58 * r, cy - 0.17 * r, cx + 0.58 * r, cy + 0.17 * r],
                fill=(255, 255, 255))


def _bridge(d, cx, cy, r, main, inner):
    d.arc([cx - r, cy - 0.5 * r, cx + r, cy + 0.6 * r], 180, 360,
          fill=main, width=5)
    d.line([cx - r, cy + 0.6 * r, cx + r, cy + 0.6 * r], fill=main, width=5)
    for frac in (-0.5, 0.0, 0.5):
        d.line([cx + frac * r, cy - 0.05 * r, cx + frac * r, cy + 0.6 * r],
               fill=main, width=4)


def _shield(d, cx, cy, r, main, inner):
    d.polygon([
        (cx - 0.7 * r, cy - 0.7 * r), (cx + 0.7 * r, cy - 0.7 * r),
        (cx + 0.7 * r, cy + 0.15 * r), (cx, cy + 0.9 * r),
        (cx - 0.7 * r, cy + 0.15 * r),
    ], fill=main)
    d.text((cx - 0.16 * r, cy - 0.42 * r), "+", font=ImageFont.truetype(BOLD, int(0.85 * r)),
           fill=(255, 255, 255))


def _eye(d, cx, cy, r, main, inner):
    d.ellipse([cx - r, cy - 0.62 * r, cx + r, cy + 0.62 * r],
              outline=main, width=5)
    d.ellipse([cx - 0.42 * r, cy - 0.42 * r, cx + 0.42 * r, cy + 0.42 * r],
              fill=main)
    d.ellipse([cx - 0.16 * r, cy - 0.16 * r, cx + 0.16 * r, cy + 0.16 * r],
              fill=(11, 32, 38))


def _chart(d, cx, cy, r, main, inner):
    bars = [0.45, 0.8, 0.6, 1.0]
    bw = 0.34 * r
    for i, hfrac in enumerate(bars):
        x0 = cx - r + i * (2 * r / 4) + 0.06 * r
        d.rectangle([x0, cy + 0.7 * r - hfrac * 1.2 * r,
                     x0 + bw, cy + 0.7 * r], fill=main)
    d.line([cx - r, cy + 0.7 * r, cx + r, cy + 0.7 * r], fill=inner, width=3)


def _gavel(d, cx, cy, r, main, inner):
    d.rectangle([cx - 0.75 * r, cy - 0.62 * r, cx + 0.75 * r, cy - 0.12 * r],
                fill=main)
    d.rectangle([cx - 0.14 * r, cy - 0.12 * r, cx + 0.14 * r, cy + 0.85 * r],
                fill=main)
    d.rectangle([cx - 0.55 * r, cy + 0.72 * r, cx + 0.55 * r, cy + 0.95 * r],
                fill=inner)


def _trophy(d, cx, cy, r, main, inner):
    d.polygon([
        (cx - 0.55 * r, cy - 0.8 * r), (cx + 0.55 * r, cy - 0.8 * r),
        (cx + 0.35 * r, cy + 0.05 * r), (cx - 0.35 * r, cy + 0.05 * r),
    ], fill=main)
    d.arc([cx - 0.95 * r, cy - 0.8 * r, cx - 0.15 * r, cy - 0.05 * r],
          90, 270, fill=main, width=4)
    d.arc([cx + 0.15 * r, cy - 0.8 * r, cx + 0.95 * r, cy - 0.05 * r],
          270, 90, fill=main, width=4)
    d.rectangle([cx - 0.12 * r, cy + 0.05 * r, cx + 0.12 * r, cy + 0.5 * r],
                fill=main)
    d.rectangle([cx - 0.5 * r, cy + 0.5 * r, cx + 0.5 * r, cy + 0.72 * r],
                fill=main)


ICONS = {"flame": _flame, "aid": _aid, "bridge": _bridge, "shield": _shield,
         "eye": _eye, "chart": _chart, "gavel": _gavel, "trophy": _trophy}


def build():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)
    mx = 34                      # side margin
    full = W - 2 * mx            # 956

    # ---------- masthead ----------
    f_mast = ImageFont.truetype(SERIF, 58)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 18), mast,
           font=f_mast, fill=INK)
    f_date = ImageFont.truetype(BOLD, 21)
    date = "T U E S D A Y ,  1 7  N O V E M B E R  2 0 2 6"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 92), date,
           font=f_date, fill=TEAL)
    d.rectangle([mx, 126, W - mx, 129], fill=TEAL)

    f_kick = ImageFont.truetype(BOLD, 17)

    # ---------- hero: Gaza ----------
    kick, accent, head, sub, icon = ITEMS[0]
    hy, hh = 142, 168
    d.rounded_rectangle([mx, hy, mx + full, hy + hh], radius=14,
                        fill=HERO_FILL, outline=PANEL_EDGE, width=2)
    d.rounded_rectangle([mx, hy, mx + 10, hy + hh], radius=5, fill=accent)
    # big aid medallion, right side
    icx, icy, ir = mx + full - 84, hy + hh // 2, 52
    d.ellipse([icx - ir - 10, icy - ir - 10, icx + ir + 10, icy + ir + 10],
              outline=accent, width=2)
    _aid(d, icx, icy, 40, accent, None)
    tx = mx + 30
    d.text((tx, hy + 20), "LEAD  \u2022  " + kick, font=f_kick, fill=accent)
    f_hero = ImageFont.truetype(BOLD, 35)
    f_hsub = ImageFont.truetype(REG, 20)
    ty = hy + 50
    for line in fit_lines(d, head, f_hero, full - 250, 2):
        d.text((tx, ty), line, font=f_hero, fill=INK)
        ty += 43
    ty += 4
    for line in fit_lines(d, sub, f_hsub, full - 250, 2):
        d.text((tx, ty), line, font=f_hsub, fill=SUBINK)
        ty += 26

    # ---------- seven rows ----------
    f_head = ImageFont.truetype(BOLD, 25)
    f_sub = ImageFont.truetype(REG, 18)
    f_tag = ImageFont.truetype(BOLD, 15)
    row_h, gap = 86, 9
    y = hy + hh + 12
    for kick, accent, head, sub, icon in ITEMS[1:]:
        d.rounded_rectangle([mx, y, mx + full, y + row_h], radius=10,
                            fill=PANEL, outline=PANEL_EDGE, width=1)
        d.rounded_rectangle([mx, y, mx + 8, y + row_h], radius=4, fill=accent)
        # icon chip
        ccx, ccy = mx + 52, y + row_h // 2
        d.ellipse([ccx - 24, ccy - 24, ccx + 24, ccy + 24],
                  outline=accent, width=2)
        ICONS[icon](d, ccx, ccy, 16, accent, (240, 246, 246))
        tx = mx + 92
        d.text((tx, y + 11), kick, font=f_tag, fill=accent)
        d.text((tx, y + 31), head, font=f_head, fill=INK)
        d.text((tx, y + 61), sub, font=f_sub, fill=SUBINK)
        y += row_h + gap

    # ---------- footer ----------
    f_foot = ImageFont.truetype(REG, 16)
    foot = ("8 stories  \u2022  Gaza  \u2022  Iran  \u2022  Ukraine  \u2022  Measles  "
            "\u2022  Trachoma  \u2022  Japan  \u2022  Depardieu  \u2022  Woods")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 990), foot,
           font=f_foot, fill=MUTED)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
