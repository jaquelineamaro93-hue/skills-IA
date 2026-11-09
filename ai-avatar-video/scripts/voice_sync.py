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
ap.add_argument('--rate', default='0.78,1.28', help='min,max speed')
ap.add_argument('--jump', type=float, default=0.20, help='max speed change from one word to the next (gradual = natural)')
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

REF = float(np.percentile(np.sqrt((np.pad(pcm(A.voice)[::3], (0, -len(pcm(A.voice)[::3]) % 160)).reshape(-1, 160) ** 2).mean(1)), 90))
SPG = (DB_G > -20).astype(float)
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
    # Cut ONLY in real silence of the original (>= 80 ms below -30 dB) between the last word of one phrase and the
    # first word of the next. No real silence -> the two phrases stay one. (Whisper word ends are often early:
    # cutting "between words" by its timestamps split "cliente" and "contratação" in two -> audible stutter.)
    def silent_cut(t0, t1, thr=-30, need=8):
        i0, i1 = int(max(0, t0) * 100), int(t1 * 100); best, run, start = None, 0, 0
        for i in range(i0, max(i0, i1)):
            if DB_O[i] < thr:
                if run == 0: start = i
                run += 1
                if run >= need and (best is None or run > best[1]): best = (start, run)
            else: run = 0
        return None if best is None else (best[0] + best[1] / 2) / 100
    merged, C = [phrases[0]], [o0]
    for ph in phrases[1:]:
        lg, lw = merged[-1][-1]; w0, w1 = max(lw['s'] + 0.1, lw['e'] - 0.05), ph[0][1]['s'] + 0.12
        c = silent_cut(w0, w1)                                     # real silence: 80 ms below -30 dB
        if c is None and ph[0][0]['s'] - lg['e'] - (ph[0][1]['s'] - lw['e']) >= 0.25:
            c = silent_cut(w0, w1, -24, 4)                         # mouth pauses, voice only breathes: cut in the breath
        if c is None: merged[-1] = merged[-1] + ph
        else: merged.append(ph); C.append(c)
    C.append(o1); phrases = merged
    # place every phrase: steady speed r in [lo, hi], starting with the mouth; then resolve overlaps in order
    L, prev = [], None  # [o_start, o_end, g_start, duration]  (o_* = where the sound starts/ends inside its cut)
    for k, ph in enumerate(phrases):
        os_ = max(C[k], snap_on(DB_O, ph[0][1]['s'])); oe = min(C[k + 1], max(os_ + 0.1, snap_off(DB_O, ph[-1][1]['e'], fwd=0.6)))
        gs, ge = snap_on(DB_G, ph[0][0]['s']), snap_off(DB_G, ph[-1][0]['e'], fwd=0.6)
        if ge - gs < 0.1: gs, ge = ph[0][0]['s'], ph[-1][0]['e']
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
            k_ = room / tot
            for p in L: p[2] = L[0][2] + (p[2] - L[0][2]) * k_; p[3] *= k_
    rates = [round((p[1] - p[0]) / p[3], 2) for p in L]
    # Render each phrase as its own piece (cut in silence, faded 10 ms). Inside the phrase the speed FOLLOWS the
    # mouth word by word, but smoothly: at most --jump change from one word to the next, inside --rate.
    # Then SELF-CORRECT: measure each piece against the mouth (first and second half), move its start/end targets
    # by the measured lag and render again, up to 4 rounds; keep the best round.
    def env_db(y):
        y = y[::3]; e = np.sqrt((np.pad(y, (0, -len(y) % 160)).reshape(-1, 160) ** 2).mean(1))
        return 20 * np.log10(e / REF + 1e-9)
    def lag_at(sp_out, t0, t1):   # voice-vs-mouth lag (s) in [t0, t1]; + = voice late
        i0, i1 = max(0, int(t0 * 100)), min(len(sp_out), len(SPG), int(t1 * 100))
        a_, b_ = SPG[i0:i1], sp_out[i0:i1]
        if i1 - i0 < 30 or a_.sum() < 15 or b_.sum() < 15: return 0.0
        c = [np.sum(a_ * np.roll(b_, -l)) for l in range(-40, 41)]
        return (int(np.argmax(c)) - 40) / 100
    def render(SH):
        buf = np.zeros(len(out), np.float32); spans, sr_, jm = [], [], []
        for i, p in enumerate(L):
            c0, c1 = C[i], C[i + 1]
            if c1 - c0 < 0.05: spans.append(None); continue
            ss, se = SH[i]
            st, en = p[2] - ss, p[2] + p[3] - se
            if i and spans[-1]: st = max(st, spans[-1][2] + 0.02)
            en = max(en, st + (p[1] - p[0]) / hi)
            W_ = [(o['s'], g['s'] - A.lead) for g, o in phrases[i] if p[0] + 0.05 < o['s'] < p[1] - 0.05]
            W_ = [(ok, tk - ss - (se - ss) * (ok - p[0]) / max(p[1] - p[0], 0.1)) for ok, tk in W_]
            r = (p[1] - p[0]) / max(en - st, 0.05); r = max(lo, min(hi, r)); t = st; o = p[0]; km = []
            for ok, tk in W_ + [(p[1], en)]:
                want = (ok - o) / max(tk - t, 0.05)
                r_new = max(lo, min(hi, max(r - A.jump, min(r + A.jump, want))))
                if sr_: jm.append(abs(r_new - r))
                r = r_new; t += (ok - o) / r; o = ok; km.append((o, t)); sr_.append(round(r, 2))
            r0 = (km[0][0] - p[0]) / max(km[0][1] - st, 1e-3) if km and km[0][1] > st else 1.0
            t0 = st - (p[0] - c0) / max(lo, min(hi, r0))
            tail = (c1 - p[1]) / r
            if i == len(L) - 1 and t + tail > g_cap: tail = max(0.05, g_cap - t)
            t1 = t + tail
            fi, fo, fm = f'{tmp}/in{j}_{i}.wav', f'{tmp}/out{j}_{i}.wav', f'{tmp}/map{j}_{i}.txt'
            if not os.path.exists(fi): wav_write(fi, pcm(A.voice, c0, c1))
            with open(fm, 'w') as m:
                m.write(f'{int(round((p[0] - c0) * SR))} {int(round((st - t0) * SR))}\n')
                for ok, tk in km[:-1] + ([km[-1]] if c1 - p[1] > 0.02 else []):
                    m.write(f'{int(round((ok - c0) * SR))} {int(round((tk - t0) * SR))}\n')
            subprocess.run(['rubberband', '-q', '-3', '--formant', '-D', f'{t1 - t0:.5f}', '--timemap', fm, fi, fo],
                           check=True, capture_output=True)
            y = pcm(fo).copy(); s0 = max(0, int(round(t0 * SR))); n = min(len(y), len(buf) - s0)
            if n <= 0: spans.append(None); continue
            f = min(int(0.01 * SR), n // 2); y[:f] *= np.linspace(0, 1, f); y[n - f:n] *= np.linspace(1, 0, f)
            buf[s0:s0 + n] += y[:n]; spans.append((st, t, t1))
        return buf, spans, sr_, jm
    SH = [[0.0, 0.0] for _ in L]; best = None
    for rnd in range(4):
        buf, spans, sr_, jm = render(SH)
        sp = (env_db(buf) > -20).astype(float)
        errs = []
        for i, spn in enumerate(spans):
            if not spn: errs.append((0, 0)); continue
            st, te, _ = spn; mid = (st + te) / 2
            errs.append((lag_at(sp, st - 0.3, mid + 0.2), lag_at(sp, mid - 0.2, te + 0.3)))
        worst = max((max(abs(a_), abs(b_)) for a_, b_ in errs), default=0)
        if best is None or worst < best[0]: best = (worst, buf, sr_, jm, rnd)
        if worst <= 0.1: break
        for i, (ea, eb) in enumerate(errs):
            if abs(ea) > 0.06: SH[i][0] += 0.8 * ea
            if abs(eb) > 0.06: SH[i][1] += 0.8 * eb
    worst, buf, seg_rates, jumps, rnd = best
    out += buf; g1 = max((sp_[2] for sp_ in spans if sp_), default=g0)
    rates = seg_rates
    ov = [f'{a_[1]:.2f}s' for a_, b_ in zip([x for x in spans if x], [x for x in spans if x][1:]) if b_[0] < a_[1] - 0.01]
    print(f'range {j}: self-correction {rnd + 1} round(s), worst phrase lag {worst * 1000:.0f} ms, '
          f'overlapping phrases: {", ".join(ov) or "none"}')
    print(f'range {j}: {len(P)} words, {len(phrases)} phrases, voice {o0:.2f}-{o1:.2f}s -> video {g0:.2f}-{g1:.2f}s, '
          f'speeds {min(rates, default=1)}x-{max(rates, default=1)}x, '
          f'biggest change between words {max(jumps, default=0):.2f}x')
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
