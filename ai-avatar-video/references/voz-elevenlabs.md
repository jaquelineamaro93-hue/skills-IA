# Voz clonada (ElevenLabs) e roteiro falado

## Clonagem
- Clone com 1 a 3 minutos de áudio limpo da própria pessoa, sem música, no tom em que ela fala nos vídeos.
- Use sempre as MESMAS configurações (modelo, estabilidade, similaridade) em todos os roteiros. Anote no `NOTAS.md`.

## Escrevendo para a voz (modelo v3)
- **Tags de emoção em inglês** entre colchetes, no início da frase: `[warmly]`, `[thoughtful]`, `[confident]`,
  `[curious]`, `[softly]`, `[excited]`, `[sincere]`, `[matter-of-fact]`, `[pause]`. Não são lidas em voz alta.
- **Reticências (…)** marcam pausas curtas. Frases curtas = cortes de câmera mais naturais.
- **Grafia fonética** para o que a voz erra, e grafia correta só nos cards e legendas:
  - marca/site: "soma mentoria ponto com" (no card: somamentoria.com)
  - siglas: "cê-éle-tê" (CLT), "érre agá" (RH)
  - nomes estrangeiros: escreva como se fala ("Gúpi" para Gupy)
- Gancho nos primeiros 3 s; CTA na última frase, completo, sem nada depois.

## Arquivos
- **Um arquivo por roteiro**, gerado inteiro de uma vez, nome `R01.mp3`, `R02.mp3`…
- Trecho estranho: gere de novo só aquele parágrafo; a emenda é feita na edição (corte em pausa).
- Se os arquivos vierem com nome genérico (data/hora), transcreva os primeiros 7 s de cada um
  (`ffmpeg -t 7` + `words.py`) e mapeie arquivo → roteiro no `NOTAS.md` antes de tudo.

## Sempre
- A voz gerada pelo modelo de VÍDEO é descartada. O áudio final é este arquivo, sincronizado com `voice_sync.py`.
- Transcreva o arquivo final para confirmar que nenhuma palavra foi trocada ou cortada.
