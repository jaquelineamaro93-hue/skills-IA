---
name: ai-avatar-video
description: Produce vertical 9:16 talking-head reels of a REAL person's AI avatar ("yap content", AI influencer, mentor or founder videos) that speak with that person's own cloned voice (ElevenLabs), with a locked identity, one consistent scene, five camera angles, natural-paced voice synced to the lips, lower-third cards (chat print, steps, quote), an end card with the CTA and low background music. Use when someone sends their photos/video + voice files + scripts and asks for avatar/influencer videos, a batch of reels, a character sheet for a consistent AI face, or fixes to such videos: face not matching, eyebrows/glasses/earrings wrong, aged look or wrinkles, background swap, voice out of sync or speeding up/slowing down, mispronounced words, clicks, cut-off CTA.
---
# AI Avatar Video

Entrega: **um MP4 por roteiro**, 9:16, 720×1280, 24 fps, voz ORIGINAL da pessoa no ritmo dela, na boca do avatar.
Siga as etapas na ordem. Leia o arquivo de `references/` indicado em cada etapa ANTES de executá-la.

## 7 regras (cada uma veio de um erro real)
1. **Consentimento.** Só o rosto e a voz da própria pessoa ou de quem autorizou por escrito. Sem isso, recuse.
2. **Fotos reais travam a identidade.** Nunca use imagem gerada como referência de rosto. Corrija tudo na imagem-base, antes do vídeo.
3. **Voz final = arquivo original.** A fala do gerador de vídeo troca palavras: descarte sempre.
4. **Ritmo natural > sincronia perfeita.** Uma velocidade por frase (0,85–1,15x). Nunca estique palavra por palavra.
5. **Expressão jovem e relaxada.** Bloco EXPRESSIONS em todo prompt; tags de frustração viram meio-sorriso.
6. **Custo com "ok".** Mostre o custo, espere a resposta, gere 1 teste, só depois o lote.
7. **CTA inteiro.** Em todo vídeo, confira a transcrição dos últimos 8 s.

## Etapas
| # | Etapa | Faça | Pare e peça aprovação? |
|---|---|---|---|
| 0 | Ambiente | `python3 scripts/check_env.py --download-model` | não |
| 1 | Perfil | Preencha `PERFIL.md` (modelo em `examples/`) e crie `NOTAS.md`. Pergunte só o que faltar. | não |
| 2 | Identidade | Ficha de personagem + imagem-base 9:16 → `references/ficha-de-personagem.md` | **sim, item a item** |
| 3 | Voz | Um `Rxx.mp3` por roteiro → `references/voz-elevenlabs.md`. Arquivo sem nome? transcreva o início e mapeie. | não |
| 4 | Plano | `scripts/words.py --lang pt R01.mp3`; blocos ≤ limite do gerador cortados em pausas; 5 planos; cards → `references/geradores.md`, `roteiro-e-ganchos.md` | não |
| 5 | Geração | Prompt de `references/prompt-video.md` com as frases EXATAS da transcrição; custo; 1 teste | **sim: custo e teste** |
| 6 | Pós | `voice_sync` → (`soften_wrinkles`) → `endcard` → `assemble` → `references/pos-producao.md` | não |
| 7 | QA | `scripts/qa_check.py final/R01.mp4` + `references/checklist-qa.md` | entrega com prova |

```bash
python3 scripts/voice_sync.py out/A.mp4 R01.mp3 out/A_fit.wav --ranges 0-28.4    # leia: speeds 0.85-1.15x
python3 scripts/soften_wrinkles.py out/A.mp4 out/A_soft.mp4 0.8                    # só se pedirem pele lisa
python3 scripts/endcard.py frame.png R01.mp3 54.4 63.4 out/endcard.mp4 "Linha|site.com|Link na bio" "KICKER"
python3 scripts/assemble.py plan.json
python3 scripts/qa_check.py final/R01.mp4 --lang pt                                # joins: none · END com o CTA
```

## Ao entregar
MP4 + 3 linhas: o que foi feito, a duração, o que a pessoa deve conferir. Atualize `NOTAS.md` (aprovado, rejeitado, custo).
Pedido de correção: repita em 1 linha o que entendeu, corrija só aquilo e mostre a prova (close, frame, transcrição do fim).

## Quando algo der errado
Antes de improvisar, procure o sintoma em `references/licoes-aprendidas.md`: rosto "embelezado", sobrancelha escura ou apagada, brinco de um lado só, fundo com cara de recorte, cara de velha, voz lenta que acelera do nada, sílaba repetida na emenda, CTA cortado aos 20 s. Cada item tem a causa e a correção testada.
