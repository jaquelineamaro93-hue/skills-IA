#!/usr/bin/env python3
"""Lower-third overlay cards on top of the talking-head video (face stays free in the upper part).
Scene JSON types:
  chat : {"type":"chat","note":"Conversa recriada · nome preservado","msgs":[{"from":"in"|"out","t":0.0,"text":"...","cps":20}]}
         "in" = received bubble (shows typing dots 0.8 s first); "out" = typed live, char by char.
  steps: {"type":"steps","kicker":"MARCA","title":"Existe um processo","items":[{"t":1.9,"text":"..."}]}
  quote: {"type":"quote","lines":[{"t":0.3,"text":"...","gold":true}]}
Times t are seconds from scene start. CLI preview:
  overlay_cards.py scene.json frame.png T out.png
Library use: from overlay_cards import apply; apply(video_in, scene_dict, video_out, t0)
"""
import json, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 720, 1280, 24
TOP = 790
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from brand import font, ACCENT as GOLD, TEXT as CREAM, SHADE   # colors/fonts come from brand.json
SANS = lambda s: font('font_sans', s)
SANSB = lambda s: font('font_sans_bold', s)
SERIF = lambda s: font('font_serif', s)

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

def _grad(alpha_max=170, start=TOP - 140):
    g = np.zeros((H, W, 4), np.uint8)
    for y in range(start, H):
        g[y, :, 3] = int(min(1, (y - start) / 220) * alpha_max); g[y, :, :3] = SHADE
    return Image.fromarray(g, 'RGBA')
GRAD = _grad()

def chat_layer(sc, t):
    L = GRAD.copy(); d = ImageDraw.Draw(L); f = SANS(27); maxw = W * 0.74
    shown, typing_in, typed = [], False, None
    for m in sc['msgs']:
        st = m['t']
        if m['from'] == 'in':
            if t >= st + 0.8: shown.append((m, t - st - 0.8))
            elif t >= st: typing_in = True
        else:
            n = len(m['text']); cps = m.get('cps', 22); td = n / cps
            if t >= st + td + 0.3: shown.append((m, t - st - td - 0.3))
            elif t >= st: typed = m['text'][:min(n, int((t - st) * cps))]
    B = []
    for m, age in shown:
        ls = wrap(d, m['text'], f, maxw - 40)
        B.append((m['from'], age, ls, len(ls) * 37 + 30, max(d.textlength(l, font=f) for l in ls) + 42))
    if typed is not None:
        ls = wrap(d, typed + ('|' if int(t * 3) % 2 == 0 else ''), f, maxw - 40) or ['|']
        B.append(('out', 1, ls, len(ls) * 37 + 30, max(d.textlength(l, font=f) for l in ls) + 42))
    if typing_in: B.append(('typing', 0, [], 56, 100))
    if not B: return Image.new('RGBA', (W, H), (0, 0, 0, 0))   # nothing on screen yet: no shade, no note
    y = H - 120
    for who, age, ls, hg, wd in reversed(B):
        y -= hg + 14
        if y < TOP: break
        a = ease(age / 0.25); left = who in ('in', 'typing')
        x = 34 if left else W - 34 - wd; col = (255, 255, 255) if left else (217, 253, 211); yy = y + (1 - a) * 20
        sh = Image.new('RGBA', (int(wd) + 40, int(hg) + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((20, 24, wd + 20, hg + 20), 22, fill=(0, 0, 0, 70))
        L.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (int(x) - 20, int(yy) - 20))
        d.rounded_rectangle((x, yy, x + wd, yy + hg), 22, fill=col + (int(250 * a),))
        if who == 'typing':
            for i in range(3):
                ph = (math.sin(t * 8 - i) + 1) / 2
                d.ellipse((x + 22 + i * 24, yy + 22 - ph * 6, x + 36 + i * 24, yy + 36 - ph * 6), fill=(150, 150, 150, 255))
        else:
            for i, l in enumerate(ls): d.text((x + 21, yy + 14 + i * 37), l, font=f, fill=(17, 27, 33, int(255 * a)))
    note = sc.get('note', '')
    if note:
        d.rounded_rectangle((34, H - 92, 34 + d.textlength(note, font=SANS(19)) + 28, H - 58), 17, fill=(0, 0, 0, 110))
        d.text((48, H - 75), note, font=SANS(19), fill=(240, 232, 220, 255), anchor='lm')
    return L

def steps_layer(sc, t):
    L = GRAD.copy(); d = ImageDraw.Draw(L); a = ease(t / 0.5); y = TOP - 20
    if sc.get('kicker'): d.text((W / 2, y), sc['kicker'], font=SANSB(24), fill=GOLD + (int(255 * a),), anchor='mm')
    d.text((W / 2, y + 52), sc['title'], font=SERIF(46), fill=CREAM + (int(255 * a),), anchor='mm')
    for i, it in enumerate(sc['items']):
        if t < it['t']: continue
        e = ease((t - it['t']) / 0.45); yy = y + 110 + i * 112 + (1 - e) * 30
        c = Image.new('RGBA', (W - 100, 96), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle((0, 0, W - 100, 96), 24, fill=(250, 245, 236, int(238 * e)))
        cd.ellipse((20, 20, 76, 76), fill=GOLD + (int(255 * e),))
        cd.text((48, 48), str(i + 1), font=SERIF(30), fill=(255, 255, 255, int(255 * e)), anchor='mm')
        cd.text((98, 48), it['text'], font=SANSB(29), fill=(40, 30, 22, int(255 * e)), anchor='lm')
        L.alpha_composite(c, (50, int(yy)))
    return L

def quote_layer(sc, t):
    L = GRAD.copy(); d = ImageDraw.Draw(L); y = TOP + 60
    for ln in sc['lines']:
        if t < ln['t']: y += 70; continue
        e = ease((t - ln['t']) / 0.5)
        for l in wrap(d, ln['text'], SERIF(44), W - 110):
            d.text((W / 2, y + (1 - e) * 20), l, font=SERIF(44), fill=(GOLD if ln.get('gold') else CREAM) + (int(255 * e),), anchor='mm'); y += 58
        y += 24
    return L

LAY = {'chat': chat_layer, 'steps': steps_layer, 'quote': quote_layer}

def apply(video, sc, out, t0=0.0):
    D = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video]))
    rd = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-i', video, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    wr = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', video, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', out], stdin=subprocess.PIPE)
    i = 0
    while True:
        b = rd.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        t = i / FPS; fr = Image.frombytes('RGB', (W, H), b).convert('RGBA')
        Lr = LAY[sc['type']](sc, t + t0); k = min(1, t / 0.3)   # no fade-out: half-transparent cards at the cut look like a glitch
        if k < 1:
            arr = np.array(Lr); arr[..., 3] = (arr[..., 3] * k).astype(np.uint8); Lr = Image.fromarray(arr, 'RGBA')
        fr.alpha_composite(Lr); wr.stdin.write(fr.convert('RGB').tobytes()); i += 1
    wr.stdin.close(); wr.wait(); rd.wait()

if __name__ == '__main__':
    sc = json.load(open(sys.argv[1])); fr = Image.open(sys.argv[2]).convert('RGBA').resize((W, H))
    fr.alpha_composite(LAY[sc['type']](sc, float(sys.argv[3]))); fr.convert('RGB').save(sys.argv[4]); print('saved', sys.argv[4])
