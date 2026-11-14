import React from 'react';
import {AbsoluteFill} from 'remotion';
import {handheld, kf} from '../animation/keys';
import {LayeredShot} from '../components/LayeredShot';
import {Dust} from '../components/Atmosphere';
import {SweatDrop} from '../components/Effects';

/** CENA 05 — A força de continuar: close com respiração cansada; a câmera sobe do peito aos olhos. */
export const S5Suor: React.FC<{t: number}> = ({t}) => {
  const cam = {x: kf(t, [[29.2, 520], [33.2, 515], [37.4, 500]]), y: kf(t, [[29.2, 1150], [33.0, 1080], [36.6, 790]]), s: kf(t, [[29.2, 1.25], [37.4, 1.32]])};
  const br = Math.sin((2 * Math.PI * (t - 29.7)) / 1.6);
  return (
    <AbsoluteFill>
      <LayeredShot
        image="cena4"
        cam={cam}
        offset={handheld(t, 0.6)}
        bgBlur={4}
        fgTransform={`translateY(${br * 3}px)`}
        fgWarps={[{cx: 560, cy: 1420, rx: 420, ry: 330, transform: `scaleY(${1 + br * 0.012}) scaleX(${1 + br * 0.006})`, origin: '560px 1800px'}]}
        onCharacter={<SweatDrop t={t} t0={33.4} t1={35.4} from={[262, 610]} to={[250, 790]} />}
      />
      <Dust t={t} seed={5} intensity={0.6} />
    </AbsoluteFill>
  );
};
