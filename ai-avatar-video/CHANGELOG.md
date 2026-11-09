# Changelog

## 1.0.2 — 2026-11-09
- `voice_sync.py`: corrige trecho fora de sincronia ("conseguido um emprego" atrasado 0,5 s, "Mas" adiantado 0,7 s).
  Frases também quebram onde a boca pausa mais que a voz; início e fim de frase medidos pelo som (o Whisper erra a
  borda da palavra depois de um silêncio); cada frase é renderizada separada e as pausas viram silêncio real.
- Novo relatório automático: "sync check" compara voz e boca a cada 3 s e aponta o trecho se passar de 0,2 s.

## 1.0.1 — 2026-11-09
- `voice_sync.py`: ritmo natural. Cada frase da voz original tem UMA velocidade constante (0,85–1,15x) e frases vizinhas mudam no máximo 0,10x; as pausas absorvem a diferença. Corrige a voz "lenta e do nada acelera" da 1.0.0 (variação real de até 2x por palavra). O relatório mostra a faixa de velocidades e o maior salto.
- Pausas detectadas pelo volume real da voz (≥ 30 ms a -24 dB), não pelos tempos do Whisper.
- Lições e pós-produção atualizadas com as medições.

## 1.0.0 — 2026-11-09
- Fluxo completo com pontos de aprovação: perfil → ficha de personagem → voz → plano de cenas → geração com custo confirmado → pós → QA.
- `voice_sync.py`: mapa de tempo contínuo (Rubber Band) com início e fim de cada palavra; pausas livres. (substituído na 1.0.1: o ritmo variava demais)
- `words.py`: transcrição local com tempo por palavra (faster-whisper), áudio lido via ffmpeg.
- `soften_wrinkles.py`: suaviza linhas finas só na pele do rosto.
- `assemble.py`: fade de 10 ms em cada emenda; música que nunca encurta a voz.
- `qa_check.py`: folha de contato, transcrição completa e do CTA, checagem das emendas (sem dependência de librosa).
- Cards e card final com cores e fontes configuráveis (`brand.json`) e fonte reserva automática.
- `check_env.py`: diagnóstico do ambiente com o comando de instalação de cada item.
- Referências: ficha de personagem, prompt de vídeo com bloco de expressões jovens, geradores (Artlist, Manus, OpenRouter+Kling), voz ElevenLabs, roteiro e ganchos, checklist de QA, lições aprendidas e ética.
