import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {H, W} from '../animation/keys';

/** Câmera virtual: ponto de foco (x, y) em coordenadas do quadro 1080×1920, escala s e rotação r (graus). */
export type Cam = {x: number; y: number; s: number; r?: number};

/** Deformação local suave: uma cópia da camada recortada por máscara elíptica com borda difusa,
 *  deslocada/rotacionada poucos pixels. Usada para tensão das ataduras, respiração, orelhas, saco e reflexo. */
export type Warp = {cx: number; cy: number; rx: number; ry: number; transform: string; origin?: string};

export const clampCam = (c: Cam): Cam => {
  const s = Math.max(1, c.s);
  const hx = W / 2 / s;
  const hy = H / 2 / s;
  return {...c, s, x: Math.min(W - hx, Math.max(hx, c.x)), y: Math.min(H - hy, Math.max(hy, c.y))};
};

const worldTransform = (c: Cam, ox = 0, oy = 0) =>
  `translate(${W / 2 + ox}px, ${H / 2 + oy}px) rotate(${c.r ?? 0}deg) scale(${c.s}) translate(${-c.x}px, ${-c.y}px)`;

const full: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: W, height: H};

const WarpLayer: React.FC<{src: string; w: Warp; filter?: string}> = ({src, w, filter}) => {
  const mask = `radial-gradient(ellipse ${w.rx}px ${w.ry}px at ${w.cx}px ${w.cy}px, #000 40%, transparent 100%)`;
  return (
    <div style={{...full, WebkitMaskImage: mask, maskImage: mask, transform: w.transform, transformOrigin: w.origin ?? `${w.cx}px ${w.cy}px`}}>
      <Img src={src} style={{...full, filter}} />
    </div>
  );
};

export const LayeredShot: React.FC<{
  image: string;
  cam: Cam;
  /** Câmera extra em pixels de tela (tremor, câmera na mão). */
  offset?: {x: number; y: number; r: number};
  parallax?: number;
  bgBlur?: number;
  fgTransform?: string;
  fgOrigin?: string;
  fgWarps?: Warp[];
  bgWarps?: Warp[];
  ghosts?: {transform: string; opacity: number}[];
  /** Elementos em coordenadas do mundo, atrás do personagem. */
  behind?: React.ReactNode;
  /** Elementos em coordenadas do mundo, à frente do personagem. */
  front?: React.ReactNode;
  /** Elementos em coordenadas do mundo que acompanham o personagem (mesma transformação dele). */
  onCharacter?: React.ReactNode;
}> = ({image, cam, offset, parallax = 0.72, bgBlur = 2.5, fgTransform = 'none', fgOrigin = '540px 1920px', fgWarps = [], bgWarps = [], ghosts = [], behind, front, onCharacter}) => {
  const c = clampCam(cam);
  const o = offset ?? {x: 0, y: 0, r: 0};
  const cc = {...c, r: (c.r ?? 0) + o.r};
  // fundo: move-se menos que o personagem (profundidade)
  const bgCam: Cam = {x: W / 2 + (c.x - W / 2) * parallax, y: H / 2 + (c.y - H / 2) * parallax, s: 1 + (c.s - 1) * parallax, r: cc.r};
  const bgSrc = staticFile(`layers/${image}_bg.jpg`);
  const fgSrc = staticFile(`layers/${image}_fg.png`);
  const bgFilter = `blur(${bgBlur}px)`;
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: '#120a05'}}>
      <div style={{...full, transformOrigin: '0 0', transform: worldTransform(bgCam, o.x * parallax, o.y * parallax)}}>
        <div style={{...full, transform: 'scale(1.07)', transformOrigin: '540px 960px'}}>
          <Img src={bgSrc} style={{...full, filter: bgFilter}} />
          {bgWarps.map((w, i) => (
            <WarpLayer key={i} src={bgSrc} w={w} filter={bgFilter} />
          ))}
        </div>
      </div>
      <div style={{...full, transformOrigin: '0 0', transform: worldTransform(cc, o.x, o.y)}}>
        {behind}
        {ghosts.map((g, i) => (
          <div key={i} style={{...full, transform: g.transform, transformOrigin: fgOrigin, opacity: g.opacity}}>
            <Img src={fgSrc} style={full} />
          </div>
        ))}
        <div style={{...full, transform: fgTransform, transformOrigin: fgOrigin}}>
          <Img src={fgSrc} style={full} />
          {fgWarps.map((w, i) => (
            <WarpLayer key={i} src={fgSrc} w={w} />
          ))}
          {onCharacter}
        </div>
        {front}
      </div>
    </AbsoluteFill>
  );
};
