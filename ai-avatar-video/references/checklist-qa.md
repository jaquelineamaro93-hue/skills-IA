# Checklist de QA (antes de entregar cada vídeo)

Rode `python3 scripts/qa_check.py final/R01.mp4 --lang pt` e olhe a folha de contato de verdade, um quadro por vez.

## Imagem
- [ ] É a pessoa (olhos, nariz, boca, mandíbula) em todos os 8 quadros
- [ ] Sobrancelha na cor real; óculos certos; acessórios iguais dos dois lados (ou nenhum)
- [ ] Testa e expressão relaxadas (sem franzir, sem boca em bico) se isso foi pedido
- [ ] Mesmo cenário em todos os planos; sem cara de recorte
- [ ] 5 enquadramentos diferentes; cortes nas pausas
- [ ] Cards legíveis, sem cobrir o rosto, sem erro de português, URL escrita certa
- [ ] Nota "Conversa recriada…" quando o print não é real

## Som
- [ ] Transcrição FULL = roteiro (nenhuma palavra trocada, faltando ou repetida nas emendas)
- [ ] Transcrição END contém o CTA inteiro, até a última palavra
- [ ] `clicking joins: none`
- [ ] Música baixa (voz sempre clara), com fade no fim
- [ ] Voz na boca: assista em velocidade normal pelo menos o começo, uma emenda e o fim

## Arquivo
- [ ] 720×1280, 24 fps, H.264 + AAC, `faststart` (o `assemble.py` já faz)
- [ ] Duração esperada (± 1 s do áudio + card final)
- [ ] `NOTAS.md` atualizado
