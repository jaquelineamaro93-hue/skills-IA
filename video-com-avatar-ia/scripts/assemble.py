#!/usr/bin/env python3
"""Interleave pieces of one or more avatar generations (each already voice-synced by voice_sync.py),
add overlay cards on chosen pieces, concatenate and mix low background music.
usage: assemble.py plan.json
plan.json:
{
 "clips": {"A": {"video": "out/A.mp4", "fit": "out/A_fit.wav"},      # fit.wav.cuts.json must exist
           "B": {"video": "out/B.mp4", "fit": "out/B_fit.wav"}},
 "timeline": [ {"clip": "A", "range": 0},
               {"clip": "B", "range": 0, "overlay": "sc/chat.json", "scene_voice_start": 11.0},
               {"clip": "A", "range": 1},
               {"file": "out/endcard.mp4"} ],
 "music": "music.wav", "music_volume": 0.11,
 "out": "final/video.mp4"
}
"range" j = j-th spoken range given to voice_sync for that clip (video span cuts[j]..cuts[j+1]).
"scene_voice_start" = time in the FULL voice file where the overlay scene's t=0 should land (keeps cards in sync with speech).
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overlay_cards import apply
sh = lambda c: subprocess.run(c, shell=True, check=True)
P = json.load(open(sys.argv[1])); work = os.path.splitext(P['out'])[0] + '_parts'; os.makedirs(work, exist_ok=True)
os.makedirs(os.path.dirname(P['out']) or '.', exist_ok=True)
parts = []
for n, it in enumerate(P['timeline']):
    if it.get('file'):   # ready-made piece (e.g. endcard.py output), 720x1280 24fps with audio
        p = f'{work}/p{n}.mp4'
        sh(f'ffmpeg -nostdin -v error -y -i "{it["file"]}" -vf "fps=24,scale=720:1280,setsar=1" -af "afade=t=in:d=0.01" -c:v libx264 -crf 17 -preset fast -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 "{p}"')
        parts.append(p); continue
    C = P['clips'][it['clip']]; cj = json.load(open(C['fit'] + '.cuts.json')); j = it['range']
    a, b = cj['cuts'][j], cj['cuts'][j + 1]; p = f'{work}/p{n}.mp4'
    sh(f'ffmpeg -nostdin -v error -y -ss {a:.3f} -to {b:.3f} -i "{C["video"]}" -ss {a:.3f} -to {b:.3f} -i "{C["fit"]}" -map 0:v -map 1:a '
       f'-vf "fps=24,scale=720:1280,setsar=1" -af "aresample=48000,apad,afade=t=in:d=0.01,afade=t=out:st={max(0, b - a - 0.012):.3f}:d=0.01" -shortest -c:v libx264 -crf 17 -preset fast -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 "{p}"')
    if it.get('overlay'):
        g, o = cj['firsts'][str(j)]
        t0 = (o - it.get('scene_voice_start', o)) - (g - a)
        q = f'{work}/p{n}_ov.mp4'; apply(p, json.load(open(it['overlay'])), q, t0); p = q
    parts.append(p)
lst = f'{work}/list.txt'; open(lst, 'w').write(''.join(f"file '{os.path.abspath(x)}'\n" for x in parts))
cat = f'{work}/cat.mp4'
sh(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i "{lst}" -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -c:a aac -ar 48000 "{cat}"')
D = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', cat]))
if P.get('music'):
    v = P.get('music_volume', 0.11); fo = max(0, D - 1.8)
    # duration=first + normalize=0: never let amix shorten the voice / cut the CTA
    sh(f'ffmpeg -nostdin -v error -y -i "{cat}" -stream_loop -1 -i "{P["music"]}" -filter_complex '
       f'"[1:a]aresample=48000,atrim=0:{D:.3f},asetpts=PTS-STARTPTS,volume={v},afade=t=in:d=0.5,afade=t=out:st={fo:.2f}:d=1.8[m];'
       f'[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "{P["out"]}"')
else:
    sh(f'ffmpeg -nostdin -v error -y -i "{cat}" -c copy -movflags +faststart "{P["out"]}"')
print('final', P['out'], round(D, 2), 's')
