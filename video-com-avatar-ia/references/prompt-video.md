# Prompt do vídeo (modelos de referência com áudio: Seedance 2.x/2.5, Kling, Veo R2V)

Prompt em inglês, falas em português (ou no idioma do áudio). As frases vão entre aspas EXATAMENTE como a
transcrição do áudio (`words.py`), não como no roteiro escrito: assim os cortes caem nas pausas reais.

## Referências (nesta ordem)
`@image1` imagem-base aprovada · `@image2` cenário 9:16 · `@image3`/`@image4` fotos reais do rosto ·
`@video1` trecho real falando (8–15 s) · `@audio1` o bloco de áudio da ElevenLabs que guia a boca.

## Modelo
```
A polished vertical talking-head video of the same real [woman/man] in @image1[, without earrings]. @image1 is the
master reference for identity and outfit: preserve the exact face, facial features, skin, body shape and outfit -
<OUTFIT>. [Without earrings: both earlobes bare in every shot.] Eyebrows: <BROW COLOR AND SHAPE>, visible, never
darker and never erased. Hair: <HAIR>, same color from roots to ends. [Glasses: <EXACT MODEL> in every shot.]
Do not beautify, slim, or change any facial trait.
EXPRESSIONS: youthful, relaxed facial expressions in every shot: smooth relaxed forehead, no frowning, no furrowed or
knitted brows, no squinting, no pursed or puckered lips, no downturned mouth. Eyes bright and open, soft natural
smile between sentences. Show emotion with the eyes, head tilts and hands, not with forehead lines. Keep natural
skin texture [and freckles].
@image2 shows only the location: <LOCATION>. Place [her/him] naturally in it, filmed on location with real natural
light on face and hair, consistent shadows, background slightly blurred with light shallow depth of field (still
recognizable). Do not use the room from @image1. @image3 and @image4 are real photos of the same face, only for
identity. @video1 shows the real speaking mannerisms, head tilts, hand gestures and diction; do not copy its room,
outfit or lighting. [With cards:] Keep face and shoulders in the upper two-thirds of the frame in every shot (the
lower part of the frame will hold graphics).

[She/He] speaks directly to the viewer in Brazilian Portuguese, lip-synced exactly to @audio1, [her/his] own voice
and the only dialogue, from the first to the last word. Five camera angles with hard cuts at sentence pauses, same
location in all shots:
Shot 1 ("<exact sentence>"): frontal medium close-up, <expression>, <gesture>.
Shot 2 ("<exact sentence>"): slow push-in to a close-up, <expression>.
Shot 3 ("<exact sentence>"): three-quarter left medium shot, <gesture>.
Shot 4 ("<exact sentence>"): frontal medium shot, <expression>.
Shot 5 ("<exact sentence>"): wider medium shot with the location visible behind, warm smile, open hand toward the viewer.
Sound: speech from @audio1 only, very quiet ambience, no music. No text, no subtitles, no microphone visible.
```

## Tag de emoção (ElevenLabs) → expressão do plano
| Tag | Expressão no prompt |
|---|---|
| `[warmly]` `[happy]` `[smiles]` | warm smile, soft eyes |
| `[confident]` `[emphatic]` | steady eye contact, small firm nod, open-hand gesture |
| `[curious]` | eyebrows slightly raised, head tilt, light smile |
| `[thoughtful]` | calm gaze, eyes slightly up, relaxed face |
| `[softly]` `[sincere]` | gentle smile, soft eyes, slower nod |
| `[frustrated]` `[sighs]` | light knowing half-smile, slight head tilt, relaxed brows (NUNCA testa franzida) |
| `[excited]` | bright eyes, bigger smile, hands open |
| `[matter-of-fact]` `[conversational]` | relaxed neutral face, natural hand movement |

## Planos que funcionam (troque para não repetir entre vídeos)
frontal medium close-up · slow push-in to close-up · three-quarter left/right medium · tight close-up slightly low ·
wider medium with location visible · high three-quarter for the CTA (points to the viewer on the CTA word).
