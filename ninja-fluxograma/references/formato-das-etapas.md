# Formato das etapas

Cada etapa vira um bloco de texto que o agente lê para saber o que fazer. Dois formatos: **linear** e **reativo**.

| | Linear | Reativo |
|---|---|---|
| Fluxo | Passo 1 → 2 → 3 | Qualquer assunto pode ser ativado a qualquer momento |
| Quando usar | Triagem, Qualificação, Agenda, Coleta | Recepção inbound, Desqualificado, Qualificado que continua conversando, Suporte |
| Estrutura | `Passo N` com Regras / Objetivo / Fallback | `Assunto N) Nome` + `Ativa quando:` + passos internos no mesmo padrão |

---

## 1. Formato linear

```markdown
[1 a 3 frases: objetivo da etapa e o que já se sabe do lead ao chegar aqui]

### Regras gerais
- [ATUALIZAR CAMPO etapa_atual = "Triagem"] ao iniciar esta etapa.
- Faça 1 pergunta por mensagem.
- Se o lead já respondeu algo numa mensagem anterior, não pergunte de novo: registre e siga.
- Transição: ao sair para a [Próxima etapa], envie a pergunta inicial dela no mesmo turno.

### Passos

#### Passo 1: "Perguntar o porte da empresa"
Regras:
- Executar uma única vez.
Objetivo:
- Envie o template "triagem_porte".
- [ATUALIZAR CAMPO num_colaboradores] com a resposta.
- Se a resposta for menor que 20, vá para o Passo 1.1.
- Se for 20 ou mais, vá para o Passo 2.
Fallback:
- Se a resposta não for clara, diga que não entendeu e repita a pergunta pendente com um exemplo de resposta.

#### Passo 1.1: "Desqualificar por porte"
Regras:
- Executar apenas se o Passo 1 indicar menos de 20 colaboradores.
Objetivo:
- Envie o template "desq_porte".
- [ATUALIZAR CAMPO motivo_desqualificacao = "porte"].
- [MUDAR ETAPA → Desqualificado].
Fallback:
- Se a resposta não for clara, diga que não entendeu e repita a pergunta pendente.

### Templates
#### Template: "triagem_porte"
Mensagem: "Pra eu te direcionar certo, quantas pessoas trabalham na empresa hoje?"

#### Template: "desq_porte"
Mensagem: "Obrigada por contar. Hoje a nossa solução atende empresas a partir de 20 pessoas, então não consigo seguir por aqui agora. Se esse número mudar, é só me chamar."
```

### Regras do formato linear
- Todo passo tem **Regras**, **Objetivo** e **Fallback**. Fallback vazio não existe: use o padrão
  "Se a resposta não for clara, diga que não entendeu e repita a pergunta pendente".
- **Sub-passos** (`1.1`, `1.2`) para ramificações dentro de um passo: cada um é uma condição com a sua ação.
- **Laços** sempre com limite: "No máximo 3 voltas entre o Passo 3 e o Passo 4. Depois, siga para o Passo 5."
- Templates com nome em `snake_case`; o texto fica na seção Templates, o passo só chama o nome.

## 2. Formato reativo

```markdown
Reaja ao que o lead trouxer, considerando a mensagem atual e as anteriores. Execute uma destas ações, em qualquer ordem:
1. AtualizarInformacao: o lead corrigiu um dado que causou a desqualificação
2. ResponderDuvida: o lead fez uma pergunta
3. MensagemNeutra: agradecimento, "ok", despedida

Não existe ordem fixa. Antes de agir, consulte motivo_desqualificacao e compare com a mensagem atual.

### Princípios
- [ATUALIZAR CAMPO etapa_atual = "Desqualificado"] ao iniciar esta etapa.
- Seja cordial e breve. Não insista na venda.

### 1) AtualizarInformacao
Ativa quando: o lead informa um dado novo que muda o critério do motivo registrado.
Sinais: "na verdade somos 40", "me enganei", "abrimos uma filial em SP".

#### Passo 1: "Reabrir o lead"
Regras:
- Executar só se o dado novo atender ao critério que reprovou.
Objetivo:
- [ATUALIZAR CAMPO] correspondente com o novo valor.
- Envie: "Obrigada pela correção, então dá pra seguir sim."
- [MUDAR ETAPA → etapa de origem do motivo].
Fallback:
- Se a resposta não for clara, pergunte qual é o dado correto.
```

## 3. Ações genéricas
Escreva com estas ações. No fim do entregável, mostre a tabela de troca para a plataforma da pessoa.

| Ação | O que faz | Regra |
|---|---|---|
| `[ATUALIZAR CAMPO x = y]` | Grava um dado do lead | 1 campo por linha |
| `[MUDAR ETAPA → X]` | Passa a conversa para outra etapa | Mensagem antes, sempre |
| `[TRANSFERIR PARA HUMANO]` | Passa para uma pessoa do time | Mensagem antes, sempre |
| `[ENCERRAR CONVERSA]` | Fecha o atendimento | Despedida antes, sempre |
| `[CONSULTAR AGENDA]` | Busca horários livres | Só na etapa de Agenda |
| `[CRIAR EVENTO]` | Marca a reunião e envia o convite | Depois de confirmar e-mail |
| `[CONSULTAR BASE: tema]` | Busca resposta numa base ou FAQ específica | Ver roteamento de dúvidas |
| `[CHAMAR INTEGRAÇÃO: nome]` | CRM, consulta de CNPJ, webhook | Diga o que fazer se falhar |

**Mensagem antes da transição:** mudar de etapa, transferir ou encerrar sem avisar deixa o lead sem resposta.
Sempre: `Envie: "..."` na linha anterior à ação.

## 4. Roteamento de dúvidas
Quando há muitas dúvidas possíveis, separe por tema dentro de um passo:
```
#### Passo 1: "Responder dúvida"
Objetivo:
- [ATUALIZAR CAMPO intencao = "duvida"].
- 1.1 Se a dúvida for sobre preço ou planos → [CONSULTAR BASE: planos].
- 1.2 Se for sobre integrações com outros sistemas → [CONSULTAR BASE: integracoes].
- 1.3 Se for comparação com concorrentes → [CONSULTAR BASE: concorrentes].
- Outro tema → [CONSULTAR BASE: faq_geral].
- Responda em 2 a 4 frases e retome a pergunta pendente.
```
Condições específicas funcionam melhor: "comparação com concorrentes ou outras ferramentas do mercado" é melhor que
"comparação".

## 5. Anti-padrões (corrija sempre)
- ❌ Passo que diz "pergunte X, se negativo desqualifique com a mensagem Y e atualize Z": são 4 ações escondidas.
  Quebre em passo + sub-passo, uma ação por linha.
- ❌ Template de desqualificação escrito dentro da regra em vez da seção Templates.
- ❌ Duas perguntas na mesma mensagem.
- ❌ Laço sem limite.
- ❌ Etapa terminal sem `[ATUALIZAR CAMPO subtipo_resultado]`.
- ❌ Informação de produto ou empresa repetida dentro das etapas (fica no prompt, na base de conhecimento).
- ❌ O agente contar ao lead que "atualizou um campo" ou "mudou de etapa".
