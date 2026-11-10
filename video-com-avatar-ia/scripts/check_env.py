#!/usr/bin/env python3
"""Check that this machine can run the whole pipeline. usage: check_env.py [--download-model]
Prints OK / MISSING with the exact install command for each piece."""
import shutil, subprocess, sys, importlib, os
ok = True
def row(name, good, fix=''):
    global ok
    ok &= good
    print(f"{'OK     ' if good else 'MISSING'} {name}" + ('' if good else f'  ->  {fix}'))

for b, fix in [('ffmpeg', 'apt install ffmpeg | brew install ffmpeg'), ('ffprobe', 'comes with ffmpeg'),
               ('rubberband', 'apt install rubberband-cli | brew install rubberband')]:
    row(b, shutil.which(b) is not None, fix)
for m, pipn in [('numpy', 'numpy'), ('PIL', 'Pillow'), ('faster_whisper', 'faster-whisper'), ('cv2', '"opencv-python-headless<5"')]:
    try: importlib.import_module(m); good = True
    except Exception: good = False
    row(f'python: {m}', good, f'pip install {pipn}')
try:
    import cv2
    row('opencv face detector (Haar)', os.path.exists(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
        'pip install "opencv-python-headless<5"  (OpenCV 5 ships without it)')
except Exception: pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from brand import _path, B
    row('fonts: ' + ', '.join(os.path.basename(_path(B[k]) or '?') for k in ('font_serif', 'font_sans', 'font_sans_bold')),
        all(_path(B[k]) for k in ('font_serif', 'font_sans', 'font_sans_bold')),
        'apt install fonts-noto-core | or set fonts in brand.json (a DejaVu fallback is used meanwhile)')
except Exception as e: row('brand.py', False, str(e))
if '--download-model' in sys.argv:
    from faster_whisper import WhisperModel
    WhisperModel('small', device='cpu', compute_type='int8'); row('whisper model "small" downloaded', True)
print('\nREADY' if ok else '\nInstall the MISSING items, then run this again.')
