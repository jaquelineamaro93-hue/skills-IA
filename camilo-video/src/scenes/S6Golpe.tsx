import React from 'react';
import {AbsoluteFill} from 'remotion';
import timeline from '../timeline.json';
import {Easing} from 'remotion';
import {damped, handheld, kf, shake} from '../animation/keys';
import {LayeredShot, clampCam} from '../components/LayeredShot';
import {Dust, LightRays} from '../components/Atmosphere';
import {Flash, ImpactBurst} from '../components/Effects';

const B = timeline.beats;
const accel = Easing.in(Easing.cubic);

/** Recuo do corpo antes do golpe (0 = pose de contato da imagem original). */
const retract = (t: number) =>
  kf(t, [[36.5, 70], [B.punchWindup, 70], [B.punchImpact - 0.15, 98]]) * (t < B.punchImpact - 0.15 ? 1 : 0) +
  (t >= B.punchImpact - 0.15 && t < B.punchImpact ? 98 - 104 * accel((t - (B.punchImpact - 0.15)) / 0.15) : 0) +
  (t >= B.punchImpact ? kf(t, [[B.punchImpact, -6], [B.punchImpact + 0.25, 0], [B.punchImpact + 0.55, 0], [B.punchImpact + 1.2, 26]]) : 0);

/** CENA 06 — O golpe: contra-plongée, respiração, preparação e soco no saco com impacto. */
export const S6Golpe: React.FC<{t: number}> = ({t}) => {
  const cam = clampCam({
    x: kf(t, [[36.8, 600], [39.5, 560], [B.punchImpact + 0.6, 560], [41.5, 626], [44, 630]]),
    y: kf(t, [[36.8, 1000], [39.5, 900], [B.punchImpact + 0.6, 900], [41.5, 700], [44, 690]]),
    s: kf(t, [[36.8, 1.2], [39.5, 1.28], [B.punchImpact, 1.3], [B.punchImpact + 0.05, 1.36], [B.punchImpact + 0.6, 1.3], [41.5, 1.4], [44, 1.44]]),
  });
  const tf = (tt: number) => {
    const r = retract(tt);
    const br = tt < B.punchWindup ? Math.sin((2 * Math.PI * tt) / 2.2) : 0;
    return `translate(${r}px, ${br * 3 - r * 0.08}px) rotate(${r * 0.04}deg) scale(${1 + br * 0.004})`;
  };
  const striking = t > B.punchImpact - 0.15 && t < B.punchImpact + 0.05;
  const ghosts = striking ? [1, 2, 3, 4].map((k) => ({transform: tf(t - k / 120), opacity: 0.25 / k})) : [];
  const sh = shake(t, B.punchImpact, 20, 6);
  const hh = handheld(t, 1);
  const bag = damped(t, B.punchImpact, 1.1, 2.2);
  const dent = t >= B.punchImpact ? Math.exp(-(t - B.punchImpact) * 9) : 0;
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena3"
        cam={cam}
        offset={{x: hh.x + sh.x, y: hh.y + sh.y, r: hh.r + sh.r}}
        bgBlur={2}
        fgOrigin="700px 1750px"
        fgTransform={tf(t)}
        ghosts={ghosts}
        bgWarps={[
          // saco balança na corrente e afunda no ponto de impacto
          {cx: 190, cy: 640, rx: 260, ry: 520, transform: `rotate(${-bag * 1.6}deg) translateX(${-dent * 10}px)`, origin: '260px 0px'},
        ]}
        front={<ImpactBurst t={t} t0={B.punchImpact} x={238} y={626} />}
      />
      <Flash t={t} t0={B.punchImpact} />
      <LightRays t={t} x={300} y={1000} angle={-35} intensity={0.55} />
      <Dust t={t} seed={6} />
    </AbsoluteFill>
  );
};
