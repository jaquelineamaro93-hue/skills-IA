# Pós-produção, passo a passo

Pasta de trabalho sugerida: `projeto/` com `out/` (clipes), `scenes/` (cards), `final/`, `PERFIL.md`, `NOTAS.md`,
`R01.mp3`… e `music.wav`. Rode os scripts a partir de `projeto/`.

## 1. Sincronizar a voz original — `voice_sync.py`
```bash
python3 scripts/voice_sync.py out/A.mp4 R01.mp3 out/A_fit.wav --ranges 0-28.4
python3 scripts/voice_sync.py out/B.mp4 R01.mp3 out/B_fit.wav --ranges 28.4-55.0
```
- `--ranges`: trechos do ÁUDIO ORIGINAL (segundos) que aquele clipe fala, em ordem. Vários trechos num clipe:
  `--ranges 0-12.5,30.2-41.0` (cada um vira o range 0, 1… do `plan.json`).
- Saída: `A_fit.wav` (exatamente a duração do vídeo) + `A_fit.wav.cuts.json`.
- Como funciona: transcreve os dois áudios, casa as palavras, divide a voz original em frases nas pausas reais
  (≥ 30 ms de silêncio) e onde a boca pausa mais que a voz; cada frase tem UMA velocidade constante entre 0,85x e
  1,15x (vizinhas mudam no máximo 0,10x), é cortada no ponto mais silencioso e começa junto com a boca (início medido
  pelo som, não pela transcrição). As pausas são silêncio de verdade. Fade de 10 ms em cada frase (sem cliques).
- Leia as duas linhas do relatório: `phrase speeds 0.85x-1.15x, biggest jump 0.10x` e
  `sync check … OK, all within 0.2 s`. Se o sync check disser "LOOK AT 15-18s +430 ms", assista esse trecho:
  quase sempre é `--ranges` errado ou uma palavra que o gerador inventou/pulou ali.
- Medido num vídeo real de 30 s: todos os trechos a menos de 0,2 s da boca, ritmo natural, texto intacto.
- NÃO aumente `--rate` ou `--jump` para "grudar" mais na boca: a voz passa a ficar lenta e acelerar do nada
  (testado e reprovado num projeto real). Boca melhor se resolve na geração, não esticando a voz.
- Ajustes: `--lead 0.04` (voz levemente antes da boca soa natural; 0,02–0,08).
- Se aparecer "only N words matched": arquivo de voz errado, `--ranges` errado ou idioma errado (`--lang`).

## 2. Pele (opcional, só se a pessoa pedir) — `soften_wrinkles.py`
```bash
python3 scripts/soften_wrinkles.py out/A.mp4 out/A_soft.mp4 0.8 --preview 12 prev.png   # confira antes
python3 scripts/soften_wrinkles.py out/A.mp4 out/A_soft.mp4 0.8
```
Suaviza só detalhes fracos da pele (testa, olheira, bigode chinês) dentro do rosto; olhos, sobrancelhas, boca,
cabelo e fundo ficam iguais. 0,6 = leve, 0,8 = padrão, 0,9 = forte. Rode ANTES dos cards. ~7 min por 30 s.
Expressão (testa franzida, boca em bico) não se corrige aqui: corrija no prompt.

## 3. Cards — `overlay_cards.py` (aplicado pelo `assemble.py`)
Tipos em `examples/scenes/`: `chat` (print de conversa recriado, bolhas entrando e digitação ao vivo), `steps`
(passos numerados), `quote` (frase de impacto). `t` = segundos desde o início da cena.
Prévia num frame: `python3 scripts/overlay_cards.py scenes/chat.json frame.png 6 prev.png`.
Cores e fontes: `brand.json` (na pasta do projeto, ou `AVATAR_BRAND=/caminho/brand.json`).
Conversas reais só com autorização; sem ela, recrie o texto e use a nota "Conversa recriada · nome preservado".

## 4. Card final — `endcard.py`
Para o CTA que não coube na geração: fundo desfocado do próprio cenário + voz original + linhas aparecendo.
```bash
ffmpeg -ss 27 -i out/B.mp4 -frames:v 1 frame.png
python3 scripts/endcard.py frame.png R01.mp3 54.4 63.4 out/endcard.mp4 "Conheça a marca|marca.com|Link na bio" "PRÓXIMO PASSO"
```
A 2ª linha sai na cor de destaque (use para a URL, escrita corretamente).

## 5. Montagem — `assemble.py plan.json`
Ver `examples/plan.json`. Cada item da timeline é `{clip, range}` (trecho cuts[j]..cuts[j+1] do clipe, com a voz
sincronizada), opcionalmente com `overlay` + `scene_voice_start` (segundo do ÁUDIO ORIGINAL em que a cena começa,
assim o card acompanha a fala), ou `{file}` (peça pronta, como o card final). Cada emenda leva fade de 10 ms (sem
estalos) e a música entra a 0,10–0,12 com fade, sem nunca encurtar a voz.

## 6. QA — `qa_check.py final/R01.mp4 --lang pt`
Gera a folha de contato `final/R01_qa.jpg`, a transcrição inteira, a dos últimos 8 s (CTA) e a checagem das
emendas. Siga `checklist-qa.md`.
