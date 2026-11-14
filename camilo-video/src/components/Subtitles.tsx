import React from 'react';
import {AbsoluteFill} from 'remotion';
import timeline from '../timeline.json';

export type Cue = {start: number; end: number; lines: string[]; speaker: string};

/** Monta as legendas a partir da timeline (mesma lógica de scripts/make_srt.py). */
export const buildCues = (): Cue[] => {
  const cues: Cue[] = [];
  const clips = timeline.voiceClips as Record<string, {in: number; out: number; speaker: string}>;
  for (const s of timeline.subtitles as {voice: string; lines?: string[]; split?: number; parts?: {lines: string[]}[]}[]) {
    const ev = timeline.voiceEvents.find((e) => e.id === s.voice)!;
    const c = clips[s.voice];
    const a = ev.at + 0.02;
    const b = ev.at + (c.out - c.in) + 0.12;
    if (s.parts && s.split) {
      cues.push({start: a, end: ev.at + s.split, lines: s.parts[0].lines, speaker: c.speaker});
      cues.push({start: ev.at + s.split, end: b, lines: s.parts[1].lines, speaker: c.speaker});
    } else {
      cues.push({start: a, end: b, lines: s.lines!, speaker: c.speaker});
    }
  }
  return cues;
};

const CUES = buildCues();

const renderLine = (line: string) =>
  line.split(/(\*[^*]+\*)/g).map((part, i) =>
    part.startsWith('*') ? (
      <span key={i} style={{color: '#FFD23F'}}>{part.slice(1, -1)}</span>
    ) : (
      <span key={i}>{part}</span>
    ),
  );

/** Legendas: branco, sombra discreta, destaque amarelo, máx. 2 linhas, área segura de Reels/TikTok/Shorts.
 *  Falas do Camilo em itálico (voz interior / fala do personagem). */
export const Subtitles: React.FC<{t: number; bottom?: number}> = ({t, bottom = 440}) => {
  const cue = CUES.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  const fin = Math.min(1, (t - cue.start) / 0.12);
  const fout = Math.min(1, (cue.end - t) / 0.12);
  const k = Math.max(0, Math.min(fin, fout));
  const camilo = cue.speaker === 'camilo';
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: bottom, pointerEvents: 'none'}}>
      <div style={{
        maxWidth: 1000, textAlign: 'center', opacity: k, transform: `translateY(${(1 - fin) * 10}px)`,
        fontFamily: 'Montserrat', fontWeight: camilo ? 800 : 700, fontStyle: camilo ? 'italic' : 'normal',
        fontSize: 50, lineHeight: 1.22, color: '#fff', letterSpacing: 0.2,
        textShadow: '0 3px 10px rgba(0,0,0,0.85), 0 0 2px rgba(0,0,0,0.9)',
      }}>
        {cue.lines.map((l, i) => (
          <div key={i} style={{whiteSpace: 'nowrap'}}>{renderLine(l)}</div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
