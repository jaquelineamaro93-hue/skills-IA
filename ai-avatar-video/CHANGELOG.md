# Changelog

## 1.0.0 — 2026-11-09
- Fluxo completo com pontos de aprovação: perfil → ficha de personagem → voz → plano de cenas → geração com custo confirmado → pós → QA.
- `voice_sync.py`: mapa de tempo contínuo (Rubber Band) com início e fim de cada palavra; pausas livres. Medido num vídeo real de 30 s: 0,06 s de diferença média entre voz e boca, 90% abaixo de 0,1 s, sem cliques.
- `words.py`: transcrição local com tempo por palavra (faster-whisper), áudio lido via ffmpeg.
- `soften_wrinkles.py`: suaviza linhas finas só na pele do rosto.
- `assemble.py`: fade de 10 ms em cada emenda; música que nunca encurta a voz.
- `qa_check.py`: folha de contato, transcrição completa e do CTA, checagem das emendas (sem dependência de librosa).
- Cards e card final com cores e fontes configuráveis (`brand.json`) e fonte reserva automática.
- `check_env.py`: diagnóstico do ambiente com o comando de instalação de cada item.
- Referências: ficha de personagem, prompt de vídeo com bloco de expressões jovens, geradores (Artlist, Manus, OpenRouter+Kling), voz ElevenLabs, roteiro e ganchos, checklist de QA, lições aprendidas e ética.
