#!/usr/bin/env python3
"""Full-screen end card (CTA) over a blurred still of the scene, carrying the ORIGINAL voice.
Use when the speech does not fit in the 30 s avatar generations (e.g. the closing URL / 'link na bio').
usage: endcard.py bg_frame.png full_voice.mp3 START END out.mp4 "Line 1|line 2 (gold)|line 3" [kicker]
Lines are revealed one by one across the duration; the 2nd line is gold (use it for the URL)."""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
bg, voice, s, e, out, text = sys.argv[1:7]; kicker = sys.argv[7] if len(sys.argv) > 7 else ''
s, e = float(s), float(e); D = e - s; W, H, FPS = 720, 1280, 24
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from brand import font, ACCENT as GOLD, TEXT as CREAM, SHADE   # colors/fonts come from brand.json
SERIF = font('font_serif', 52); SANSB = font('font_sans_bold', 26)
b = Image.open(bg).convert('RGB').resize((int(W * 1.1), int(H * 1.1))).filter(ImageFilter.GaussianBlur(18))
b = Image.blend(b, Image.new('RGB', b.size, SHADE), 0.55)
lines = text.split('|')
p = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-ss', str(s), '-t', str(D), '-i', voice, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
                      '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-af', 'afade=t=in:d=0.03,apad', '-shortest', out], stdin=subprocess.PIPE)
ease = lambda x: 1 - (1 - max(0, min(1, x))) ** 3
for i in range(int(D * FPS)):
    t = i / FPS; z = 1 + 0.04 * t / D; cw, ch = int(W * 1.1 / z), int(H * 1.1 / z)
    fr = b.crop(((b.width - cw) // 2, (b.height - ch) // 2, (b.width + cw) // 2, (b.height + ch) // 2)).resize((W, H)).convert('RGBA')
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if kicker: d.text((W / 2, 470), kicker, font=SANSB, fill=GOLD + (int(255 * ease(t / 0.5)),), anchor='mm')
    for k, ln in enumerate(lines):
        st = k * min(1.2, D / (len(lines) + 1)); a = ease((t - st) / 0.5)
        if t < st: continue
        d.text((W / 2, 560 + k * 92 + (1 - a) * 20), ln, font=SERIF, fill=(GOLD if k == 1 else CREAM) + (int(255 * a),), anchor='mm')
    fo = min(1, (D - t) / 0.4)
    fr.alpha_composite(L); fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, fo) if fo < 1 else fr
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print('saved', out)
