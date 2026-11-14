import React from 'react';
import {AbsoluteFill} from 'remotion';
import {ramp} from '../animation/keys';
import {Dust} from './Atmosphere';

/** Tela final: CAMILO / EPISÓDIO 1 | O TAMANHO DO SONHO. t0 = início do cartão. */
export const EndCard: React.FC<{t: number; t0: number; t1: number}> = ({t, t0, t1}) => {
  const a = ramp(t, t0 + 0.3, t0 + 1.6);
  const b = ramp(t, t0 + 1.3, t0 + 2.2);
  const line = ramp(t, t0 + 0.9, t0 + 2.0);
  const out = 1 - ramp(t, t1 - 0.45, t1 - 0.05);
  return (
    <AbsoluteFill style={{backgroundColor: '#060302', justifyContent: 'center', alignItems: 'center', opacity: out}}>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 60% 40% at 50% 48%, rgba(120,60,15,0.35) 0%, rgba(0,0,0,0) 70%)'}} />
      <Dust t={t} count={26} seed={9} intensity={0.5} />
      <div style={{textAlign: 'center', marginTop: -60}}>
        <div style={{
          fontFamily: 'Anton', fontSize: 230, lineHeight: 1, letterSpacing: 18 + 26 * (1 - a), paddingLeft: 18 + 26 * (1 - a),
          opacity: a, transform: `scale(${1.06 - 0.06 * a})`,
          background: 'linear-gradient(180deg, #FFE7A8 0%, #F2B544 55%, #C9781E 100%)',
          WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
          filter: 'drop-shadow(0 6px 24px rgba(255,150,40,0.35))',
        }}>
          CAMILO
        </div>
        <div style={{height: 3, width: 640 * line, margin: '34px auto 30px', background: 'linear-gradient(90deg, transparent, #F2B544, transparent)'}} />
        <div style={{fontFamily: 'Montserrat', fontWeight: 700, fontSize: 38, letterSpacing: 7, color: '#F6EBDD', opacity: b, transform: `translateY(${(1 - b) * 14}px)`}}>
          EPISÓDIO 1 <span style={{color: '#F2B544'}}>|</span> O TAMANHO DO SONHO
        </div>
      </div>
    </AbsoluteFill>
  );
};
