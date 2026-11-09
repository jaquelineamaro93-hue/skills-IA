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
- Grudar a voz palavra por palavra na boca (velocidade livre até 2x) deu ótima sincronia no papel (0,06 s) e ficou HORRÍVEL de ouvir: "bem lento e do nada acelera". Medido: 0,49x a 1,48x dentro das frases. Regra: uma velocidade constante por frase (0,85–1,15x), mudança máxima de 0,10x entre frases, pausas absorvem o resto. Ritmo natural vale mais que 0,05 s de sincronia.
- "0:19 'conseguido um emprego' sai de sintonia": duas causas, ambas corrigidas no `voice_sync.py`:
  (1) o vídeo gerado fez uma pausa de 1,5 s onde a voz original só respira; tratado como uma frase só, o erro se espalhou (+0,5 s antes, -0,44 s depois). Regra: quebrar a frase também onde a BOCA pausa mais que a voz.
  (2) o Whisper marcou o início de "Mas" 0,27 s antes do som real, e a pausa esticada "espalhou" o começo da palavra no silêncio. Regra: início/fim de frase pelo som (volume), e pausas são silêncio de verdade, nunca áudio esticado.
  Confirme sempre com o relatório "sync check … OK, all within 0.2 s" e assistindo o trecho apontado.
- "Travadinha" em 0:09 e 0:20: o corte entre frases caiu DENTRO de "cliente" e "contratação" (o Whisper marcou o fim dessas palavras cedo demais) e os dois pedaços ficaram separados por 0,07–0,18 s. Regra: só cortar em silêncio real (≥ 80 ms abaixo de -30 dB) ou, onde a boca pausa e a voz só respira, no meio da respiração. Sem isso, as frases ficam juntas.
- Tempos de palavra do Whisper erram até 0,4 s (ex.: "Mas" marcado 0,34 s antes do som). Use-os só para casar palavras; bordas de frase e cortes vêm do volume do áudio.
- Velocidade constante por frase longa deixou a voz derivar 0,3–0,5 s no fim da frase. Dentro da frase a velocidade acompanha a boca, mas mudando no máximo 0,20x de uma palavra para a seguinte (0,78–1,28x): gradual não se percebe.
- Em 0:29 os cards sumiam com transparência nos últimos 0,3 s e "vazavam" o fundo. Regra: cards ficam inteiros até o corte; o card final nasce do ÚLTIMO quadro do clipe, desfocando.
- 0:09 "sobrepôs": uma frase começava 0,18 s antes de a anterior terminar (o fim de "e como" por cima de "valorizar"). Regra: uma frase nunca começa antes de a anterior acabar; o relatório lista "overlapping phrases" e tem que dar "none".
- "Se você notar, eu ajusto" não é aceitável: o ajuste fino é automático. O `voice_sync.py` mede cada frase contra a boca (primeira e segunda metade), corrige início/fim e renderiza de novo até 4 rodadas. Resultado no teste: pior trecho 0,21 s → 0,09 s.
- Métrica de velocidade por re-transcrição engana: numa cópia SEM alteração ela já mostra 0,80x–1,85x. Confie no relatório do `voice_sync.py` (velocidade exata do mapa) e no ouvido, não nessa medida.
- Detector de "cliques" por salto de amostra acusa os "s" e "p" da própria voz original. A garantia é por construção (fade de 10 ms em cada emenda) e a checagem é só nas emendas.
- O fim de um trecho precisa parar antes da próxima palavra do áudio completo, senão uma sílaba vaza e repete na emenda ("É super"/"Se... Se você"). Travado no `voice_sync.py` desde a 1.1.0 (o teste com dois trechos pegou o trecho 1 invadindo o 2 em 0,27 s).
- Um início negativo em t=0 apagou a primeira frase sem aviso. Nunca deixe o início abaixo de 0.

## Mixagem e CTA
- A mixagem com `amix` padrão cortou o áudio em ~20,5 s e o "Comenta MIGRAR" sumiu. Use `duration=first:normalize=0` (já no `assemble.py`) e confira o fim da transcrição em todo vídeo.
- Se o CTA não cabe na geração, card final com a voz original (`endcard.py`) em vez de cortar.

## Formato e comunicação
- A pessoa queria aparecer mais: cards na parte de baixo, sobre o próprio vídeo, e não telas de celular em tela cheia.
- Prints de conversa: sem autorização, recriar e marcar "Conversa recriada · nome preservado"; com autorização, desfocar foto e sobrenome mesmo assim.
- Mantenha `NOTAS.md`: bases aprovadas, mapa áudio→roteiro, o que foi aprovado e rejeitado. Evita repetir erro de uma sessão para outra.
- Ao responder pedidos de correção, confirme o que entendeu em uma linha e mostre a prova (close, frame, transcrição do fim).
