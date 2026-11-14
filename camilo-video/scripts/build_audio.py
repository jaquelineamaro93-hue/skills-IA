"""Camilo Ep.1 — motor de áudio.

Lê src/timeline.json (fonte única) e gera:
  public/voices/<ID>.wav        recortes das falas (sem alteração de velocidade ou timbre;
                                apenas corte nos silêncios + fade de 10 ms contra cliques)
  public/music/trilha_original.wav   trilha 100% original, sintetizada aqui (violão
                                     Karplus-Strong, pad, baixo, percussão inspirada em cumbia)
  public/sfx/*.wav              efeitos sintetizados (ataduras, corda, passos, golpe, corrente, gongo...)
  public/mix/stem_*.wav         stems (vozes, música com ducking, sfx, ambiente)
  public/mix/master.wav         mix final normalizado (-14 LUFS, true peak -1.5 dBTP via FFmpeg)

Uso: python3 scripts/build_audio.py
"""
import json, subprocess
from pathlib import Path
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[1]
TL = json.loads((ROOT / "src/timeline.json").read_text())
SR = 48000
DUR = TL["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(7)
B = TL["beats"]
for d in ["voices", "music", "sfx", "mix"]:
    (ROOT / "public" / d).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- utilidades
def write_wav(path, x):
    x = np.asarray(x, dtype=np.float32)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    from scipy.io import wavfile
    wavfile.write(str(path), SR, x)


def load_audio(path, t_in=None, t_out=None):
    cmd = ["ffmpeg", "-v", "error"]
    if t_in is not None:
        cmd += ["-ss", f"{t_in:.3f}", "-to", f"{t_out:.3f}"]
    cmd += ["-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.2):
    t = np.arange(n) / SR
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, max(na, 1))[:na]
    e[na:na + nd] = np.linspace(1, s, max(nd, 1))[: len(e[na:na + nd])]
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, btype="high", fs=SR, output="sos"), x)


def noise(n):
    return rng.standard_normal(n)


def place(buf, x, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if x.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * l * 1.414, x * r * 1.414], 1)
    j = min(len(buf), i + len(x))
    if j > i:
        buf[i:j] += x[: j - i] * gain


def reverb(x, secs=1.4, mix=0.25, damp=3500):
    n = int(secs * SR)
    t = np.arange(n) / SR
    irL = noise(n) * np.exp(-t * 6.9 / secs)
    irR = noise(n) * np.exp(-t * 6.9 / secs)
    irL, irR = lp(irL, damp), lp(irR, damp)
    irL[: int(0.012 * SR)] = 0; irR[: int(0.017 * SR)] = 0
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    wl = signal.fftconvolve(x[:, 0], irL)[: len(x)]
    wr = signal.fftconvolve(x[:, 1], irR)[: len(x)]
    return x * (1 - mix) + np.stack([wl, wr], 1) * mix


def save(name, x):
    write_wav(ROOT / "public/sfx" / f"{name}.wav", x / (np.abs(x).max() + 1e-9) * 0.9)
    return x


# ---------------------------------------------------------------- 1. vozes
voice_bus = np.zeros((N, 2))
fade = int(0.010 * SR)
for vid, c in TL["voiceClips"].items():
    x = load_audio(ROOT / "assets-originais/audios" / c["file"], c["in"], c["out"])
    x[:fade] *= np.linspace(0, 1, fade)[:, None]
    x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    write_wav(ROOT / "public/voices" / f"{vid}.wav", x)
    c["_audio"] = x
# equilíbrio de nível entre narrador e Camilo (apenas ganho, RMS das partes faladas)
def rms_db(x):
    v = x.mean(1); v = v[np.abs(v) > 0.01]
    return 20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-9)
lv = {k: rms_db(c["_audio"]) for k, c in TL["voiceClips"].items()}
nar = np.mean([v for k, v in lv.items() if k.startswith("N")])
cam = np.mean([v for k, v in lv.items() if not k.startswith("N")])
for ev in TL["voiceEvents"]:
    c = TL["voiceClips"][ev["id"]]
    g_db = (nar - cam) if c["speaker"] == "camilo" else 0.0
    place(voice_bus, c["_audio"], ev["at"], 10 ** ((g_db - 1.0) / 20))
print(f"nível RMS narrador {nar:.1f} dB | Camilo {cam:.1f} dB -> Camilo ajustado {nar-cam:+.1f} dB")


# ---------------------------------------------------------------- 2. trilha original
BPM = TL["bpm"]; beat = 60 / BPM; bar = 4 * beat
def midi(m): return 440 * 2 ** ((m - 69) / 12)

def pluck(f, dur, bright=0.5, decay=0.996):
    n = int(dur * SR)
    P = max(2, int(SR / f))
    exc = lp(noise(P), 1500 + 5000 * bright)
    x = np.zeros(n); x[:P] = exc
    a = decay
    # Karplus-Strong como filtro IIR: y[n] = x[n] + a/2 (y[n-P] + y[n-P-1])
    den = np.zeros(P + 2); den[0] = 1; den[P] = -a / 2; den[P + 1] = -a / 2
    y = signal.lfilter([1], den, x)
    y = hp(y, 70) * env_adsr(n, 0.001, 0.05, 1.0, 0.08)
    return y / (np.abs(y).max() + 1e-9)

CH = {  # acordes (MIDI) — tonalidade de Ré maior
    "D": [50, 57, 62, 66, 69], "A": [45, 57, 61, 64, 69], "Bm": [47, 54, 59, 62, 66],
    "G": [43, 55, 59, 62, 67], "Em": [40, 52, 55, 59, 64], "A/C#": [49, 57, 61, 64, 69],
}
prog = ["D", "A/C#", "Bm", "G"] * 3 + ["Em", "A", "D", "G"] + ["G", "A", "Bm", "G", "A", "A", "D", "D"]
music = np.zeros((N, 2))
guitar = np.zeros(N); pad = np.zeros(N); bass = np.zeros(N); perc = np.zeros(N)
pattern = [0, 2, 3, 4, 1, 3, 2, 4]  # arpejo em colcheias

def sect_level(t):
    """Arco dinâmico da trilha (0-1) por trecho."""
    pts = [(0, .55), (14.5, .6), (15, .75), (22, .8), (29.7, .55), (37.3, .7), (40.0, 1.0),
           (43.5, .7), (50, .85), (54, .9), (60.5, .9)]
    xs, ys = zip(*pts); return float(np.interp(t, xs, ys))

t0 = 0.25
for bi, name in enumerate(prog):
    tb = t0 + bi * bar
    if tb > 56: break
    notes = CH[name]
    for k in range(8):
        tn = tb + k * beat / 2
        if B["musicCutStart"] - 0.05 < tn < B["musicResume"]: continue
        if tn > 56.5: break
        idx = pattern[k]
        y = pluck(midi(notes[idx] + 12 if idx > 2 else notes[idx]), 1.6, bright=0.35 + 0.1 * (k == 0))
        place_i = int(tn * SR); j = min(N, place_i + len(y))
        guitar[place_i:j] += y[: j - place_i] * (0.55 if k else 0.7) * sect_level(tn)
    # baixo (fundamental) a partir de S3
    if tb >= 14.9:
        for k, off in enumerate([0, 1.5 * beat, 2 * beat, 3.5 * beat]):
            tn = tb + off
            if B["musicCutStart"] - 0.05 < tn < B["musicResume"] or tn > 56: continue
            if 29.7 <= tn < 37.3 and k: continue  # S5: só a cabeça do compasso
            n = int(0.45 * SR); tt = np.arange(n) / SR
            y = np.sin(2 * np.pi * midi(notes[0] - 12) * tt) * np.exp(-tt * 5) + 0.3 * np.sin(4 * np.pi * midi(notes[0] - 12) * tt) * np.exp(-tt * 9)
            i = int(tn * SR); j = min(N, i + n); bass[i:j] += y[: j - i] * 0.5
    # pad sustentado a partir de S5
    if tb >= 29.5:
        n = int(bar * SR) + int(0.5 * SR); tt = np.arange(n) / SR
        y = np.zeros(n)
        for m in notes[1:4]:
            for det in (-0.08, 0.08):
                f = midi(m) * 2 ** (det / 12)
                y += signal.sawtooth(2 * np.pi * f * tt) * 0.2
        y = lp(y, 1400) * env_adsr(n, 0.6, 0.2, 0.8, 0.7)
        i = int(tb * SR); j = min(N, i + n)
        seg = y[: j - i] * 0.22 * sect_level(tb)
        pad[i:j] += seg
pad[int(B["musicCutStart"] * SR): int(B["musicResume"] * SR)] = 0

# percussão (shaker em colcheias, guacharaca, tambora suave) — S3, S4, pós-golpe e S7 leve
def shaker(n=int(0.07 * SR)):
    return bp(noise(n), 5000, 11000) * np.exp(-np.arange(n) / SR * 60)
def guacharaca(n=int(0.16 * SR)):
    tt = np.arange(n) / SR
    return bp(noise(n), 2500, 7000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 70 * tt))) * np.exp(-tt * 14)
def tambora(f=95, n=int(0.35 * SR)):
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * tt * (1 + 0.6 * np.exp(-tt * 30))) * np.exp(-tt * 11) + 0.15 * lp(noise(n), 900) * np.exp(-tt * 40)

perc_zones = [(15.0, 29.4, 1.0), (40.75, 43.5, 1.0), (45.5, 54.5, 0.55)]
t = 0.25
while t < 56:
    lvl = next((z[2] for z in perc_zones if z[0] <= t < z[1]), 0)
    if lvl:
        sub = round((t - 0.25) / (beat / 2)) % 8
        place_i = int(t * SR)
        s = shaker() * (0.25 if sub % 2 else 0.4)
        perc[place_i:place_i + len(s)] += s * lvl
        if sub in (2, 6):
            g = guacharaca(); perc[place_i:place_i + len(g)] += g * 0.35 * lvl
        if sub in (0, 3, 4):
            d = tambora(95 if sub != 3 else 120); perc[place_i:place_i + len(d)] += d * 0.55 * lvl
    t += beat / 2

# riser antes do golpe
n = int((B["musicCutStart"] - 37.6) * SR); tt = np.arange(n) / SR
riser = bp(noise(n), 400, 4000) * (tt / tt[-1]) ** 2.2 * 0.35
roll = np.zeros(n)
k = 0.0
while k < tt[-1]:
    d = tambora(110); i = int(k * SR); j = min(n, i + len(d)); roll[i:j] += d[: j - i] * 0.2 * (k / tt[-1]) ** 1.5
    k += max(0.06, 0.5 * (1 - k / tt[-1]))
place(music, riser + roll, 37.6, 1.0)

# acorde de chegada após o golpe e acorde final
for tc, name, g in [(B["musicResume"], "D", 0.9), (54.25, "D", 1.0)]:
    for m in CH[name]:
        y = pluck(midi(m), 4.5, 0.55, 0.9985)
        place(music, y, tc + rng.uniform(0, 0.03), 0.35 * g, pan=rng.uniform(-.3, .3))

gtr_st = np.stack([guitar * 0.9, np.concatenate([np.zeros(int(0.012 * SR)), guitar[: -int(0.012 * SR)]]) * 0.9], 1)
music += reverb(gtr_st, 1.6, 0.22)
music += reverb(pad, 2.2, 0.4)
music += np.stack([bass, bass], 1) * 0.8
music += reverb(perc, 0.9, 0.15) * 0.8
# fim em fade
fe0, fe1 = int(57.0 * SR), int(60.3 * SR)
music[fe0:fe1] *= np.linspace(1, 0, fe1 - fe0)[:, None]; music[fe1:] = 0
music /= np.abs(music).max() + 1e-9
write_wav(ROOT / "public/music/trilha_original.wav", music * 0.9)


# ---------------------------------------------------------------- 3. efeitos sonoros
def fabric(d=0.55):
    n = int(d * SR); tt = np.arange(n) / SR
    x = bp(noise(n), 900, 5000) * (np.sin(np.pi * tt / d) ** 1.5)
    x *= 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 23 * tt + rng.uniform(0, 6)))
    return x
def creak(d=0.7):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 95 + 25 * np.sin(2 * np.pi * 1.3 * tt) + 8 * noise(n).cumsum() / SR
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return bp(x, 250, 1400) * np.sin(np.pi * tt / d) ** 2
def bird(d=0.18, f0=None):
    n = int(d * SR); tt = np.arange(n) / SR
    f0 = f0 or rng.uniform(3200, 4800)
    f = f0 * (1 + 0.25 * np.sin(2 * np.pi * rng.uniform(15, 30) * tt)) * (1 + 0.2 * tt / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 2
def whoosh(d=0.22, lo=300, hi=2500):
    n = int(d * SR); tt = np.arange(n) / SR
    x = noise(n); out = np.zeros(n)
    for a, b in [(0, .33), (.33, .66), (.66, 1)]:
        i, j = int(a * n), int(b * n)
        c = lo + (hi - lo) * np.sin(np.pi * (a + b) / 2)
        out[i:j] = bp(x, c * 0.6, c * 1.6)[i:j]
    return out * np.sin(np.pi * tt / d) ** 2
def slap(d=0.05):
    n = int(d * SR); tt = np.arange(n) / SR
    return (bp(noise(n), 1500, 6000) * np.exp(-tt * 120) + 0.5 * np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 80))
def step(d=0.12):
    n = int(d * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 85 * tt) * np.exp(-tt * 40) + 0.3 * bp(noise(n), 800, 3000) * np.exp(-tt * 90)
def squeak(d=0.22):
    n = int(d * SR); tt = np.arange(n) / SR
    f = 1900 + 500 * tt / d + 80 * np.sin(2 * np.pi * 45 * tt)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * 0.5 + 0.3 * bp(noise(n), 2000, 6000) * np.sin(np.pi * tt / d)
def breath(d=0.9, inhale=True):
    n = int(d * SR); tt = np.arange(n) / SR
    e = (tt / d) ** 1.5 * np.exp(-(tt / d) * 2) if inhale else np.exp(-tt * 3) * (1 - np.exp(-tt * 40))
    return bp(noise(n), 500, 3000) * e
def impact(d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * (55 + 45 * np.exp(-tt * 18)) * tt) * np.exp(-tt * 7)
    thud = lp(noise(n), 1800) * np.exp(-tt * 35)
    slapc = bp(noise(n), 1200, 5000) * np.exp(-tt * 90)
    leather = np.sin(2 * np.pi * 160 * tt) * np.exp(-tt * 22)
    return body * 1.0 + thud * 0.8 + slapc * 0.5 + leather * 0.4
def chain(d=1.2):
    n = int(d * SR); x = np.zeros(n)
    t = 0.0
    while t < d * 0.85:
        m = int(0.05 * SR); tt = np.arange(m) / SR
        ping = sum(np.sin(2 * np.pi * f * tt) for f in rng.uniform(2200, 6500, 3)) * np.exp(-tt * rng.uniform(60, 110))
        i = int(t * SR); j = min(n, i + m); x[i:j] += ping[: j - i] * (1 - t / d) * rng.uniform(.4, 1)
        t += rng.uniform(0.02, 0.09) * (1 + 2 * t / d)
    return x
def gong(d=5.5):
    n = int(d * SR); tt = np.arange(n) / SR
    f0 = 98
    ratios = [1, 1.47, 2.03, 2.71, 3.33, 4.16, 5.4]
    x = sum(np.sin(2 * np.pi * f0 * r * tt * (1 + 0.004 * np.exp(-tt))) * np.exp(-tt * (0.6 + 0.35 * i)) / (1 + 0.5 * i)
            for i, r in enumerate(ratios))
    x *= 1 - np.exp(-tt * 60)
    x += 0.15 * bp(noise(n), 300, 3000) * np.exp(-tt * 25)
    return lp(x, 2500)
def gust(d=3.0):
    n = int(d * SR); tt = np.arange(n) / SR
    return lp(noise(n), 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.4 * tt + 1)) * np.sin(np.pi * tt / d)

sfx = np.zeros((N, 2)); amb = np.zeros((N, 2))
# Ambiente: bairro distante + sala (contínuo, sobe em S2, desce em S8)
room = lp(noise(N), 500) * 0.02 + lp(bp(noise(N), 150, 900), 900) * 0.015
amb_env = np.interp(np.arange(N) / SR, [0, 1.2, 7.4, 8.4, 14.5, 15.5, 54.5, 57, 60.5], [0, .7, .7, 1.1, 1.1, .6, .6, .2, 0])
amb += np.stack([room * amb_env, np.roll(room, 997) * amb_env], 1)
for tc in [1.6, 3.3, 9.5, 11.0, 13.8]:  # buzinas/motos distantes muito baixas
    n = int(1.2 * SR); tt = np.arange(n) / SR
    moto = bp(signal.sawtooth(2 * np.pi * (70 + 20 * np.sin(2 * np.pi * .5 * tt)) * tt), 120, 900) * np.sin(np.pi * tt / 1.2) ** 2
    place(amb, lp(moto, 600) * 0.05, tc, 1, pan=rng.uniform(-.7, .7))
for tc in np.arange(7.8, 15.0, 0.9) + rng.uniform(-.2, .2, len(np.arange(7.8, 15.0, 0.9))):  # passarinhos em S2
    for k in range(rng.integers(1, 4)):
        place(amb, bird(), tc + k * 0.14, 0.06, pan=rng.uniform(-.8, .8))
place(amb, gust(4.0), 8.0, 0.08, pan=-.4); place(amb, gust(3.0), 11.5, 0.06, pan=.4)
for tc in [44.5, 47.8, 51.5]:
    place(amb, bird(0.16, 4200), tc, 0.035, pan=.6)

# S1: ataduras, madeira, respiração
for tc in [0.9, 2.2, 3.4, 4.6, 6.0]:
    place(sfx, save("ataduras", fabric(rng.uniform(.4, .7))), tc, 0.22, pan=.15)
place(sfx, save("madeira_rangendo", creak()), 2.9, 0.06, pan=-.5)
place(sfx, save("respiracao", breath(1.0)), 4.2, 0.10)
# S2: passos leves
for k, tc in enumerate([9.2, 9.75, 10.3]):
    place(sfx, save("passo_madeira", step()), tc, 0.12, pan=-.2 + .1 * k)
# S3: corda (whoosh + batida no chão a cada tempo), tropeço, tênis deslizando, suspiro
t = B["ropeStart"]
while t <= B["ropeEnd"] + 1e-6:
    place(sfx, save("corda_whoosh", whoosh(0.2, 600, 3500)), t - 0.16, 0.14, pan=rng.uniform(-.3, .3))
    place(sfx, save("corda_batida", slap()), t, 0.30)
    place(sfx, step(0.08), t + 0.04, 0.1)
    t += beat
st = B["stumble"]
place(sfx, whoosh(0.18, 600, 3500), st - 0.15, 0.14)
place(sfx, slap(), st - 0.02, 0.22)
place(sfx, save("tenis_deslizando", squeak()), st + 0.02, 0.16, pan=.2)
place(sfx, step(0.15), st + 0.18, 0.3); place(sfx, step(0.12), st + 0.33, 0.22)
place(sfx, breath(0.7, inhale=False), st + 0.4, 0.12)
# S4: passos, esquivas, socos no ar
for tc in B["weaves"]:
    place(sfx, whoosh(0.25, 250, 1200), tc - 0.1, 0.12); place(sfx, step(), tc + 0.12, 0.14)
for tc in B["airPunches"]:
    place(sfx, save("soco_no_ar", whoosh(0.16, 900, 4500)), tc - 0.12, 0.18, pan=rng.uniform(-.2, .2))
# S5: respiração cansada
for tc in [30.0, 31.6, 33.0, 34.6, 36.0]:
    place(sfx, breath(0.85), tc, 0.09); place(sfx, breath(0.6, False), tc + 0.85, 0.06)
# S6: inspiração profunda, preparação, impacto, corrente
place(sfx, breath(1.3), 38.2, 0.14)
place(sfx, whoosh(0.35, 200, 900), B["punchWindup"], 0.10)
place(sfx, whoosh(0.18, 900, 5000), B["punchImpact"] - 0.14, 0.24)
place(sfx, save("impacto_couro", impact()), B["punchImpact"], 0.85)
place(sfx, save("corrente", chain()), B["punchImpact"] + 0.03, 0.18, pan=-.35)
place(sfx, chain(0.9), B["punchImpact"] + 0.9, 0.08, pan=-.35)
# S8: gongo distante
g = save("gongo_distante", gong())
place(sfx, reverb(g, 3.5, 0.55, 2000), B["gong"], 0.32)

sfx = reverb(sfx, 0.8, 0.14, 4000)

# ---------------------------------------------------------------- 4. mixagem com ducking
v_env = np.abs(voice_bus.mean(1))
v_env = lp(v_env, 6, 1)
win = int(0.25 * SR)
hold = np.convolve((v_env > 0.004).astype(float), np.ones(win) / win, mode="same")
duck = 1 - 0.6 * np.clip(hold * 1.6, 0, 1)          # até ~ -8 dB sob a voz
duck = lp(duck, 4, 1)
music_bus = music * duck[:, None] * 0.30
write_wav(ROOT / "public/mix/stem_vozes.wav", voice_bus)
write_wav(ROOT / "public/mix/stem_musica_duck.wav", music_bus)
write_wav(ROOT / "public/mix/stem_sfx.wav", sfx)
write_wav(ROOT / "public/mix/stem_ambiente.wav", amb)
mix = voice_bus + music_bus + sfx + amb
pre = ROOT / "public/mix/_premaster.wav"
write_wav(pre, mix / (np.abs(mix).max() + 1e-9) * 0.7)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(pre), "-af",
                "highpass=f=30,loudnorm=I=-14:TP=-1.5:LRA=11:linear=true", "-ar", str(SR),
                "-c:a", "pcm_s16le", str(ROOT / "public/mix/master.wav")], check=True)
pre.unlink()
print("ok: public/mix/master.wav")
