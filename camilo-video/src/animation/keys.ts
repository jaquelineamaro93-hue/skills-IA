import {Easing, interpolate} from 'remotion';

export const FPS = 30;
export const W = 1080;
export const H = 1920;

export type Key = [number, number];
const smooth = Easing.bezier(0.45, 0, 0.25, 1);

/** Interpola uma sequência de chaves [tempo, valor] com easing cinematográfico suave. */
export const kf = (t: number, keys: Key[], ease: (n: number) => number = smooth): number => {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, v0] = keys[i];
    const [t1, v1] = keys[i + 1];
    if (t <= t1) return v0 + (v1 - v0) * ease((t - t0) / (t1 - t0));
  }
  return keys[keys.length - 1][1];
};

export const ramp = (t: number, a: number, b: number, ease = smooth) =>
  interpolate(t, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

/** Pulso 0→1→0 entre a e a+d (seno). */
export const pulse = (t: number, a: number, d: number) =>
  t < a || t > a + d ? 0 : Math.sin((Math.PI * (t - a)) / d);

/** Oscilação amortecida após um impacto em t0. */
export const damped = (t: number, t0: number, freq = 3, decay = 4) =>
  t < t0 ? 0 : Math.sin(2 * Math.PI * freq * (t - t0)) * Math.exp(-decay * (t - t0));

/** Câmera na mão: ruído suave e determinístico (soma de senos). */
export const handheld = (t: number, amp = 1) => ({
  x: amp * (3.2 * Math.sin(t * 0.9 + 1.3) + 1.6 * Math.sin(t * 2.1 + 0.4)),
  y: amp * (2.6 * Math.sin(t * 0.7 + 2.1) + 1.2 * Math.sin(t * 1.9 + 3.3)),
  r: amp * (0.12 * Math.sin(t * 0.55 + 0.7) + 0.05 * Math.sin(t * 1.7)),
});

/** Tremor de impacto (decai exponencialmente). */
export const shake = (t: number, t0: number, amp = 16, decay = 7) => {
  if (t < t0) return {x: 0, y: 0, r: 0};
  const e = Math.exp(-decay * (t - t0)) * amp;
  return {
    x: e * Math.sin((t - t0) * 83),
    y: e * Math.sin((t - t0) * 67 + 1.1),
    r: (e / amp) * 0.6 * Math.sin((t - t0) * 51),
  };
};

/** Gerador pseudoaleatório determinístico. */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};
