# Etapas do funil SDR

O SDR cuida do meio do funil: recebe o lead, filtra, entende a dor e entrega um lead qualificado. O que vem antes
(geração de demanda) e depois (closer, onboarding) não vira etapa; vira contexto no cabeçalho do prompt.

```
Recepção → Triagem → Qualificação → [Coleta de dados] → [Agenda] → Qualificado
              │           │                                  │
              └───────────┴──────────────┬───────────────────┘
                                         ▼
                                  Desqualificado (porta aberta: volta se o lead corrigir a informação)
```

| Etapa | Obrigatória | Tipo | Tamanho típico |
|---|---|---|---|
| Recepção | sim | linear (outbound) ou reativa (inbound com muitos assuntos) | 2 a 5 passos |
| Triagem | sim (pode fundir com a Recepção) | linear | 3 a 8 passos |
| Qualificação | sim | linear | 4 a 8 passos |
| Coleta / confirmação de dados | não | linear | 2 a 4 passos |
| Negociação de agenda | não | linear | 4 a 6 passos |
| Qualificado | sim | terminal simples, ou reativa se o agente continua conversando | 1 a 3 |
| Desqualificado | sim | reativa | 2 a 4 assuntos |

---

## 1. Recepção
**Para quê:** receber o lead depois da primeira mensagem (template de abertura ou mensagem dele).
- Pode cumprimentar e se apresentar em uma frase.
- Na primeira resposta do lead, já faz a **primeira pergunta da Triagem** e muda de etapa no mesmo turno.
  Quem guarda a resposta é a Triagem.
- Prevê saídas imediatas: já é cliente (→ suporte), só quer uma informação (→ responde e retoma), é fornecedor ou
  candidato a vaga (→ canal certo e encerra).
- Inbound com muitos tipos de pedido: use Recepção **reativa** (um assunto por intenção).

## 2. Triagem
**Para quê:** tirar rápido quem não é cliente possível, antes de gastar conversa.
- 1 pergunta por critério eliminatório: porte, faturamento, região atendida, segmento, tipo de pessoa (PF/PJ).
- Pergunta de roteamento quando há produtos diferentes ("Você procura A, B ou C?").
- Cada critério que reprova leva a um motivo de desqualificação próprio.
- Pergunte ao responsável se algum sinal aqui já indica lead muito quente.

## 3. Qualificação
**Para quê:** entender a dor e ligar a dor a uma solução.
Sequência consultiva recomendada (SPIN resumido, uma mensagem por vez):
1. **Situação / problema:** "Me conta um pouco como vocês fazem X hoje?"
2. **Implicação:** reconhece a consequência da dor que o lead citou, com as palavras dele.
3. **Necessidade de solução:** liga a dor a 1 a 3 recursos concretos e propõe o próximo passo (reunião, proposta).
Pode desqualificar se a dor estiver fora do que a empresa resolve.
Depois: vai para Agenda (se o agente marca reunião) ou direto para Qualificado.

## 4. Coleta ou confirmação de dados (opcional)
**Para quê:** completar ou confirmar dados (nome, e-mail corporativo, CNPJ, cargo).
- **Antes da Qualificação** quando o dado decide o corte.
- **Depois** quando é só bom de ter.
- Se o CRM já tem o dado, confirme em vez de perguntar de novo.

## 5. Negociação de agenda (opcional)
Use sempre a mesma estrutura, não reinvente a cada agente:
```
Passo 1  [CONSULTAR AGENDA] do responsável
Passo 2  Filtrar: só dias úteis, faixa de horário aceita, antecedência mínima
Passo 3  Sugerir de 2 a 4 horários numa mensagem
Passo 4  Validar a escolha:
           data no passado      → avisa e volta ao Passo 3
           fim de semana        → avisa e volta ao Passo 3
           horário indisponível → avisa e volta ao Passo 3
           válido               → Passo 5
Passo 5  Confirmar e-mail para o convite
Passo 6  [CRIAR EVENTO] + mensagem de confirmação + [MUDAR ETAPA → Qualificado]
```
Limite de voltas (ex.: 3). Estourou: oferece link de agenda ou transfere para humano.

## 6. Qualificado
**Para quê:** resultado de sucesso.
- Sub-tipos para relatório: `Qualificado`, `Qualificado - Reunião agendada`, `Qualificado - Lead quente`.
- Sem follow-up automático nesta etapa.
- Defina com o responsável: o agente para de falar (passa para humano) ou continua respondendo? Se continua,
  sobre quais assuntos? Nesse caso a etapa é reativa.

## 7. Desqualificado
**Para quê:** resultado de descarte, com porta aberta.
- Um motivo por critério que reprovou: `Desqualificado - Fora do ICP`, `- Região não atendida`,
  `- Orçamento insuficiente`, `- Sem interesse`, etc.
- Sempre reativa, com estes assuntos:
  1. **Lead trouxe informação nova** que muda o corte → agradece, atualiza o campo e volta para a etapa de origem.
  2. **Lead tem dúvida** → responde pela base de conhecimento e mantém desqualificado.
  3. **Mensagem neutra** (ok, obrigado) → resposta curta e cordial, mantém.
- Mensagem de desqualificação educada, sem culpa, indicando alternativa quando existir.

---

## Regras que atravessam o funil
- **Lead muito quente / transbordo:** pergunte sempre se existe. Pode surgir na Triagem (sinal claro de fit),
  na Coleta (perfil VIP) ou na Qualificação (pedido explícito de compra). Vai direto para Qualificado ou humano.
- **Pedido de humano** em qualquer etapa: mensagem + `[TRANSFERIR PARA HUMANO]`.
- **Desvio de assunto:** responde em 2 a 3 frases e retoma a pergunta pendente.
- **Contexto antes/depois do SDR:** 1 parágrafo cada, no cabeçalho do prompt (não vira passo).
