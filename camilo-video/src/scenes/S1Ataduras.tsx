import React from 'react';
import {AbsoluteFill} from 'remotion';
import {handheld, kf, pulse} from '../animation/keys';
import {LayeredShot} from '../components/LayeredShot';
import {Dust, LightRays} from '../components/Atmosphere';

/** CENA 01 — O começo de um sonho: close nas patas enrolando as ataduras; travelling lento revelando o rosto concentrado. */
export const S1Ataduras: React.FC<{t: number}> = ({t}) => {
  const cam = {x: kf(t, [[0, 640], [7.6, 470]]), y: kf(t, [[0, 1000], [7.6, 830]]), s: kf(t, [[0, 1.55], [7.6, 1.17]])};
  const tugs = [0.9, 2.2, 3.4, 4.6, 6.0];
  const tug = tugs.reduce((a, tc) => a + pulse(t, tc, 0.5), 0);
  const fingers = Math.sin(t * 1.7) * 0.6 + pulse(t, 2.6, 0.8) * 1.2;
  const breath = Math.sin((2 * Math.PI * t) / 3.4);
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena1"
        cam={cam}
        offset={handheld(t, 0.8)}
        bgBlur={3}
        fgTransform={`translateY(${breath * 2.5}px) scale(${1 + breath * 0.003})`}
        fgWarps={[
          // pata puxando a atadura: pequenos puxões sincronizados ao som do tecido
          {cx: 470, cy: 650, rx: 230, ry: 200, transform: `translate(${tug * 2}px, ${-tug * 6}px)`},
          // dedos da pata enfaixada: micro movimentos
          {cx: 860, cy: 760, rx: 190, ry: 150, transform: `rotate(${fingers}deg)`, origin: '760px 930px'},
        ]}
      />
      <LightRays t={t} x={900} y={-200} angle={28} intensity={0.75} />
      <Dust t={t} seed={1} intensity={0.8} />
    </AbsoluteFill>
  );
};
