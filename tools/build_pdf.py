#!/usr/bin/env python3
"""Rebuild ../six-hills-cafe-menu.pdf from menu.json.

Needs: pip install reportlab pillow numpy fonttools brotli
Usage: python3 tools/build_pdf.py
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont as FT
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.lib.colors import HexColor, white

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / 'tools' / '.cache'; CACHE.mkdir(exist_ok=True)
data = json.loads((ROOT / 'tools' / 'menu.json').read_text(encoding='utf-8'))
B = data['business']

def ttf(name):
    out = CACHE / (name + '.ttf')
    if not out.exists():
        f = FT(str(ROOT / 'fonts' / (name + '.woff2'))); f.flavor = None; f.save(str(out))
    return str(out)

pdfmetrics.registerFont(TTFont('Inter', ttf('inter-latin-400-normal')))
pdfmetrics.registerFont(TTFont('InterB', ttf('inter-latin-600-normal')))
pdfmetrics.registerFont(TTFont('Play', ttf('playfair-display-latin-700-normal')))

DARK = HexColor('#3f4a21'); ACC = HexColor('#66752f'); MUTED = HexColor('#5c5e45'); CREAM = HexColor('#fbf6f0')
TINT = HexColor('#f7f5ea'); INK = HexColor('#262a12')
W, H = A4; M = 40; GAP = 24; CW = (W - 2 * M - GAP) / 2; HDR = 112

# hills artwork with the fade baked in (hidden on the left so the title stays readable)
art = np.array(Image.open(ROOT / 'images' / 'hills-art.png')).astype(float)
ramp = np.clip((np.linspace(0, 1, art.shape[1]) - 0.18) / 0.5, 0, 1); ramp = ramp * ramp * (3 - 2 * ramp)
art[..., 3] *= ramp[None, :]
ART = CACHE / 'hills-art-pdf.png'; Image.fromarray(art.astype('uint8'), 'RGBA').save(ART)

def section(c, x, y, cat):
    c.setFont('Play', 15); c.setFillColor(DARK); c.drawString(x, y, cat['title']); y -= 6
    c.setStrokeColor(ACC); c.setLineWidth(1.2); c.line(x, y, x + CW, y); y -= 14
    if cat.get('note'):
        c.setFont('Inter', 7.5); c.setFillColor(MUTED)
        for ln in simpleSplit(cat['note'].replace(' · ', ' / '), 'Inter', 7.5, CW): c.drawString(x, y, ln); y -= 10
        y -= 2
    for it in cat['items']:
        name = it['name'] + ('  (V)' if it.get('veg') else '')
        c.setFont('InterB', 9.5); c.setFillColor(INK); c.drawString(x, y, name)
        c.setFillColor(ACC); c.drawRightString(x + CW, y, it['price'].replace(' · ', ' / ')); y -= 11.5
        if it.get('desc'):
            c.setFont('Inter', 7.8); c.setFillColor(MUTED)
            for ln in simpleSplit(it['desc'], 'Inter', 7.8, CW - 55): c.drawString(x, y, ln); y -= 9.5
        y -= 5
    return y - 6

def header(c):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    steps = 60
    for i in range(steps):
        t = i / (steps - 1)
        col = '#%02x%02x%02x' % (int(0x3f + (0x66 - 0x3f) * t), int(0x4a + (0x74 - 0x4a) * t), int(0x21 + (0x33 - 0x21) * t))
        c.setFillColor(HexColor(col)); c.rect(W * i / steps, H - HDR, W / steps + 1, HDR, fill=1, stroke=0)
    ah = 106; aw = ah * art.shape[1] / art.shape[0]
    c.drawImage(ImageReader(str(ART)), W - aw + 14, H - HDR, width=aw, height=ah, mask='auto')
    c.saveState(); p = c.beginPath(); p.circle(M + 40, H - HDR / 2, 40); c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(str(ROOT / 'logo.jpeg')), M, H - HDR / 2 - 40, width=80, height=80); c.restoreState()
    c.setStrokeColor(white); c.setLineWidth(1.5); c.circle(M + 40, H - HDR / 2, 40, stroke=1, fill=0)
    c.setFillColor(white); c.setFont('Play', 28); c.drawString(M + 98, H - HDR / 2 + 2, B['name'])
    c.setFont('Inter', 10); c.setFillColor(HexColor('#fbfae8'))
    c.drawString(M + 99, H - HDR / 2 - 16, 'Menu  ·  Selston  ·  ' + B['hours'])

def footer(c, n, total):
    c.setFillColor(DARK); c.rect(0, 0, W, 38, fill=1, stroke=0)
    c.setFillColor(white); c.setFont('Inter', 8)
    c.drawCentredString(W / 2, 22, f"{B['name']}  ·  {B['address']}  ·  {B['phone']}  ·  {B['mobile']}")
    c.drawCentredString(W / 2, 11, f"{B['hours']}  ·  {B['email']}  ·  Page {n} of {total}  ·  Prices may change")

out = ROOT / 'six-hills-cafe-menu.pdf'
c = canvas.Canvas(str(out), pagesize=A4)
c.setTitle(B['name'] + ' Menu'); c.setAuthor(B['name']); c.setSubject('Menu and prices')
pages = sorted({cat['pdf']['page'] for cat in data['categories']})
for n in pages:
    header(c); top = H - HDR - 24
    if n == 1:
        f = data['feature']
        c.setFillColor(ACC); c.roundRect(M, top - 54, W - 2 * M, 54, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Play', 15); c.drawString(M + 16, top - 24, f['title'])
        c.setFont('Inter', 8.3); c.setFillColor(HexColor('#fbfae8')); c.drawString(M + 16, top - 40, f['text'])
        c.setFont('Play', 20); c.setFillColor(white); c.drawRightString(W - M - 16, top - 30, f['price'])
        top -= 54 + 26
    else:
        top -= 6
    ys = {'L': top, 'R': top}
    for cat in data['categories']:
        if cat['pdf']['page'] != n: continue
        col = cat['pdf']['col']; x = M if col == 'L' else M + CW + GAP
        ys[col] = section(c, x, ys[col], cat)
    if n == pages[-1]:
        by = min(ys.values()) - 6; a = data['allergen']
        c.setFillColor(TINT); c.roundRect(M, by - 96, W - 2 * M, 96, 8, fill=1, stroke=0)
        c.setFillColor(ACC); c.rect(M, by - 96, 5, 96, fill=1, stroke=0)
        c.setFillColor(DARK); c.setFont('Play', 12.5); c.drawString(M + 18, by - 20, a['title'])
        c.setFont('Inter', 8.3); c.setFillColor(INK); yy = by - 36
        for ln in simpleSplit(a['text'], 'Inter', 8.3, W - 2 * M - 36): c.drawString(M + 18, yy, ln); yy -= 11.5
    footer(c, n, len(pages)); c.showPage()
c.save(); print('wrote', out)
