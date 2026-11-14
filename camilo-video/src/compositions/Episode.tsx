import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import timeline from '../timeline.json';
import {FPS, ramp} from '../animation/keys';
import {loadFonts} from '../fonts';
import {FilmFinish} from '../components/Atmosphere';
import {Subtitles} from '../components/Subtitles';
import {EndCard} from '../components/EndCard';
import {S1Ataduras} from '../scenes/S1Ataduras';
import {S2Bairro} from '../scenes/S2Bairro';
import {S3Corda} from '../scenes/S3Corda';
import {S4Espelho} from '../scenes/S4Espelho';
import {S5Suor} from '../scenes/S5Suor';
import {S6Golpe} from '../scenes/S6Golpe';
import {S7Sonho} from '../scenes/S7Sonho';

loadFonts();

type In = {kind: 'fade' | 'whip' | 'cut'; dur: number};
const SC = timeline.scenes;
const parts: {C: React.FC<{t: number}>; start: number; end: number; tin: In}[] = [
  {C: S1Ataduras, start: SC[0].start, end: SC[0].end, tin: {kind: 'cut', dur: 0}},
  {C: S2Bairro, start: SC[1].start, end: SC[1].end, tin: {kind: 'fade', dur: 0.7}},
  {C: S3Corda, start: SC[2].start, end: SC[2].end, tin: {kind: 'whip', dur: 0.3}},
  {C: S4Espelho, start: SC[3].start, end: SC[3].end, tin: {kind: 'fade', dur: 0.35}},
  {C: S5Suor, start: SC[4].start, end: SC[4].end, tin: {kind: 'cut', dur: 0}},
  {C: S6Golpe, start: SC[5].start, end: SC[5].end, tin: {kind: 'cut', dur: 0}},
  {C: S7Sonho, start: SC[6].start, end: SC[6].end, tin: {kind: 'fade', dur: 0.9}},
];

/** Episódio completo. As cenas leem o tempo global; transições de entrada sobrepõem a cena anterior. */
export const Episode: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  const end = timeline.duration;
  const s8 = SC[7].start;
  // mergulhos no preto: abertura, passagem S4→S5 (mudança de clima)
  const dip = Math.max(1 - ramp(t, 0, 0.9), 1 - Math.min(1, Math.abs(t - SC[4].start) / 0.35));
  const leak = Math.max(0, 1 - Math.abs(t - SC[1].start) / 0.45);
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Audio src={staticFile('mix/master.wav')} />
      {parts.map(({C, start, end: e, tin}, i) => {
        const next = parts[i + 1];
        const visEnd = next ? next.start : s8 + 1.2;
        if (t < start - tin.dur || t >= visEnd) return null;
        let style: React.CSSProperties = {};
        if (tin.kind === 'fade') style = {opacity: ramp(t, start - tin.dur, start)};
        if (tin.kind === 'whip') {
          const k = ramp(t, start - tin.dur, start + 0.15);
          style = {opacity: Math.min(1, k * 3), transform: `translateY(${(1 - k) * -340}px)`, filter: k < 1 ? `blur(${(1 - k) * 22}px)` : undefined};
        }
        return (
          <AbsoluteFill key={i} style={{...style, filter: [style.filter, 'contrast(1.04) saturate(1.06)'].filter(Boolean).join(' ')}}>
            <C t={t} />
          </AbsoluteFill>
        );
      })}
      {/* chicote de câmera saindo de S2 (borrão) */}
      {t > SC[2].start - 0.35 && t < SC[2].start && (
        <AbsoluteFill style={{backdropFilter: `blur(${ramp(t, SC[2].start - 0.35, SC[2].start) * 18}px)`}} />
      )}
      <AbsoluteFill style={{background: `radial-gradient(ellipse at 20% 15%, rgba(255,190,110,${0.55 * leak}) 0%, rgba(255,120,40,${0.25 * leak}) 40%, rgba(0,0,0,0) 75%)`, mixBlendMode: 'screen'}} />
      {t >= s8 - 1.0 && (
        <AbsoluteFill style={{opacity: ramp(t, s8 - 1.0, s8)}}>
          <EndCard t={t} t0={s8} t1={end} />
        </AbsoluteFill>
      )}
      <FilmFinish />
      <AbsoluteFill style={{backgroundColor: '#000', opacity: dip}} />
      {t < s8 && <Subtitles t={t} />}
    </AbsoluteFill>
  );
};
