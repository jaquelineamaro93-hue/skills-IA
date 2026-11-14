import React from 'react';
import {AbsoluteFill} from 'remotion';
import {rand} from '../animation/keys';

/** Impacto do soco: onda de choque + explosão de poeira (coordenadas do mundo). */
export const ImpactBurst: React.FC<{t: number; t0: number; x: number; y: number}> = ({t, t0, x, y}) => {
  const dt = t - t0;
  if (dt < 0 || dt > 1.2) return null;
  const ring = Math.min(1, dt / 0.28);
  return (
    <>
      <div style={{
        position: 'absolute', left: x - 260 * ring, top: y - 260 * ring, width: 520 * ring, height: 520 * ring,
        borderRadius: '50%', border: `${10 * (1 - ring) + 1}px solid rgba(255,235,200,${0.75 * (1 - ring)})`,
        filter: 'blur(2px)', mixBlendMode: 'screen',
      }} />
      <div style={{
        position: 'absolute', left: x - 160, top: y - 160, width: 320, height: 320, borderRadius: '50%',
        background: `radial-gradient(circle, rgba(255,245,220,${0.9 * Math.exp(-dt * 14)}) 0%, rgba(255,200,140,0) 65%)`,
        mixBlendMode: 'screen',
      }} />
      {new Array(38).fill(0).map((_, i) => {
        const a = (rand(i + 3) - 0.5) * 2.6 + Math.PI * (rand(i) > 0.75 ? 1 : 0); // maioria espirra para a direita
        const v = 260 + rand(i + 9) * 520;
        const px = x + Math.cos(a) * v * (1 - Math.exp(-dt * 4)) / 1.2;
        const py = y + Math.sin(a) * v * (1 - Math.exp(-dt * 4)) / 1.2 + 160 * dt * dt;
        const s = 3 + rand(i + 20) * 9;
        return (
          <div key={i} style={{
            position: 'absolute', left: px, top: py, width: s, height: s, borderRadius: '50%',
            background: 'rgba(240,215,170,0.9)', opacity: Math.max(0, 1 - dt / (0.6 + rand(i) * 0.6)),
            filter: s > 8 ? 'blur(2px)' : 'blur(0.5px)', mixBlendMode: 'screen',
          }} />
        );
      })}
    </>
  );
};

/** Clarão de tela inteira (poucos quadros). */
export const Flash: React.FC<{t: number; t0: number; strength?: number}> = ({t, t0, strength = 0.45}) => {
  const dt = t - t0;
  if (dt < 0 || dt > 0.3) return null;
  return <AbsoluteFill style={{background: `rgba(255,244,225,${strength * Math.exp(-dt * 18)})`, mixBlendMode: 'screen'}} />;
};

/** Corda de pular em movimento (rastro com desfoque de movimento), coordenadas do mundo.
 *  phase 0 = corda no chão sob os pés; a corda desce pela frente entre phase 0.72 e 1. */
export const RopeStreak: React.FC<{phase: number; left: [number, number]; right: [number, number]; floorY: number; spread: number}> = ({
  phase, left, right, floorY, spread,
}) => {
  const vis = (p: number) => (p > 0.7 ? (p - 0.7) / 0.3 : p < 0.06 ? 1 + p / 0.06 * 0.04 : -1);
  const samples = [0, 0.025, 0.05, 0.075];
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
      {samples.map((d, i) => {
        let p = phase - d;
        p = ((p % 1) + 1) % 1;
        const k = vis(p);
        if (k < 0) return null;
        const yb = left[1] + (floorY + 30 - left[1]) * Math.min(1, k);
        const cx = (left[0] + right[0]) / 2;
        const path = `M ${left[0]} ${left[1]} C ${left[0] - spread} ${yb + 40}, ${right[0] + spread} ${yb + 40}, ${right[0]} ${right[1]}`;
        return (
          <path key={i} d={path} stroke="#7d1f1c" strokeWidth={7 - i} fill="none" strokeLinecap="round"
            opacity={(0.85 - i * 0.2) * (k > 0.98 ? 1 : 0.8)} style={{filter: `blur(${1 + i * 1.6}px)`}} data-cx={cx} />
        );
      })}
    </svg>
  );
};

/** Corda caída e enroscada no tênis após o tropeço. */
export const RopeCaught: React.FC<{left: [number, number]; right: [number, number]; floorY: number; spread: number; opacity: number}> = ({
  left, right, floorY, spread, opacity,
}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', opacity}}>
    <path d={`M ${left[0]} ${left[1]} C ${left[0] - spread} ${floorY + 20}, ${right[0] + spread * 0.4} ${floorY - 30}, ${right[0]} ${right[1]}`}
      stroke="#7d1f1c" strokeWidth={7} fill="none" strokeLinecap="round" style={{filter: 'blur(0.6px)'}} />
  </svg>
);

/** Gota de suor que escorre (coordenadas do mundo). */
export const SweatDrop: React.FC<{t: number; t0: number; t1: number; from: [number, number]; to: [number, number]}> = ({t, t0, t1, from, to}) => {
  if (t < t0 - 0.4 || t > t1 + 0.6) return null;
  const p = Math.max(0, Math.min(1, (t - t0) / (t1 - t0)));
  const e = p * p * (3 - 2 * p);
  const x = from[0] + (to[0] - from[0]) * e;
  const y = from[1] + (to[1] - from[1]) * e;
  const op = Math.min(1, (t - (t0 - 0.4)) / 0.4) * (t > t1 ? Math.max(0, 1 - (t - t1) / 0.6) : 1);
  const stretch = 1 + 0.35 * Math.sin(Math.PI * p);
  return (
    <div style={{
      position: 'absolute', left: x - 9, top: y - 13 * stretch, width: 18, height: 26 * stretch, opacity: op * 0.9,
      borderRadius: '50% 50% 50% 50% / 62% 62% 40% 40%',
      background: 'radial-gradient(ellipse 40% 30% at 38% 62%, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.15) 55%), radial-gradient(ellipse at 50% 70%, rgba(255,230,200,0.35), rgba(160,90,40,0.25))',
      boxShadow: '0 2px 3px rgba(80,30,0,0.35)', border: '1px solid rgba(255,255,255,0.35)',
    }} />
  );
};

/** Brilho nos olhos (estrela de quatro pontas). */
export const EyeGlint: React.FC<{x: number; y: number; k: number; size?: number}> = ({x, y, k, size = 26}) =>
  k <= 0 ? null : (
    <div style={{position: 'absolute', left: x - size, top: y - size, width: size * 2, height: size * 2, opacity: k, mixBlendMode: 'screen'}}>
      <div style={{position: 'absolute', left: size - 1.5, top: 0, width: 3, height: size * 2, background: 'linear-gradient(transparent, #fff, transparent)'}} />
      <div style={{position: 'absolute', top: size - 1.5, left: 0, height: 3, width: size * 2, background: 'linear-gradient(90deg, transparent, #fff, transparent)'}} />
      <div style={{position: 'absolute', left: size - 5, top: size - 5, width: 10, height: 10, borderRadius: '50%', background: '#fff', filter: 'blur(2px)'}} />
    </div>
  );
