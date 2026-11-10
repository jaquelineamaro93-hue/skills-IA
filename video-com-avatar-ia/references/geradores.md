# Onde gerar e quanto custa

Os geradores mudam de nome, preço e limite com frequência. **Sempre confira no momento** (lista de modelos, saldo
e custo) e diga à pessoa o valor antes de gerar. Nunca estime custo "de cabeça".

## O que o gerador precisa aceitar
- Imagem(ns) de referência + **áudio de referência** (a boca segue a voz) + idealmente um vídeo de referência.
- Saída 9:16, 720p ou mais. Duração por geração cobrindo um bloco do roteiro.

## Opções testadas
| Caminho | Como usar | Observações |
|---|---|---|
| **Artlist (conector MCP `https://mcp.artlist.io/mcp`)** | Conecte em Claude → Configurações → Conectores → conector personalizado. Use a família **Seedance 2.5 R2V** (imagem + áudio [+ vídeo]). | Mostra custo e pede confirmação antes de gerar. O teste grátis NÃO inclui Seedance 2.5; o grátis (Seedance 2.0 Mini) limita a **15 s**. O Seedance 2.5 tem modo rascunho 480p barato que depois renderiza em 1080p a mesma tomada. |
| **Manus (Video Editor)** | Fluxo "talking head" ou "multi-ângulo": mande o vídeo real em 1 ângulo + fotos do cenário + o áudio. | Bom para quem não quer configurar nada. Use os prompts daqui. Confira o MP4 antes de pedir de novo (aviso de cobrança pode aparecer mesmo com o arquivo gerado). |
| **OpenRouter + Kling 3** (ou outro R2V via API) | Chave de API do provedor; mesmo prompt. | Pague por uso; confira o limite de duração do modelo. |

## UGC de uma foto + áudio inteiro (testado)
- **OmniHuman 1.5** (no Artlist; disponível nas gerações grátis): 1 imagem 9:16 + o áudio INTEIRO (26 s testados) +
  prompt de gestos → a pessoa falando o roteiro todo numa geração. A voz do vídeo é o próprio arquivo enviado
  (correlação 0,9999): **não precisa de `voice_sync.py`**. Bom para UGC de produto em plano único (selfie/estúdio);
  não faz 5 ângulos. **HeyGen Avatar 4** é a alternativa do mesmo tipo.
- Monte a imagem 9:16 a partir da ficha (recorte + parede estendida, sem emenda visível) e confira antes de enviar.
- Em conta de teste, alguns modelos listados como grátis podem vir bloqueados ("não incluso no plano"): tente o
  próximo grátis antes de pedir assinatura.
- Arquivos gerados vêm de `cms-toolkit-artifacts.artlist.io`: libere esse host na rede para baixar e finalizar.

## Dividir o roteiro pelo limite
- Seedance 2.5: até ~30 s por geração. Seedance 2.0 Mini: 15 s. Confira o do modelo escolhido.
- Corte o áudio em pausas reais (`words.py`), mantendo cada bloco ≤ limite − 1 s.
- Mesmo cenário, roupa e referências em todos os blocos. Na montagem, `assemble.py` intercala os blocos.
- Avise antes: "é um vídeo final só; ele é gerado em 2 partes por causa do limite de 30 s".
- Se só o CTA final não couber, use `endcard.py` (card em tela cheia com a voz original) em vez de outra geração.

## Duração e custo
- Duração pedida = duração do bloco de áudio arredondada para cima (o custo sobe com a duração).
- Faça 1 bloco de teste, aprove expressão e identidade, depois o lote.
- Guarde no `NOTAS.md`: modelo, duração, custo e o que foi aprovado em cada geração.
