# Entrevista de cores (antes de montar o cérebro 3D)

Faça em uma mensagem só, com as quatro perguntas. A pessoa pode responder do jeito dela; você transforma em cores.

1. **Que sensação você quer quando abrir o seu cérebro?** (energia, calma, crescimento, calor, elegância)
2. **Fundo claro ou escuro?**
3. **Você já tem cores de marca, site ou logo?** Se tiver, cole o link do site ou os códigos das cores (ex.: #8b5cf6).
4. **Tem alguma cor que você ama ou que não quer ver de jeito nenhum?**

## Como transformar as respostas
| Resposta | Paleta pronta (`references/paletas.json`) |
|---|---|
| Energia, tecnologia, roxo, rosa, neon | `neon` |
| Calma, precisão, azul | `oceano` |
| Crescimento, natureza, verde | `floresta` |
| Calor, criatividade, laranja | `por-do-sol` |
| Elegante, acolhedor, fundo claro, bege | `areia` |

Se a pessoa tiver cores de marca, monte um `cores.json` com os mesmos campos de uma paleta pronta:
- `fundo`, `texto`, `texto_suave`
- `destaque1` (cor principal: linhas e brilho), `destaque2` (pontos de tema), `destaque3` (sinais e item selecionado)
- `pontos` (partículas do cérebro), `cerebelo`
- `claro: true` quando o fundo for claro

Regras rápidas:
- Fundo escuro pede destaques vivos. Fundo claro pede destaques escuros ou médios.
- `destaque3` deve contrastar com os outros dois: é ele que mostra o que está selecionado.
- Se a pessoa disser uma cor que não quer, troque por outra da mesma família de sensação.
- Mostre a escolha em uma frase antes de gerar: "Vou usar roxo, rosa e verde-limão em fundo escuro. Pode ser?"
