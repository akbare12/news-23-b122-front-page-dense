"""news-23 b122 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 heroes + 10 cards + 18 ALSO. PIL only (draw.py may use PIL).
Output: entry.png 1024x1024, < 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"

def f_serif_b(s):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSerif-Bold.ttf"), s)

def f_sans(s):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans.ttf"), s)

def f_sans_b(s):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans-Bold.ttf"), s)

# palette
BLACK = (17, 17, 17)
PAPER = (250, 247, 238)
RED = (185, 28, 28)
RED_D = (153, 27, 27)
GOLD = (201, 162, 39)
GOLD_D = (160, 120, 20)
NAVY = (27, 42, 74)
GREEN = (30, 107, 58)
CREAM = (245, 239, 224)
GREY = (90, 90, 90)
LINE = (200, 195, 180)
WHITE = (255, 255, 255)
TEAL = (14, 116, 116)
PURPLE = (107, 33, 168)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, text, fill=NAVY, fg=WHITE, size=9):
    ft = f_sans_b(size)
    tw = d.textlength(text, font=ft)
    d.rounded_rectangle([x, y, x + tw + 10, y + 14], radius=2, fill=fill)
    d.text((x + 5, y + 2), text, font=ft, fill=fg)
    return x + tw + 10

def chip_claim(x, y):
    return chip(x, y, "CLAIM", fill=RED)

# ---------- masthead ----------
d.rectangle([0, 0, W, 52], fill=BLACK)
d.text((14, 6), "THE WORLD TODAY", font=f_serif_b(34), fill=WHITE)
d.text((W - 14 - d.textlength("MONDAY 23 NOVEMBER 2026", font=f_sans_b(16)),
        16), "MONDAY 23 NOVEMBER 2026", font=f_sans_b(16), fill=GOLD)

# ---------- kicker ----------
d.rectangle([0, 52, W, 72], fill=RED)
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text(((W - d.textlength(kick, font=f_sans_b(14))) / 2, 56), kick,
       font=f_sans_b(14), fill=WHITE)

# ---------- number strip: 2 rows x 5 ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
col_w = 204
for i, (val, lab) in enumerate(nums):
    cx = 10 + (i % 5) * col_w
    cy = 78 if i < 5 else 116
    d.text((cx, cy), val, font=f_sans_b(20), fill=BLACK)
    d.text((cx, cy + 24), lab, font=f_sans(10), fill=GREY)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", TEAL),
           ("EUROPE 5", PURPLE), ("AFRICA 3", GREEN), ("WORLD 2", (90, 90, 90))]
rx = 0
seg_w = [190, 150, 190, 130, 130, 234]
for (label, col), wseg in zip(regions, seg_w):
    d.rectangle([rx, 152, rx + wseg, 170], fill=col)
    d.text((rx + 8, 156), label, font=f_sans_b(11), fill=WHITE)
    rx += wseg

# ---------- THE DAY IN UTC strip ----------
d.text((10, 174), "THE DAY IN UTC", font=f_sans_b(10), fill=BLACK)
utc = "~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles"
d.text((150, 174), utc, font=f_sans(10), fill=GREY)
d.text((W - 10 - d.textlength("~ APPROX", font=f_sans(10)), 174),
       "~ APPROX", font=f_sans(10), fill=GREY)

# ---------- hero scenes ----------
HX = [8, 348, 688]
HW = 328
SY, SH = 190, 142

# scene 1: Kospi skyline + falling chart (navy)
x0 = HX[0]
d.rectangle([x0, SY, x0 + HW, SY + SH], fill=NAVY)
# buildings with lit windows
import random
random.seed(122)
bx = x0 + 8
while bx < x0 + HW - 14:
    bw = random.randint(18, 30)
    bh = random.randint(35, 78)
    d.rectangle([bx, SY + SH - 18 - bh, bx + bw, SY + SH - 18], fill=(38, 58, 100))
    for wy in range(SY + SH - 18 - bh + 5, SY + SH - 22, 10):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    bx += bw + 4
# falling orange chart line, routed to the right of the big number
pts = [(x0 + 130, SY + 62), (x0 + 165, SY + 74), (x0 + 200, SY + 70),
       (x0 + 235, SY + 88), (x0 + 270, SY + 84), (x0 + 305, SY + 102)]
d.line(pts, fill=(255, 140, 40), width=3)
for (px, py) in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE)
d.text((x0 + 10, SY + 8), "-3.3%", font=f_sans_b(34), fill=WHITE)
d.rectangle([x0, SY + SH - 18, x0 + HW, SY + SH], fill=(10, 18, 38))
d.text((x0 + 10, SY + SH - 16), "KOSPI 4,708.54  \u00b7  -161 PTS",
       font=f_sans_b(10), fill=WHITE)

# scene 2: Guterres (green) — big gold 150 + globe
x0 = HX[1]
d.rectangle([x0, SY, x0 + HW, SY + SH], fill=GREEN)
d.text((x0 + 12, SY + 6), "150", font=f_sans_b(46), fill=GOLD)
d.text((x0 + 12, SY + 58), "DELEGATES", font=f_sans_b(17), fill=GOLD)
d.text((x0 + 12, SY + 78), "BACK A RISK", font=f_sans_b(17), fill=GOLD)
d.text((x0 + 12, SY + 98), "FRAMEWORK", font=f_sans_b(17), fill=GOLD)
# globe, right side
gx, gy, gr = x0 + 262, SY + 66, 46
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(190, 230, 200),
          outline=(220, 240, 220), width=2)
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(90, 140, 110), width=1)
d.ellipse([gx - 18, gy - gr, gx + 18, gy + gr], outline=(90, 140, 110), width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=(90, 140, 110), width=1)
d.arc([gx - gr, gy - 24, gx + gr, gy + 24], 0, 360, fill=(90, 140, 110), width=1)

# scene 3: Power Index bars (cream)
x0 = HX[2]
d.rectangle([x0, SY, x0 + HW, SY + SH], fill=CREAM)
d.text((x0 + 10, SY + 6), "NARROWEST SINCE 2018", font=f_sans_b(12), fill=BLACK)
d.text((x0 + HW - 10 - d.textlength("GAP 5.3", font=f_sans_b(12)), SY + 6),
       "GAP 5.3", font=f_sans_b(12), fill=RED)
bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 232),
        ("40.5", "INDIA", GOLD_D, 128)]
by = SY + 30
for val, name, col, bw in bars:
    d.text((x0 + 10, by), val, font=f_sans_b(14), fill=BLACK)
    d.rectangle([x0 + 10, by + 18, x0 + 10 + bw, by + 34], fill=col)
    d.text((x0 + 16, by + 20), name, font=f_sans_b(11), fill=WHITE)
    by += 38

# hero headlines / body / source+chip
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 - gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(heroes):
    x0 = HX[i]
    hy = SY + SH + 6
    lines = wrap(head, f_sans_b(17), HW)[:2]
    for j, ln in enumerate(lines):
        d.text((x0, hy + j * 20), ln, font=f_sans_b(17), fill=BLACK)
    byy = hy + 42
    blines = wrap(body, f_sans(12), HW)[:2]
    for j, ln in enumerate(blines):
        d.text((x0, byy + j * 15), ln, font=f_sans(12), fill=(40, 40, 40))
    syy = byy + 32
    d.text((x0, syy + 2), src, font=f_sans(9), fill=GREY)
    chip(x0 + HW - 62, syy, "REPORTED")

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 410, W, 428], fill=BLACK)
d.text((10, 413), "MORE OF THE DAY  \u2014  10 STORIES", font=f_sans_b(12), fill=WHITE)

# ---------- 10 cards: 5 cols x 2 rows ----------
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", False),
    ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", False),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", False),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", False),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", False),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", False),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", False),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", False),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", True),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", True),
]
CW, CHH = 197, 68
for i, (region, head, body, src, is_claim) in enumerate(cards):
    cx = 8 + (i % 5) * 203
    cy = 432 + (i // 5) * 72
    d.rectangle([cx, cy, cx + CW, cy + CHH], outline=LINE, width=1)
    d.text((cx + 6, cy + 4), region, font=f_sans_b(9), fill=RED)
    num = str(i + 1)
    d.text((cx + CW - 8 - d.textlength(num, font=f_sans_b(10)), cy + 4),
           num, font=f_sans_b(10), fill=RED)
    hlines = wrap(head, f_sans_b(12), CW - 12)[:2]
    for j, ln in enumerate(hlines):
        d.text((cx + 6, cy + 16 + j * 13), ln, font=f_sans_b(12), fill=BLACK)
    d.text((cx + 6, cy + 45), body, font=f_sans(9), fill=(60, 60, 60))
    d.text((cx + 6, cy + 58), src, font=f_sans(8), fill=GREY)
    if is_claim:
        chip_claim(cx + CW - 52, cy + 52)
    else:
        chip(cx + CW - 72, cy + 52, "REPORTED")

# ---------- WHERE IT HAPPENED strip ----------
d.rectangle([0, 576, W, 594], fill=BLACK)
d.text((10, 579), "WHERE IT HAPPENED", font=f_sans_b(12), fill=WHITE)

# ---------- map blobs ----------
MAP_TOP = 596
# Americas blob
d.polygon([(18, 610), (120, 600), (150, 640), (140, 720), (105, 800),
           (70, 800), (40, 740), (16, 660)], fill=(190, 225, 185))
# Europe blob
d.polygon([(168, 606), (250, 600), (262, 640), (240, 676), (196, 682),
           (168, 650)], fill=(190, 225, 185))
# Africa blob
d.polygon([(180, 690), (246, 686), (258, 740), (228, 800), (196, 792),
           (178, 740)], fill=(190, 225, 185))
# Asia blob
d.polygon([(258, 600), (326, 600), (332, 660), (300, 706), (262, 690),
           (256, 640)], fill=(190, 225, 185))

pins = [
    (1, 310, 622), (2, 62, 772), (3, 296, 648), (4, 56, 668), (5, 78, 626),
    (6, 228, 622), (7, 202, 648), (8, 192, 614), (9, 240, 652),
    (10, 180, 642), (11, 280, 668), (12, 270, 690), (13, 216, 742),
]
for n, px, py in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
    t = str(n)
    d.text((px - d.textlength(t, font=f_sans_b(9)) / 2, py - 6),
           t, font=f_sans_b(9), fill=WHITE)

# map legend (4 lines)
leg = ["Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
       "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris",
       "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut",
       "12 Gaza \u00b7 13 Khartoum"]
for j, ln in enumerate(leg):
    d.text((10, 806 + j * 12), ln, font=f_sans(9), fill=GREY)

# ---------- ALSO list ----------
d.text((348, 596), "ALSO ON MONDAY", font=f_sans_b(13), fill=BLACK)
also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after Antalya pact rejected", False),
    ("18. Israel unity talks resume", False),
    ("19. Gaza: two killed in Israeli strike", False),
    ("20. West Bank settler attacks", False),
    ("21. Iran war: no deal in sight", False),
    ("22. Lebanon seizes 264 kg explosives", False),
    ("23. Bahrain: strike hits plant, 2 hurt", False),
    ("24. Benghazi: UN demands probe", True),
    ("25. Sudan: defences down drones", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if she returns", False),
    ("28. Seoul minister quits in exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
ax1, ax2 = 348, 690
for i, (txt, is_claim) in enumerate(also):
    col = ax1 if i < 9 else ax2
    ay = 616 + (i % 9) * 24
    d.text((col, ay), txt, font=f_sans(11), fill=BLACK)
    if is_claim:
        tw = d.textlength(txt, font=f_sans(11))
        d.text((col + tw + 6, ay), "[CLAIM]", font=f_sans_b(10), fill=RED)

# ---------- DATE CHECK red box ----------
d.rectangle([8, 856, W - 8, 936], outline=RED, width=2)
d.text((16, 862), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
       font=f_sans_b(12), fill=RED)
d.text((16, 882), "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro captured (22 Nov)",
       font=f_sans(11), fill=BLACK)
d.text((16, 898), "EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)",
       font=f_sans(11), fill=BLACK)
d.text((16, 916), "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=f_sans(11), fill=BLACK)

# ---------- footer ----------
d.text((10, 946), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=f_sans(9), fill=GREY)
d.text((10, 960), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing.",
       font=f_sans(9), fill=GREY)
d.text((10, 974), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=f_sans(9), fill=GREY)
foot = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(foot, font=f_sans_b(11))) / 2, 996), foot,
       font=f_sans_b(11), fill=GOLD_D)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
