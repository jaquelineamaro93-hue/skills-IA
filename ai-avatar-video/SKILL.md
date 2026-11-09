---
name: ai-avatar-video
description: Produce vertical 9:16 talking-head reels of a REAL person's AI avatar ("yap content", AI influencer, mentor or founder videos) that speak with that person's own cloned voice (ElevenLabs), with a locked identity, one consistent scene, five camera angles, word-accurate lip sync, lower-third cards (chat print, steps, quote), an end card with the CTA and low background music. Use when someone sends their photos/video + voice files + scripts and asks for avatar/influencer videos, a batch of reels, a character sheet for a consistent AI face, or fixes to such videos: face not matching, eyebrows/glasses/earrings wrong, aged look or wrinkles, background swap, voice out of sync, mispronounced words, clicks, cut-off CTA.
---
# AI Avatar Video — vídeos com o avatar e a voz clonada de uma pessoa real

Entrega: **um MP4 final por roteiro**, 9:16, 720×1280, 24 fps, com a voz ORIGINAL da pessoa sincronizada à boca do avatar.
Este arquivo é o fluxo. Os detalhes ficam em `references/` (leia cada um quando chegar na etapa) e as ferramentas em `scripts/`.

## Regras que nunca mudam
1. **Só com consentimento.** O avatar e a voz são da própria pessoa que pede, ou de alguém que autorizou por escrito. Recuse rostos e vozes de terceiros sem autorização (`references/etica-e-consentimento.md`).
2. **Nunca publique a voz gerada pelo modelo de vídeo.** Ela troca palavras. A voz final é sempre o arquivo original, sincronizado por `voice_sync.py`.
3. **Gasto só com "ok" explícito.** Antes de cada geração paga, mostre o custo (créditos ou valor) e espere a resposta. Gere 1 vídeo de teste antes do lote.
4. **Identidade se corrige na imagem-base, não no vídeo.** Cada correção depois da geração custa um vídeo inteiro.
5. **Um vídeo final só.** Se o roteiro passa do limite do gerador, divida em gerações do MESMO cenário e avise a pessoa que é um vídeo dividido só pelo limite, não dois vídeos.
6. **O CTA nunca é cortado.** Confira o fim da transcrição do vídeo final em todo vídeo.

## Fluxo (com os pontos de aprovação)
**0. Ambiente.** `python3 scripts/check_env.py` (instala o que faltar; `--download-model` baixa o Whisper uma vez).

**1. Briefing e perfil.** Crie `projeto/PERFIL.md` a partir de `examples/PERFIL-modelo.md`: aparência exata (cabelo e cor da raiz, sobrancelhas, óculos, piercings, acessórios, tatuagens), roupa, cenário, marca, CTA e URL, tom de voz, plataforma de geração disponível. Pergunte só o que faltar. Crie também `projeto/NOTAS.md` (aprovado, rejeitado, áudio→roteiro).

**2. Trava de identidade → APROVAÇÃO.** Gere a ficha do personagem (character sheet) e a imagem-base 9:16 só a partir de fotos reais (`references/ficha-de-personagem.md`). Mostre os dois e confira com a pessoa: olhos, nariz, boca, mandíbula, sobrancelhas, óculos, acessórios dos dois lados, cabelo. Não siga sem "aprovado".

**3. Voz.** Um áudio da ElevenLabs por roteiro, com tags de emoção e grafia fonética (`references/voz-elevenlabs.md`). Peça os arquivos com o número do roteiro no nome (`R01.mp3`). Se vierem com nome genérico, transcreva o início de cada um com `words.py` e mapeie no `NOTAS.md`.

**4. Plano de cenas.** `scripts/words.py --lang pt R01.mp3` → frases com tempos. Divida o áudio em blocos que caibam no limite do gerador (`references/geradores.md`), cortando em pausas reais. Para cada bloco: 5 planos (1 por frase), expressão por tag e onde entram os cards. Os cards precisam do rosto no terço de cima.

**5. Geração → CUSTO → APROVAÇÃO do teste.** Monte o prompt com `references/prompt-video.md` (inclui o bloco de expressões jovens e as frases EXATAS da transcrição). Consulte o custo, peça o "ok", gere o bloco de teste, mostre e só então gere o resto.

**6. Pós-produção** (`references/pos-producao.md`):
```bash
python3 scripts/voice_sync.py out/A.mp4 R01.mp3 out/A_fit.wav --ranges 0-28.4     # voz original na boca
python3 scripts/soften_wrinkles.py out/A.mp4 out/A_soft.mp4 0.8                     # se pedirem pele lisa
python3 scripts/endcard.py frame.png R01.mp3 54.4 63.4 out/endcard.mp4 "Linha 1|site.com|Link na bio" "KICKER"
python3 scripts/assemble.py plan.json                                              # cards + emendas + música
```
**7. QA.** `python3 scripts/qa_check.py final/R01.mp4 --lang pt` e a lista de `references/checklist-qa.md`. Olhe a folha de contato (`*_qa.jpg`) de verdade: identidade, sobrancelha, acessórios, testa, fundo, cards legíveis. Confira o "END" da transcrição (CTA inteiro) e "clicking joins: none".

**8. Entrega.** Envie o MP4 e um resumo curto (o que foi usado, duração, o que conferir). Atualize `NOTAS.md`. Vídeos não vão para o git.

## Quando algo dá errado
Consulte `references/licoes-aprendidas.md` antes de improvisar: cada item ali custou uma regeneração real (rosto "embelezado", sobrancelha escura demais ou apagada, brinco de um lado só, fundo com cara de chroma key, voz acelerando de repente, sílaba repetida na emenda, CTA cortado aos 20 s, expressões envelhecidas).

## Arquivos
- `scripts/` — `check_env.py`, `words.py` (transcrição local), `voice_sync.py`, `soften_wrinkles.py`, `overlay_cards.py`, `endcard.py`, `assemble.py`, `qa_check.py`, `brand.py`.
- `references/` — ficha de personagem, prompt de vídeo, geradores e custos, voz, pós-produção, roteiro e ganchos, checklist de QA, lições, ética.
- `examples/` — `PERFIL-modelo.md`, `NOTAS-modelo.md`, `plan.json`, `brand.json`, `scenes/*.json`.
