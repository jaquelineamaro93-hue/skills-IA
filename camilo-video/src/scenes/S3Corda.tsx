import React from 'react';
import {AbsoluteFill} from 'remotion';
import timeline from '../timeline.json';
import {handheld, kf, ramp, shake} from '../animation/keys';
import {LayeredShot, clampCam} from '../components/LayeredShot';
import {Dust, LightRays} from '../components/Atmosphere';
import {RopeCaught, RopeStreak} from '../components/Effects';

const B = timeline.beats;
const beat = 60 / timeline.bpm;

/** CENA 03 — Treinar também é cair: pulos de corda em plano fechado nas pernas, tropeço, reação e nova tentativa.
 *  Não há imagem de referência de Camilo pulando corda: a corda é desenhada como rastro em movimento
 *  sobre o recorte do personagem (limitação documentada). */
export const S3Corda: React.FC<{t: number}> = ({t}) => {
  const whip = ramp(t, B.stumble + 0.45, B.stumble + 0.85);
  const cam = clampCam({
    x: kf(t, [[14.6, 500], [B.stumble + 0.45, 500], [B.stumble + 0.85, 370], [22.6, 360]]),
    y: kf(t, [[14.6, 1300], [B.stumble + 0.45, 1300], [B.stumble + 0.85, 660], [20.9, 640], [22.6, 620]]),
    s: kf(t, [[14.6, 1.55], [B.stumble + 0.45, 1.6], [B.stumble + 0.85, 1.42], [20.9, 1.42], [21.4, 1.52], [22.6, 1.55]]),
  });
  const ropeOn = t >= B.ropeStart - 0.5 && t < B.stumble;
  const hop = ropeOn && t >= B.ropeStart - beat / 2 ? Math.abs(Math.sin((Math.PI * (t - B.ropeStart)) / beat)) : 0;
  const phase = (t - B.ropeStart) / beat;
  const st = shake(t, B.stumble + 0.02, 14, 6);
  const fall = ramp(t, B.stumble, B.stumble + 0.22) * (1 - ramp(t, B.stumble + 0.9, B.stumble + 1.6));
  const guardUp = ramp(t, 20.95, 21.35);
  const hh = handheld(t, 1);
  const blur = Math.sin(Math.PI * whip) * 14;
  const L: [number, number] = [238, 880];
  const R: [number, number] = [713, 905];
  return (
    <AbsoluteFill style={{filter: blur > 0.3 ? `blur(${blur}px)` : undefined}}>
      <LayeredShot
        image="cena5"
        cam={cam}
        offset={{x: hh.x + st.x, y: hh.y + st.y, r: hh.r + st.r}}
        bgBlur={2.5}
        fgOrigin="560px 1600px"
        fgTransform={`translate(${fall * 10}px, ${-hop * 30 + fall * 14 - guardUp * 6}px) rotate(${fall * 5}deg) scaleY(${1 - (hop < 0.15 && ropeOn ? 0.012 : 0)})`}
        front={
          <>
            {ropeOn && <RopeStreak phase={phase} left={L} right={R} floorY={1640} spread={420} />}
            {t >= B.stumble && t < B.stumble + 1.0 && (
              <RopeCaught left={L} right={R} floorY={1640} spread={420} opacity={1 - ramp(t, B.stumble + 0.6, B.stumble + 0.9)} />
            )}
          </>
        }
      />
      <LightRays t={t} x={120} y={-150} angle={-20} intensity={0.7} />
      <Dust t={t} seed={3} intensity={0.8} />
    </AbsoluteFill>
  );
};
