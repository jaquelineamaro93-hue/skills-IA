import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {H, W, rand} from '../animation/keys';

/** Poeira suspensa iluminada pelo sol (coordenadas de tela). */
export const Dust: React.FC<{t: number; count?: number; seed?: number; intensity?: number; area?: [number, number, number, number]}> = ({
  t, count = 46, seed = 1, intensity = 1, area = [0, 0, W, H],
}) => {
  const [ax, ay, aw, ah] = area;
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
      {new Array(count).fill(0).map((_, i) => {
        const r1 = rand(seed * 100 + i), r2 = rand(seed * 200 + i), r3 = rand(seed * 300 + i);
        const size = 2 + r3 * 7;
        const x = ax + ((r1 * aw + t * (6 + 14 * r2) + Math.sin(t * 0.6 + i) * 18) % aw);
        const y = ay + (((r2 * ah - t * (10 + 16 * r3) + Math.cos(t * 0.4 + i * 2) * 14) % ah) + ah) % ah;
        const tw = 0.35 + 0.65 * Math.abs(Math.sin(t * (0.8 + r1) + i));
        return (
          <div key={i} style={{
            position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(255,236,190,0.95) 0%, rgba(255,200,120,0) 70%)',
            opacity: tw * intensity * (0.4 + 0.6 * r3), filter: size > 6 ? 'blur(1.5px)' : undefined,
          }} />
        );
      })}
    </AbsoluteFill>
  );
};

/** Raios de luz entrando pela janela. origin em tela; angle em graus. */
export const LightRays: React.FC<{t: number; x: number; y: number; angle: number; intensity?: number; color?: string}> = ({
  t, x, y, angle, intensity = 1, color = '255,196,120',
}) => (
  <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
    {[0, 1, 2, 3].map((i) => {
      const w = 90 + i * 70;
      const flick = 0.75 + 0.25 * Math.sin(t * (0.5 + i * 0.17) + i * 1.7);
      return (
        <div key={i} style={{
          position: 'absolute', left: x - w / 2 + (i - 1.5) * 110, top: y, width: w, height: 2600,
          transformOrigin: `${w / 2 - (i - 1.5) * 110}px 0px`, transform: `rotate(${angle + (i - 1.5) * 4}deg)`,
          background: `linear-gradient(180deg, rgba(${color},${0.32 * flick * intensity}) 0%, rgba(${color},${0.1 * flick * intensity}) 45%, rgba(${color},0) 85%)`,
          filter: 'blur(26px)',
        }} />
      );
    })}
  </AbsoluteFill>
);

/** Brilho de sol / reflexo de lente. */
export const SunFlare: React.FC<{x: number; y: number; size?: number; intensity?: number}> = ({x, y, size = 520, intensity = 1}) => (
  <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
    <div style={{
      position: 'absolute', left: x - size / 2, top: y - size / 2, width: size, height: size, borderRadius: '50%',
      background: 'radial-gradient(circle, rgba(255,240,200,0.75) 0%, rgba(255,190,110,0.35) 25%, rgba(255,140,60,0) 70%)',
      opacity: intensity,
    }} />
  </AbsoluteFill>
);

/** Correção de cor, vinheta e granulação de filme (camada global). */
export const FilmFinish: React.FC<{warm?: number}> = ({warm = 0.18}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: `rgba(255,150,60,${warm})`, mixBlendMode: 'soft-light'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 62% at 50% 45%, rgba(0,0,0,0) 55%, rgba(10,4,0,0.55) 100%)'}} />
      <svg width={W} height={H} style={{position: 'absolute', opacity: 0.07, mixBlendMode: 'overlay'}}>
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={frame % 24} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
