#!/usr/bin/env python3
"""QA of a finished video: contact sheet + local transcript of the whole file and of the last 8 s (CTA),
plus click detection on the audio. usage: qa_check.py final.mp4 [--lang pt]
Outputs <video>_qa.jpg and prints transcript tail. Look at the sheet: identity, eyebrows, accessories, background, cards."""
import sys, os, subprocess, json
import numpy as np
from PIL import Image
v = sys.argv[1]; lang = sys.argv[sys.argv.index('--lang') + 1] if '--lang' in sys.argv else 'pt'
HERE = os.path.dirname(os.path.abspath(__file__))
D = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v]))
QP = os.path.splitext(v)[0] + '_qa_frame.png'
ts = np.linspace(1, D - 1, 8); S = Image.new('RGB', (8 * 240, 427))
for i, t in enumerate(ts):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1', '-vf', 'scale=240:427', QP], check=True)
    S.paste(Image.open(QP), (i * 240, 0))
S.save(os.path.splitext(v)[0] + '_qa.jpg', quality=88)
w = os.path.splitext(v)[0] + '_qa.wav'; subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', v, '-vn', '-ac', '1', '-ar', '16000', w], check=True)
sr = 16000; y = np.frombuffer(subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', w, '-f', 's16le', '-'], capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768
# joins: the points where assemble.py glued parts (read from <out>_parts/list.txt). A join "clicks" when the jump
# right at the join is much bigger than the normal sample-to-sample movement around it.
joins, lst = [], os.path.splitext(v)[0] + '_parts/list.txt'
if os.path.exists(lst):
    t = 0.0
    for ln in open(lst).read().split('\n')[:-2]:
        t += float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ln[6:-1]])); joins.append(t)
d = np.abs(np.diff(y)); bad = []
for t in joins:
    i = int(t * sr); near = d[max(0, i - 8):i + 8].max(); ctx = np.percentile(d[max(0, i - 1600):i + 1600], 99.5) + 1e-4
    if near > 0.05 and near > 1.5 * ctx: bad.append(round(t, 2))   # ~0.5% false alarms on natural speech
print('duration', round(D, 2), '| joins', [round(t, 2) for t in joins], '| clicking joins:', bad or 'none')
subprocess.run([sys.executable, f'{HERE}/words.py', '--lang', lang, w], check=True, stdout=subprocess.DEVNULL)
W = json.load(open(w + '.words.json'))
print('FULL :', ' '.join(x['w'] for x in W))
print('END  :', ' '.join(x['w'] for x in W if x['s'] > D - 8))
os.remove(QP)
print('sheet:', os.path.splitext(v)[0] + '_qa.jpg')
