# Lições aprendidas (projeto real, avatar de mentora, PT-BR)

Cada linha é um erro que custou uma regeneração ou uma reclamação. Leia antes da primeira geração.

## Identidade
- Ficha gerada a partir de imagem gerada → rosto "idealizado" (olhos, nariz, contorno e sorriso mudaram). Use só fotos reais e escreva "preserve asymmetries, do not beautify".
- "Mesma mulher, roupa nova" por texto→imagem mudou o rosto duas vezes. Só fotos reais + edição local.
- Sobrancelha: a real era clara/acobreada; o modelo escureceu ("não é tão escura assim"). Corrigindo demais, sumiu. Prompt: "natural light copper, visible, never dark brown and never erased". Confira em close.
- Óculos: use o modelo ATUAL da pessoa (ela corrigiu redondo → oval fino).
- Cabelo: liso × ondulado e cor da raiz fazem diferença para quem conhece a pessoa.
- Brinco grande de um lado só saiu só de um lado; pintar o outro na pós ficou "pintado". Tirar da base + "without earrings" resolveu.
- Expressões "de velha" (testa franzida, boca em bico, olhos semicerrados) vinham das tags [frustrated]/[sighs]/[thoughtful]. Trocar a expressão por tag (ver `prompt-video.md`) + bloco EXPRESSIONS no prompt.
- Pessoa que faz botox quer testa lisa: pedir no prompt e, se precisar, `soften_wrinkles.py` 0,8 — sem mexer em traços.

## Cenário
- Fundo trocado por recorte e colagem → "parece chroma key". Dê o cenário como referência própria 9:16 e peça luz natural consistente.
- Pedido de "um cenário" e entrega em 2 gerações confundiu ("só pedi um cenário"). Avise antes que é um vídeo só, dividido pelo limite de duração.

## Voz e sincronia
- A fala gerada pelo modelo de vídeo inventa palavras ("sabote", "candilita", "minida andando"). Sempre trocar pela voz original.
- Alinhamento global (DTW) derrapou ~0,5 s e criou acelerações bruscas ("velocidade 10x").
- Esticar a voz em pedaços por palavra (atempo) gerou cliques e ruídos.
- O vídeo gerado faz pausas mais longas que a voz original; forçar a fala a cobrir a pausa deixou a voz 0,15 s fora da boca. Solução (`voice_sync.py`): mapa contínuo do Rubber Band com início e fim de cada palavra; pausas livres, palavras com limite de velocidade → 0,06 s.
- O fim de um trecho precisa parar antes da próxima palavra do áudio completo, senão uma sílaba vaza e repete na emenda ("É super"/"Se... Se você").
- Um início negativo em t=0 apagou a primeira frase sem aviso. Nunca deixe o início abaixo de 0.

## Mixagem e CTA
- A mixagem com `amix` padrão cortou o áudio em ~20,5 s e o "Comenta MIGRAR" sumiu. Use `duration=first:normalize=0` (já no `assemble.py`) e confira o fim da transcrição em todo vídeo.
- Se o CTA não cabe na geração, card final com a voz original (`endcard.py`) em vez de cortar.

## Formato e comunicação
- A pessoa queria aparecer mais: cards na parte de baixo, sobre o próprio vídeo, e não telas de celular em tela cheia.
- Prints de conversa: sem autorização, recriar e marcar "Conversa recriada · nome preservado"; com autorização, desfocar foto e sobrenome mesmo assim.
- Mantenha `NOTAS.md`: bases aprovadas, mapa áudio→roteiro, o que foi aprovado e rejeitado. Evita repetir erro de uma sessão para outra.
- Ao responder pedidos de correção, confirme o que entendeu em uma linha e mostre a prova (close, frame, transcrição do fim).
