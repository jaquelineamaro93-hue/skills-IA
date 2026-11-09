#!/usr/bin/env python3
"""Replace the AI-generated voice of an avatar clip with the ORIGINAL voice file, aligned word by word to the lips.

usage: voice_sync.py generated.mp4 original_voice.mp3 out_fit.wav [--ranges "11.0-36.9,40.2-52.0"] [--lang pt]

--ranges  the parts of the ORIGINAL voice file (seconds) that this clip speaks, in order. Omit if the clip speaks
          the whole file. Each range becomes range j for assemble.py (video span cuts[j]..cuts[j+1]).
Output:   out_fit.wav (48 kHz mono, exactly as long as the video) and out_fit.wav.cuts.json
          {"cuts": [0, ..., video_len], "firsts": {"j": [video_t, voice_t]}} (first matched word of each range).

Method (why): both audios are transcribed with word timestamps (words.py) and matched in order (difflib).
The original is split into phrases at its real pauses; each phrase keeps one steady speed (0.85x-1.15x) and is
centred on the mouth's phrase, and the pauses absorb the rest. It is ONE continuous Rubber Band time map per range
(no pieces = no clicks; no global DTW = no drift). Word-by-word speed changes were tried and rejected: the voice
went slow and then sped up, which sounds fake. Hallucinated words in the generated speech are simply skipped.
Requires the `rubberband` CLI (apt install rubberband-cli / brew install rubberband).
"""
import sys, os, json, re, argparse, difflib, subprocess, unicodedata, shutil, tempfile, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('gen'); ap.add_argument('voice'); ap.add_argument('out')
ap.add_argument('--ranges', default=''); ap.add_argument('--lang', default='pt')
ap.add_argument('--lead', type=float, default=0.04, help='voice leads the lips by this much (s); 0.02-0.08 looks natural')
ap.add_argument('--rate', default='0.85,1.15', help='min,max steady speed of each phrase (natural: 0.85-1.15)')
ap.add_argument('--jump', type=float, default=0.10, help='max speed change from one phrase to the next')
ap.add_argument('--pause', type=float, default=0.03, help='silence (s) in the original that separates two phrases (tuned: 0.03)')
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

# real pauses of the original voice, from its loudness (Whisper word edges often touch each other)
_y = pcm(A.voice)[::3]  # 16 kHz is plenty for loudness
_e = np.sqrt((np.pad(_y, (0, -len(_y) % 160)).reshape(-1, 160) ** 2).mean(1))   # 10 ms frames
_q = _e < np.percentile(_e, 90) * 10 ** (-24 / 20)   # quiet = 24 dB below speech
def paused(t0, t1):  # is there >= A.pause of silence between the end of one word and the start of the next?
    a, b = int(max(0, t0 - 0.1) * 100), int((t1 + 0.05) * 100); need = max(1, int(A.pause * 100)); run = 0
    for v in _q[a:b]:
        run = run + 1 if v else 0
        if run >= need: return True
    return False

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
    # PHRASES (runs of speech between real pauses of the original voice) keep ONE steady speed each, limited to
    # --rate (default 0.85x-1.15x): a voice that slows down and speeds up word by word sounds fake, even when it
    # matches the lips better. Each phrase is centred on the mouth's phrase; the pauses absorb the difference
    # (they are silence/breath, so they can stretch or shrink freely). Key frames only at phrase edges.
    lo, hi = map(float, A.rate.split(','))
    phrases, cur = [], [P[0]]
    for (_, wa), pb in zip(P[:-1], P[1:]):
        if paused(wa['e'], pb[1]['s']): phrases.append(cur); cur = []
        cur.append(pb)
    phrases.append(cur)
    # place every phrase: steady speed r in [lo, hi], centred on the mouth; then resolve overlaps in order
    L, prev = [], None  # [o_start, o_end, g_start, duration]
    for ph in phrases:
        os_, oe = ph[0][1]['s'], ph[-1][1]['e']; gs, ge = ph[0][0]['s'], ph[-1][0]['e']
        r = max(lo, min(hi, (oe - os_) / max(ge - gs, 0.05)))
        if prev is not None: r = max(prev - A.jump, min(prev + A.jump, r))   # no sudden speed change between phrases
        prev = r; d = (oe - os_) / r
        L.append([os_, oe, (gs + ge) / 2 - d / 2 - A.lead, d])
    L[0][2] = max(L[0][2], g0 + (L[0][0] - o0) / 1.5)            # room for the breath before the first word
    for i in range(1, len(L)):                                     # a pause may shrink, never below 1/3 of it
        L[i][2] = max(L[i][2], L[i - 1][2] + L[i - 1][3] + (L[i][0] - L[i - 1][1]) / 3)
    over = L[-1][2] + L[-1][3] - (g_cap - 0.05)
    if over > 0:                                                   # ran past the end: pull back, then speed up
        for p in L: p[2] -= over
        L[0][2] = max(L[0][2], g0)
        for i in range(1, len(L)): L[i][2] = max(L[i][2], L[i - 1][2] + L[i - 1][3] + 0.03)
        tot = L[-1][2] + L[-1][3] - L[0][2]; room = g_cap - 0.05 - L[0][2]
        if tot > room:
            k = room / tot
            for p in L: p[2] = L[0][2] + (p[2] - L[0][2]) * k; p[3] *= k
    KK = [(o0, g0)] + [kf for p in L for kf in ((p[0], p[2]), (p[1], p[2] + p[3]))]
    rates = [round((p[1] - p[0]) / p[3], 2) for p in L]
    KK = [kf for i, kf in enumerate(KK) if i == 0 or (kf[0] > KK[i - 1][0] + 0.005 and kf[1] > KK[i - 1][1] + 0.005)]
    rest = o1 - KK[-1][0]                                   # tail after the last key frame plays at natural speed
    g1 = min(g_cap, KK[-1][1] + rest)
    if rest / max(g1 - KK[-1][1], 1e-3) > 1.3:              # no room: speed the tail up a little, never cut it
        g1 = min(g_cap, KK[-1][1] + rest / 1.3)
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
    print(f'range {j}: {len(P)} words, {len(phrases)} phrases, voice {o0:.2f}-{o1:.2f}s -> video {g0:.2f}-{g1:.2f}s, '
          f'phrase speeds {min(rates, default=1)}x-{max(rates, default=1)}x, '
          f'biggest jump {max((abs(a - b) for a, b in zip(rates, rates[1:])), default=0):.2f}x')
    if nxt_g is not None: cuts.append(round((P[-1][0]['e'] + nxt_g) / 2, 3))
cuts.append(round(GD, 3))
wav_write(A.out, out[:int(round(GD * SR))])
json.dump({'cuts': cuts, 'firsts': firsts}, open(A.out + '.cuts.json', 'w'))
shutil.rmtree(tmp, ignore_errors=True)
print('cuts', cuts); print('saved', A.out)
