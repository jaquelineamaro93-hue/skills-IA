import React from 'react';
import {AbsoluteFill} from 'remotion';
import {handheld, kf, pulse} from '../animation/keys';
import {LayeredShot, clampCam} from '../components/LayeredShot';
import {Dust, LightRays, SunFlare} from '../components/Atmosphere';

/** CENA 02 — O menino do bairro: a câmera parte das casas coloridas na janela e desliza até Camilo; aproxima no sorriso. */
export const S2Bairro: React.FC<{t: number}> = ({t}) => {
  const cam = clampCam({
    x: kf(t, [[7.0, 330], [9.6, 360], [11.9, 540], [13.0, 548], [14.8, 556]]),
    y: kf(t, [[7.0, 600], [9.6, 640], [11.9, 900], [13.0, 880], [14.8, 600]]),
    s: kf(t, [[7.0, 1.6], [9.6, 1.52], [11.9, 1.06], [13.0, 1.1], [14.8, 1.34]]),
  });
  const sway = Math.sin(t * 1.1) * 0.35;
  const ear = pulse(t, 10.6, 0.35) - pulse(t, 13.9, 0.3) * 0.8;
  const lift = Math.min(1, Math.max(0, (t - 12.4) / 0.8));
  // posição aproximada da janela em tela (para o reflexo do sol)
  const sx = 540 + (194 - cam.x) * cam.s * 0.72;
  const sy = 960 + (216 - cam.y) * cam.s * 0.72;
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena2"
        cam={cam}
        offset={handheld(t, 0.7)}
        bgBlur={2.2}
        fgTransform={`rotate(${sway}deg) translateY(${-lift * 6 + Math.sin(t * 1.8) * 2}px)`}
        fgWarps={[{cx: 356, cy: 292, rx: 110, ry: 120, transform: `rotate(${-ear * 2.2}deg)`, origin: '380px 380px'}]}
      />
      <SunFlare x={sx} y={sy} size={700} intensity={0.75 + 0.15 * Math.sin(t * 0.8)} />
      <LightRays t={t} x={sx} y={sy - 100} angle={-24} intensity={0.8} />
      <Dust t={t} seed={2} />
    </AbsoluteFill>
  );
};
