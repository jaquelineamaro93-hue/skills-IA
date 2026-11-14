import React from 'react';
import {AbsoluteFill} from 'remotion';
import {handheld, kf, pulse, ramp} from '../animation/keys';
import {LayeredShot, clampCam} from '../components/LayeredShot';
import {Dust, LightRays, SunFlare} from '../components/Atmosphere';
import {EyeGlint} from '../components/Effects';

/** CENA 07 — O tamanho do sonho: luz dourada, aproximação lenta até os olhos, guarda ajustada, brilho no olhar. */
export const S7Sonho: React.FC<{t: number}> = ({t}) => {
  const cam = clampCam({
    x: kf(t, [[42.7, 540], [47.0, 548], [50.8, 552], [55.5, 552]]),
    y: kf(t, [[42.7, 1000], [47.0, 760], [50.8, 660], [55.5, 640]]),
    s: kf(t, [[42.7, 1.06], [47.0, 1.28], [50.8, 1.42], [55.5, 1.52]]),
  });
  const guard = ramp(t, 48.9, 49.5);
  const glint = pulse(t, 48.4, 1.6) * 0.75 + pulse(t, 52.6, 1.4) * 0.6;
  const ear = pulse(t, 45.6, 0.35);
  const sx = 540 + (194 - cam.x) * cam.s * 0.72;
  const sy = 960 + (216 - cam.y) * cam.s * 0.72;
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena2"
        cam={cam}
        offset={handheld(t, 0.5)}
        bgBlur={3.5}
        fgTransform={`translateY(${-guard * 7 + Math.sin(t * 1.4) * 2}px) rotate(${-guard * 0.5}deg)`}
        fgWarps={[{cx: 356, cy: 292, rx: 110, ry: 120, transform: `rotate(${-ear * 2.2}deg)`, origin: '380px 380px'}]}
        onCharacter={
          <>
            <EyeGlint x={436} y={452} k={glint} />
            <EyeGlint x={704} y={432} k={glint * 0.8} size={20} />
          </>
        }
      />
      <SunFlare x={sx} y={sy} size={900} intensity={0.85 + 0.15 * Math.sin(t * 0.6)} />
      <LightRays t={t} x={sx} y={sy - 120} angle={-26} intensity={1} />
      <Dust t={t} seed={7} intensity={1.1} />
    </AbsoluteFill>
  );
};
