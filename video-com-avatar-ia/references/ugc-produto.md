# UGC de produto (avatar segurando e indicando um produto)

Use quando o vídeo divulga um produto físico (suplemento, cosmético, livro, gadget) ou uma loja/cupom.

## Antes de gerar — confira e pergunte se faltar
- [ ] **Foto REAL do produto**, de frente, rótulo legível (foto de celular ou imagem da loja). Fichas de personagem
      geradas por IA deformam rótulos ("Whoy Tasty", "BONGISSIMO"): nunca use o pote da ficha como referência do produto.
- [ ] **Nome do produto na voz**: transcreva o áudio (`words.py`) e confira o nome da marca. Marca estrangeira sai
      errada ("Gods Whey Tasty" → "God's Weigh Taste 3W"). Corrija na ElevenLabs com grafia fonética
      ("Gódis Uêi Têisti") ANTES de gerar o vídeo. O card e a legenda usam a grafia correta.
- [ ] **Cupom/link é da pessoa do vídeo** (ou combinado com a marca). Cupom de outra criadora com o rosto e a voz
      desta pessoa é erro — pergunte.
- [ ] **Relação com a marca**: pago ou produto recebido = publicidade (ver "Aviso" abaixo).
- [ ] **Afirmações**: só o que o rótulo/marca comprova. Nada de promessa de resultado, saúde ou emagrecimento.

## Prompt — acrescente ao `prompt-video.md`
Referências extras: `@image5` = foto real do produto (frente).
```
She holds the product from @image5 in every product shot: same container shape, colors and label layout as @image5,
label facing the camera, held still and upright at chest height so the label stays readable; her fingers never cover
the brand name. Do not invent or change any text on the package. The product is the same size in every shot.
```
Planos que funcionam (um por frase):
1. Gancho: produto na mão, perto do rosto, olhar para a câmera.
2. Aponta para o rótulo / sabor.
3. Detalhe de uso (colher, textura, abrir a tampa) — plano mais fechado.
4. Como usar / para quem é: gesto de explicação, produto apoiado.
5. CTA: celular na outra mão ou aponta para baixo (onde vai o card do cupom), sorriso.

## Pós
- Card do CTA com loja + cupom em letras grandes (`overlay_cards.py` tipo `quote`: linha 1 "Compre na <loja>",
  linha 2 dourada com o CUPOM). Escreva o cupom exatamente como a loja aceita (maiúsculas, números).
- Se o rótulo saiu deformado em algum plano, corte esse plano ou regere: não publique rótulo errado de marca real.

- Quando o rótulo deforma só em alguns segundos, posicione o card do CTA por cima do pote nesse trecho (testado:
  o card do cupom cobriu a tampa deformada no último segundo).
- Imagens coladas no chat nem sempre viram arquivo: peça o anexo pelo clipe ou o painel de upload do gerador.

## Aviso (obrigatório)
- Pago ou produto recebido: selo "Parceria paga"/"Conteúdo pago" ligado na rede + `#publi` no início da legenda.
- Avatar/voz de IA realistas: ligue o rótulo de IA da rede (Instagram/TikTok/YouTube) e, se for anúncio, siga a
  regra de conteúdo sintético da plataforma.
- Modelo de legenda: `#publi Avatar criado com IA a partir da minha imagem e voz. <texto>. Cupom <CUPOM> na <loja>.`
