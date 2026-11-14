import React from 'react';
import {AbsoluteFill} from 'remotion';
import {loadFonts} from '../fonts';
import {LayeredShot} from '../components/LayeredShot';
import {Dust, FilmFinish, LightRays} from '../components/Atmosphere';
import {ImpactBurst} from '../components/Effects';

loadFonts();

/** Thumbnail vertical: o golpe (cena 3) + título. */
export const Thumbnail: React.FC = () => (
  <AbsoluteFill>
    <LayeredShot image="cena3" cam={{x: 560, y: 900, s: 1.12}} bgBlur={2.5} front={<ImpactBurst t={0.06} t0={0} x={238} y={626} />} />
    <LightRays t={2} x={300} y={1000} angle={-35} intensity={0.6} />
    <Dust t={3} seed={6} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(8,3,0,0.88) 86%)'}} />
    <FilmFinish />
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 300, textAlign: 'center'}}>
      <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 40, letterSpacing: 8, color: '#F6EBDD'}}>EPISÓDIO 1</div>
      <div style={{
        fontFamily: 'Anton', fontSize: 250, lineHeight: 1.0, letterSpacing: 14,
        background: 'linear-gradient(180deg, #FFE7A8 0%, #F2B544 55%, #C9781E 100%)',
        WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
        filter: 'drop-shadow(0 8px 26px rgba(0,0,0,0.7))',
      }}>CAMILO</div>
      <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 56, color: '#fff', textShadow: '0 4px 14px rgba(0,0,0,0.9)'}}>
        O TAMANHO DO <span style={{color: '#FFD23F'}}>SONHO</span>
      </div>
    </AbsoluteFill>
  </AbsoluteFill>
);
