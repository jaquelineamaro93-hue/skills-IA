#!/usr/bin/env python3
"""Replace the AI-generated voice of an avatar clip with the ORIGINAL voice file, aligned word by word to the lips.

usage: voice_sync.py generated.mp4 original_voice.mp3 out_fit.wav [--ranges "11.0-36.9,40.2-52.0"] [--lang pt]

--ranges  the parts of the ORIGINAL voice file (seconds) that this clip speaks, in order. Omit if the clip speaks
          the whole file. Each range becomes range j for assemble.py (video span cuts[j]..cuts[j+1]).
Output:   out_fit.wav (48 kHz mono, exactly as long as the video) and out_fit.wav.cuts.json
          {"cuts": [0, ..., video_len], "firsts": {"j": [video_t, voice_t]}} (first matched word of each range).

Method (why): both audios are transcribed with word timestamps (words.py) and matched in order (difflib).
The original is split into phrases at its real pauses AND where the mouth pauses longer than the voice. Each phrase
keeps ONE steady speed (0.85x-1.15x, max 0.10x change between neighbours), is cut at the quietest point around it,
and placed so its first word lands on the mouth (start found from the sound, not Whisper's often-wrong word edges).
Pauses are real silence. Rejected on purpose: word-by-word speed (sounds slow-then-fast), global DTW (drifts),
one time map with stretched pauses (smears a word into the silence before the mouth opens).
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
def _db(path):  # loudness in dB relative to the speech level, 10 ms frames
    y = pcm(path)[::3]; e = np.sqrt((np.pad(y, (0, -len(y) % 160)).reshape(-1, 160) ** 2).mean(1))
    return 20 * np.log10(e / (np.percentile(e, 90) + 1e-9) + 1e-9)
DB_O, DB_G = _db(A.voice), _db(A.gen)
def snap_on(db, t, back=0.35, fwd=0.6):
    # Whisper often puts the first word after a silence too early/late; use where the sound really starts
    a, b = max(0, int((t - back) * 100)), min(len(db) - 1, int((t + fwd) * 100))
    for i in range(a, b):
        if db[i] > -18 and (db[max(0, i - 6):i] < -26).all(): return i / 100
    return t
def snap_off(db, t, back=0.4, fwd=0.4):
    a, b = max(0, int((t - back) * 100)), min(len(db) - 7, int((t + fwd) * 100))
    for i in range(b, a, -1):
        if db[i] > -18 and (db[i + 1:i + 7] < -26).all(): return (i + 1) / 100
    return t

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
    # PHRASES (runs of speech between pauses) keep ONE steady speed each, limited to --rate (0.85x-1.15x): a voice
    # that slows down and speeds up word by word sounds fake, even when it matches the lips better.
    lo, hi = map(float, A.rate.split(','))
    phrases, cur = [], [P[0]]
    for (ga, wa), pb in zip(P[:-1], P[1:]):
        # a new phrase where the ORIGINAL voice pauses, or where the MOUTH pauses clearly longer than the voice
        # does (the generated video often holds a 1-2 s pause where the original only breathes: without this
        # split, the words before the pause come late and the words after it come early)
        mouth_gap, voice_gap = pb[0]['s'] - ga['e'], pb[1]['s'] - wa['e']
        if paused(wa['e'], pb[1]['s']) or (mouth_gap >= 0.25 and mouth_gap - voice_gap >= 0.2):
            phrases.append(cur); cur = []
        cur.append(pb)
    phrases.append(cur)
    # place every phrase: steady speed r in [lo, hi], starting with the mouth; then resolve overlaps in order
    L, prev = [], None  # [o_start, o_end, g_start, duration]
    for ph in phrases:
        os_, oe = snap_on(DB_O, ph[0][1]['s']), snap_off(DB_O, ph[-1][1]['e'])
        gs, ge = snap_on(DB_G, ph[0][0]['s']), snap_off(DB_G, ph[-1][0]['e'])
        if oe - os_ < 0.1 or ge - gs < 0.1: os_, oe, gs, ge = ph[0][1]['s'], ph[-1][1]['e'], ph[0][0]['s'], ph[-1][0]['e']
        r = max(lo, min(hi, (oe - os_) / max(ge - gs, 0.05)))
        if prev is not None: r = max(prev - A.jump, min(prev + A.jump, r))   # no sudden speed change between phrases
        prev = r; d = (oe - os_) / r
        # start of the phrase ~ the mouth opening (voice a hair early looks natural; voice before the mouth opens,
        # or long after, is what viewers notice). Within that window, centre the phrase on the mouth.
        a = min(gs - A.lead + 0.05, max(gs - A.lead - 0.08, (gs + ge) / 2 - d / 2 - A.lead))
        L.append([os_, oe, a, d])
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
    rates = [round((p[1] - p[0]) / p[3], 2) for p in L]
    # Render phrase by phrase: each piece of the original runs from the quietest point before the phrase to the
    # quietest point after it, at the phrase's ONE speed, placed so its first word lands on the mouth. Pauses
    # between pieces are real silence. (A single time map stretched the pauses too, and a word whose start
    # Whisper marked late got smeared 10x into the silence before the mouth opened.)
    def quietest(t0, t1):
        i0, i1 = int(max(0, t0) * 100), max(int(max(0, t0) * 100) + 1, int(t1 * 100))
        return (i0 + int(np.argmin(DB_O[i0:i1]))) / 100
    C = [o0] + [quietest(L[i - 1][1] - 0.05, L[i][0] + 0.05) for i in range(1, len(L))] + [o1]
    g1 = 0.0
    for i, p in enumerate(L):
        c0, c1 = C[i], C[i + 1]
        if c1 - c0 < 0.02: continue
        r = (p[1] - p[0]) / p[3]
        t0 = p[2] - (p[0] - c0) / r
        dur = (c1 - c0) / r
        if i == len(L) - 1 and t0 + dur > g_cap:                     # the CTA tail must fit: speed it up a bit
            r = min(1.3, (c1 - c0) / max(g_cap - t0, 0.05)); dur = (c1 - c0) / r
        fi, fo = f'{tmp}/in{j}_{i}.wav', f'{tmp}/out{j}_{i}.wav'
        wav_write(fi, pcm(A.voice, c0, c1))
        if abs(r - 1) > 0.005:
            subprocess.run(['rubberband', '-q', '-3', '--formant', '-D', f'{dur:.5f}', fi, fo], check=True, capture_output=True)
        else: fo = fi
        y = pcm(fo).copy(); s0 = max(0, int(round(t0 * SR))); n = min(len(y), len(out) - s0)
        if n <= 0: continue
        f = min(int(0.01 * SR), n // 2); y[:f] *= np.linspace(0, 1, f); y[n - f:n] *= np.linspace(1, 0, f)
        out[s0:s0 + n] += y[:n]; g1 = max(g1, (s0 + n) / SR)
    print(f'range {j}: {len(P)} words, {len(phrases)} phrases, voice {o0:.2f}-{o1:.2f}s -> video {g0:.2f}-{g1:.2f}s, '
          f'phrase speeds {min(rates, default=1)}x-{max(rates, default=1)}x, '
          f'biggest jump {max((abs(a - b) for a, b in zip(rates, rates[1:])), default=0):.2f}x')
    if nxt_g is not None: cuts.append(round((P[-1][0]['e'] + nxt_g) / 2, 3))
cuts.append(round(GD, 3))
wav_write(A.out, out[:int(round(GD * SR))])
# SYNC REPORT: the generated audio follows the mouth, so compare when each one is speaking, 3 s at a time
F = _db(A.out); n = min(len(F), len(DB_G)); sg, sf = (DB_G[:n] > -20).astype(float), (F[:n] > -20).astype(float)
bad = []
for t in range(0, max(1, n // 100 - 2), 2):
    a_, b_ = sg[t * 100:(t + 3) * 100], sf[t * 100:(t + 3) * 100]
    if a_.sum() < 30: continue
    c = [np.sum(a_ * np.roll(b_, -l)) for l in range(-50, 51)]; lag = (int(np.argmax(c)) - 50) * 10
    if abs(lag) > 200: bad.append(f'{t}-{t + 3}s {lag:+d} ms')
print('sync check (voice vs mouth, 3 s windows):', 'OK, all within 0.2 s' if not bad else 'LOOK AT ' + ', '.join(bad))
json.dump({'cuts': cuts, 'firsts': firsts}, open(A.out + '.cuts.json', 'w'))
shutil.rmtree(tmp, ignore_errors=True)
print('cuts', cuts); print('saved', A.out)
