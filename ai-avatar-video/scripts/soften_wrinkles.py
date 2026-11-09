#!/usr/bin/env python3
"""Soften fine facial lines (forehead, under-eye, nasolabial) on a talking-head video, face region only.
Keeps eyes, brows, lips, hair and background untouched: only LOW-amplitude skin detail is attenuated.
usage: soften_wrinkles.py in.mp4 out.mp4 [strength 0..1, default 0.75; 0.8 approved] [--preview T out.png]
needs: pip install "opencv-python-headless<5" (OpenCV 5 ships without the Haar cascades)"""
import sys, subprocess
import numpy as np, cv2

src, out = sys.argv[1], sys.argv[2]
k = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 0.75
W, H, FPS = 720, 1280, 24
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
prof = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
box = None  # EMA-smoothed (cx, cy, w)

def detect(g):
    f = casc.detectMultiScale(g, 1.1, 6, minSize=(110, 110))
    if len(f) == 0: f = prof.detectMultiScale(g, 1.1, 5, minSize=(110, 110))
    if len(f) == 0: f = prof.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(110, 110)); f = [(W - x - w, y, w, h) for x, y, w, h in f]
    if len(f) == 0: return None
    x, y, w, h = max(f, key=lambda r: r[2])
    return np.array([x + w / 2, y + h / 2, w], float)

def process(fr):
    global box
    g = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY); d = detect(g)
    if d is not None: box = d if box is None else box * 0.7 + d * 0.3
    if box is None: return fr
    cx, cy, w = box
    # face ellipse: forehead to chin, inset from hairline and ears
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (int(cx), int(cy + w * 0.0)), (int(w * 0.44), int(w * 0.66)), 0, 0, 360, 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), w * 0.06)
    # skin gate (YCrCb) so hair/background at the ellipse border is not touched much
    ycc = cv2.cvtColor(fr, cv2.COLOR_RGB2YCrCb)
    skin = cv2.inRange(ycc, (60, 135, 85), (255, 180, 135)).astype(np.float32) / 255
    skin = cv2.GaussianBlur(skin, (0, 0), 4)
    m *= skin
    f = fr.astype(np.float32)
    base = cv2.bilateralFilter(cv2.bilateralFilter(f, 0, 22, 5), 0, 26, 11)            # edge-aware low band
    det = f - base
    a = np.abs(det).max(axis=2, keepdims=True)
    keep = np.clip((a - 11) / 14, 0, 1)                  # strong edges (eyes, brows, lips) kept, faint lines reduced
    att = 1 - k * (1 - keep)
    res = base + det * att
    mm = m[..., None]
    return np.clip(f * (1 - mm) + res * mm, 0, 255).astype(np.uint8)

if '--preview' in sys.argv:
    i = sys.argv.index('--preview'); T = float(sys.argv[i + 1]); po = sys.argv[i + 2]
    b = subprocess.check_output(['ffmpeg', '-nostdin', '-v', 'error', '-ss', str(T), '-i', src, '-frames:v', '1', '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    o = process(fr); cv2.imwrite(po, cv2.cvtColor(np.hstack([fr, o]), cv2.COLOR_RGB2BGR)); print('saved', po); sys.exit()

rd = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
n = 0
while True:
    b = rd.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    wr.stdin.write(process(np.frombuffer(b, np.uint8).reshape(H, W, 3)).tobytes()); n += 1
wr.stdin.close(); wr.wait(); rd.wait(); print('saved', out, n, 'frames')
