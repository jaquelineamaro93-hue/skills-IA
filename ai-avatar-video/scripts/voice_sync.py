#!/usr/bin/env python3
"""Replace the AI-generated voice of an avatar clip with the ORIGINAL voice file, aligned word by word to the lips.

usage: voice_sync.py generated.mp4 original_voice.mp3 out_fit.wav [--ranges "11.0-36.9,40.2-52.0"] [--lang pt]

--ranges  the parts of the ORIGINAL voice file (seconds) that this clip speaks, in order. Omit if the clip speaks
          the whole file. Each range becomes range j for assemble.py (video span cuts[j]..cuts[j+1]).
Output:   out_fit.wav (48 kHz mono, exactly as long as the video) and out_fit.wav.cuts.json
          {"cuts": [0, ..., video_len], "firsts": {"j": [video_t, voice_t]}} (first matched word of each range).

Method (why): both audios are transcribed with word timestamps (words.py) and matched in order (difflib).
Every matched word becomes a key frame of ONE continuous Rubber Band time map per range, so the voice follows
the mouth without per-word pieces (pieces = clicks) and without global DTW (drifts ~0.5 s). Generated speech often
hallucinates words: unmatched words are simply interpolated between their neighbours.
Requires the `rubberband` CLI (apt install rubberband-cli / brew install rubberband).
"""
import sys, os, json, re, argparse, difflib, subprocess, unicodedata, shutil, tempfile, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('gen'); ap.add_argument('voice'); ap.add_argument('out')
ap.add_argument('--ranges', default=''); ap.add_argument('--lang', default='pt')
ap.add_argument('--lead', type=float, default=0.04, help='voice leads the lips by this much (s); 0.02-0.08 looks natural')
ap.add_argument('--max-rate', type=float, default=2.0, help='max speed change inside a word (pauses are free)')
A = ap.parse_args()
SR = 48000
if not shutil.which('rubberband'): sys.exit('rubberband CLI not found: apt install rubberband-cli  (macOS: brew install rubberband)')

dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
GD, VD = dur(A.gen), dur(A.voice)

def words(path):
    j = path + '.words.json'
    if not os.path.exists(j):
        subprocess.run([sys.executable, f'{HERE}/words.py', '--lang', A.lang, path], check=True, stdout=subprocess.DEVNULL)
    return json.load(open(j))

def pcm(path, t0=None, t1=None):
    cmd = ['ffmpeg', '-nostdin', '-v', 'error']
    if t0 is not None: cmd += ['-ss', f'{t0:.4f}', '-to', f'{t1:.4f}']
    raw = subprocess.run(cmd + ['-i', path, '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def wav_write(path, y):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())

G, O_all = words(A.gen), words(A.voice)
av = [tuple(map(float, r.split('-'))) for r in A.ranges.split(',') if r.strip()] or [(0.0, VD)]
O = [w for w in O_all if any(a - 0.3 <= w['s'] <= b + 0.3 for a, b in av)]
rng = lambda t: next((j for j, (a, b) in enumerate(av) if a - 0.3 <= t <= b + 0.3), len(av) - 1)
nz = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode())
sm = difflib.SequenceMatcher(None, [nz(w['w']) for w in G], [nz(w['w']) for w in O], autojunk=False)
pairs = [(G[b.a + k], O[b.b + k]) for b in sm.get_matching_blocks() for k in range(b.size)]
if len(pairs) < 3: sys.exit(f'only {len(pairs)} words matched: wrong voice file, wrong --ranges or wrong --lang?')
print(f'matched {len(pairs)} words (generated {len(G)}, original {len(O)})')

out = np.zeros(int(GD * SR) + SR, np.float32)
cuts, firsts, tmp = [0.0], {}, tempfile.mkdtemp()
for j, (ra, rb) in enumerate(av):
    P = [(g, o) for g, o in pairs if rng(o['s']) == j]
    if not P: print(f'range {j}: no matched words, skipped'); continue
    firsts[str(j)] = [P[0][0]['s'], P[0][1]['s']]
    nxt_g = next((g['s'] for g, o in pairs if rng(o['s']) > j), None)
    g_cap = GD if nxt_g is None else nxt_g - 0.05          # never overlap the next range's speech
    # source span: a breath before the first word .. end of the range (the CTA tail is never trimmed)
    o0 = max(0.0, ra - 0.05, P[0][1]['s'] - 0.15); o1 = min(VD, max(rb, P[-1][1]['e']) + 0.12)
    g0 = max(0.0, P[0][0]['s'] - A.lead - (P[0][1]['s'] - o0))
    # key frames: original time -> video time (word starts + the last word's end), lips lead = A.lead
    # Word starts AND ends are key frames: inside a word the speed change is limited (natural voice); a pause
    # (end -> next start) may stretch or shrink freely, because it is silence or breath. Generated videos often
    # pause much longer than the original voice; forcing that through the words is what made voices drift.
    K = []
    for g, o in P: K += [(o['s'], g['s'] - A.lead, 'S'), (o['e'], g['e'] - A.lead, 'E')]
    KK, kind = [(o0, g0)], ['E']
    for o, g, t in K:
        if not (o0 < o < o1 and g0 < g < g_cap): continue
        do, dg = o - KK[-1][0], g - KK[-1][1]
        if do < 0.03 or dg < 0.03: continue
        pause = kind[-1] == 'E' and t == 'S'
        lim = 6.0 if pause else A.max_rate
        if not (1 / lim <= do / dg <= lim): continue
        KK.append((o, g)); kind.append(t)
    rest = o1 - KK[-1][0]                                   # tail after the last key frame plays at natural speed
    g1 = min(g_cap, KK[-1][1] + rest)
    if rest / max(g1 - KK[-1][1], 1e-3) > A.max_rate:       # no room: speed the tail up, but never cut it
        g1 = min(g_cap, KK[-1][1] + rest / A.max_rate)
    src = pcm(A.voice, o0, o1)
    fi, fo, fm = f'{tmp}/in{j}.wav', f'{tmp}/out{j}.wav', f'{tmp}/map{j}.txt'
    wav_write(fi, src)
    with open(fm, 'w') as m:
        for o, g in KK[1:]: m.write(f'{int(round((o - o0) * SR))} {int(round((g - g0) * SR))}\n')
    subprocess.run(['rubberband', '-q', '-3', '--formant', '-D', f'{g1 - g0:.5f}', '--timemap', fm, fi, fo],
                   check=True, capture_output=True)
    y = pcm(fo).copy(); s0 = int(g0 * SR); n = min(len(y), len(out) - s0)
    f = min(int(0.008 * SR), n // 2); y[:f] *= np.linspace(0, 1, f); y[n - f:n] *= np.linspace(1, 0, f)
    out[s0:s0 + n] += y[:n]
    print(f'range {j}: {len(P)} words, {len(KK) - 1} key frames, voice {o0:.2f}-{o1:.2f}s -> video {g0:.2f}-{g1:.2f}s')
    if nxt_g is not None: cuts.append(round((P[-1][0]['e'] + nxt_g) / 2, 3))
cuts.append(round(GD, 3))
wav_write(A.out, out[:int(round(GD * SR))])
json.dump({'cuts': cuts, 'firsts': firsts}, open(A.out + '.cuts.json', 'w'))
shutil.rmtree(tmp, ignore_errors=True)
print('cuts', cuts); print('saved', A.out)
