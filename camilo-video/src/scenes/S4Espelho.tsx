import React from 'react';
import {AbsoluteFill} from 'remotion';
import timeline from '../timeline.json';
import {handheld, kf, pulse} from '../animation/keys';
import {LayeredShot} from '../components/LayeredShot';
import {Dust, LightRays} from '../components/Atmosphere';

const B = timeline.beats;

/** CENA 04 — O espelho rachado: travelling lateral; esquivas e socos no ar com reflexo acompanhando. */
export const S4Espelho: React.FC<{t: number}> = ({t}) => {
  const cam = {x: kf(t, [[21.8, 470], [30.0, 620]]), y: kf(t, [[21.8, 880], [30.0, 830]]), s: kf(t, [[21.8, 1.12], [30.0, 1.16]])};
  const weave = B.weaves.reduce((a, tc, i) => a + pulse(t, tc - 0.15, 0.5) * (i % 2 ? 1 : -1), 0);
  const punchAt = (tt: number) => B.airPunches.reduce((a, tc) => a + (tt > tc - 0.1 && tt < tc + 0.18 ? Math.sin((Math.PI * (tt - (tc - 0.1))) / 0.28) : 0), 0);
  const p = punchAt(t);
  const tf = (pp: number, w: number) => `translate(${w * 30 - pp * 22}px, ${Math.abs(w) * 8 - pp * 4}px) rotate(${-w * 3.2}deg) scale(${1 + pp * 0.018})`;
  const ghosts = p > 0.2 ? [1, 2, 3].map((k) => ({transform: tf(punchAt(t - k / 90), weave), opacity: 0.22 / k})) : [];
  const dx = weave * 30 - p * 22;
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena5"
        cam={cam}
        offset={handheld(t, 0.9)}
        bgBlur={1.6}
        fgOrigin="500px 1600px"
        fgTransform={tf(p, weave)}
        ghosts={ghosts}
        // reflexo no espelho acompanha a esquiva
        bgWarps={[{cx: 950, cy: 700, rx: 150, ry: 210, transform: `translateX(${dx * 0.45}px) rotate(${-weave * 1.5}deg)`}]}
      />
      <LightRays t={t} x={100} y={-200} angle={-22} intensity={0.85} />
      <Dust t={t} seed={4} />
    </AbsoluteFill>
  );
};
