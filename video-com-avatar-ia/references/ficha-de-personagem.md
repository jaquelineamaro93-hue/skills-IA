# Ficha de personagem e imagem-base (trava de identidade)

Tudo o que o vídeo vai mostrar do rosto nasce aqui. Erro de identidade não se conserta depois: refaz a base.

## Entradas
- 4 a 10 fotos REAIS e recentes: frente, 3/4 dos dois lados, perfil, sorrindo e séria, luz natural, sem filtro.
- 1 vídeo real de 8 a 15 s falando para a câmera (serve para gestos e dicção, não para o visual).
- A roupa e o cenário desejados (foto ou descrição). O cenário vai como referência separada, 9:16.

## Regras (aprendidas a duras penas)
- **Fotos reais acima de imagens geradas.** Nunca use uma imagem gerada como referência de rosto se houver foto real. "A mesma mulher com roupa nova" por texto→imagem muda o rosto.
- **Preserve o que é da pessoa:** formato do rosto, nariz, olhos, boca, mandíbula, assimetrias, textura da pele, sardas. A IA tende a suavizar, afinar e rejuvenescer. Escreva isso no prompt.
- **Pele lisa ≠ rosto novo.** Se a pessoa pedir pele mais lisa ou sem rugas (botox, por exemplo), peça "smooth relaxed forehead, soft under-eyes, keep freckles and skin texture". Não mexa em traços.
- **Detalhes que o modelo erra sempre:** cor da sobrancelha (puxa para castanho escuro; corrigir demais apaga), modelo exato dos óculos (redondo × oval fino), cor da raiz do cabelo, liso × ondulado, piercing (lado), tatuagem.
- **Acessórios assimétricos** (brinco grande de um lado só) saem de um lado só ou somem. Tire da base e escreva "without earrings, both earlobes bare". Pintar na pós fica falso.
- **Corrija na base, uma coisa por vez,** com edição local ("change only the glasses to thin silver oval frames, keep everything else identical"). Não peça para refazer a imagem inteira.

## Prompt da ficha (ajuste os colchetes)
```
Character sheet of the same adult [nacionalidade] [woman/man] in every panel, consistent identity, based ONLY on
the attached real photos. Preserve the exact face shape, eyes, nose, lips, jawline, natural asymmetries, skin
texture and freckles. Do not beautify, slim, rejuvenate or idealize.
[Hair: length, straight/wavy, exact color from roots to ends, part side.]
[Eyebrows: natural light copper / dark blonde ..., visible, never dark brown.]
[Glasses: thin silver oval wire frames ... | no glasses.]
[Piercings, earrings (or "without earrings"), bracelet, watch, tattoo with side.]
[Outfit.]
Neutral light-grey studio backdrop, soft diffused front light, sharp focus, portrait lens.
Layout: front view, three-quarter left, three-quarter right, side profile, close-up face, neutral expression,
warm smile, thoughtful expression, upper body. Label each panel. No other text.
```

## Imagem-base 9:16 (a referência mestre do vídeo)
- A pessoa no enquadramento do vídeo (plano médio, rosto no terço de cima), com a roupa final.
- Cenário NEUTRO ou o próprio cenário final. Se o cenário vier de outra referência, diga no prompt de vídeo "do not use the room from @image1".
- Mostre ficha + base lado a lado com as fotos reais e peça aprovação item a item (lista abaixo).

## Checklist de aprovação
- [ ] Olhos, nariz, boca e mandíbula batem com as fotos reais (compare em close)
- [ ] Sobrancelha: cor e espessura reais
- [ ] Óculos: modelo atual da pessoa (ou sem óculos)
- [ ] Cabelo: cor da raiz às pontas, liso/ondulado, repartição
- [ ] Acessórios iguais dos dois lados (ou removidos)
- [ ] Pele com textura real (lisa só onde a pessoa pediu)
- [ ] Roupa e enquadramento finais
