# Padrões de Rejeição — Templates Utility WhatsApp

Use este arquivo para diagnosticar por que um template foi rejeitado ou para prevenir rejeições antes da submissão.

---

## Motivos de Rejeição por Frequência

| Rank | Motivo | Frequência | Solução |
|------|--------|-----------|---------|
| 1 | Conteúdo promocional em Utility | 22% | Remover toda linguagem de marketing |
| 2 | Variáveis malformadas | 20% | Usar formato {{1}}, {{2}} exato |
| 3 | Palavras-chave de spam/urgência | 15% | Substituir por linguagem neutra |
| 4 | URL inválida ou encurtada | 12% | Usar URL completa https:// |
| 5 | Categoria incorreta (Marketing submetido como Utility) | 10% | Reescrever sem promoção |
| 6 | Sample values genéricos | 9% | Usar valores realistas |
| 7 | Nomes duplicados ou genéricos | 7% | Usar naming convention descritivo |
| 8 | Erros de digitação ou gramática | 5% | Revisão editorial antes de submeter |

---

## NÍVEL 1 — Rejeição Automática Garantida

Qualquer template que contenha essas palavras/padrões em qualquer componente (incluindo footer):

### Palavras Promocionais Diretas
```
OFERTA LIMITADA
COMPRE AGORA
GANHE DESCONTO
SALE / % OFF
ÚLTIMAS UNIDADES
APROVEITE ENQUANTO DURA
OFERTA TERMINA HOJE / AMANHÃ
NÃO PERCA ESSA CHANCE
CLIQUE AQUI AGORA
PROMOÇÃO ESPECIAL
BLACK FRIDAY
LIQUIDAÇÃO
CUPOM DE DESCONTO
CÓDIGO PROMOCIONAL
```

### Padrões de Urgência Artificial
```
URGENTE!
RÁPIDO!
ACT NOW / AGORA
HOJE APENAS
LIMITED TIME
ATENÇÃO!!!
NÃO PERCA!
ÚLTIMA OPORTUNIDADE
EXPIRA EM [tempo]
```

### Solicitações de Dados Sensíveis (violação de segurança)
```
Número do cartão de crédito
CPF / CNPJ (solicitar, não informar)
Senha
CVV / código de segurança
Dados bancários por mensagem
```

### URLs Proibidas
```
bit.ly/*
tinyurl.com/*
goo.gl/*
wa.me/*
Qualquer encurtador de URL
URLs sem https://
```

---

## NÍVEL 2 — Alerta (Rejeição provável se combinado)

Essas palavras sozinhas não causam rejeição automática, mas em combinação com outras ou em contexto comercial, causam:

```
"Aproveite"          → OK em contexto neutro, REJEITADO antes de link de loja
"Especial"           → OK "atendimento especial", REJEITADO "oferta especial"
"Promoção"           → Quase sempre Marketing, evite
"Novo"               → OK "novo status do pedido", REJEITADO "nova coleção chegou"
"Exclusivo"          → OK "acesso exclusivo ao seu pedido", REJEITADO em maioria dos contextos
"Economize"          → Quase sempre Marketing
"Oportunidade"       → Quase sempre Marketing
"Hoje"               → OK "entrega hoje", REJEITADO "oferta válida hoje"
"Esta semana"        → Contexto importa muito
"Disponível agora"   → OK para status, REJEITADO para promoção
```

---

## NÍVEL 3 — Atenção (Contexto decide)

```
"Parabéns"           → OK em confirmação (inscrito, pedido), EVITE em outros contextos
"Incrível"           → Evite sempre
"Ótimo"              → OK como saudação, EVITE em corpo principal
"Frete grátis"       → Sempre Marketing
"Desconto"           → Sempre Marketing (mesmo "sem desconto")
```

---

## Templates REPROVADOS — Análise Detalhada

### Reprovado 1 — Marketing Disfarçado de Utility
```
NOME SUBMETIDO: util_order_status_v1
CATEGORIA SUBMETIDA: UTILITY

BODY (rejeitado):
"Seu pedido foi enviado! 🎉

E aproveite: {{1}}% OFF em sua próxima compra!
Use código: {{2}}

Compre agora: [link loja]"

❌ REJEITADO: "Category mismatch — promotional content detected"

ANÁLISE:
- Linha 1: Legitima Utility (pedido enviado)
- Linha 2-4: 100% Marketing (desconto + "compre agora")
- A Meta detectou o padrão: "status + upsell" = Marketing
- Resubmissão como Utility será rejeitada novamente

CORREÇÃO:
Fazer DOIS templates separados:
1. Utility: "Seu pedido foi enviado. Rastreio: {{1}}"
2. Marketing: "Aproveite {{1}}% OFF em sua próxima compra. Código: {{2}}"
```

### Reprovado 2 — Variáveis Malformadas
```
NOME SUBMETIDO: util_payment_confirm_v1
CATEGORIA SUBMETIDA: UTILITY

BODY (rejeitado):
"Oi [name],
Seu pagamento de [amount] foi recebido.
ID: [transaction_id]"

❌ REJEITADO: "Template format error — invalid variable format"

ANÁLISE:
- Sistema não reconhece [name], [amount] como variáveis dinâmicas
- Formato esperado: {{1}}, {{2}}, {{3}}
- Rejeição técnica automática, sem revisão humana

CORREÇÃO:
"Oi {{1}},
Seu pagamento de {{2}} foi recebido.
ID: {{3}}"
```

### Reprovado 3 — Urgência Artificial
```
NOME SUBMETIDO: util_appointment_remind_v1
CATEGORIA SUBMETIDA: UTILITY

BODY (rejeitado):
"ATENÇÃO {{1}}!!!
Sua consulta VENCE AMANHÃ às {{2}}!
RÁPIDO — NÃO PERCA!
Confirme AGORA ou será cancelada."

❌ REJEITADO: "Spam pattern detected — excessive urgency language"

ANÁLISE:
- ATENÇÃO + !!! = red flag imediato
- VENCE + RÁPIDO + NÃO PERCA + AGORA = múltiplos gatilhos de spam
- MAIÚSCULAS em excesso = padrão de spam
- "será cancelada" = pressão artificial
- Todos esses elementos juntos = rejeição certa

CORREÇÃO:
"Olá {{1}},

Lembrete: sua consulta é amanhã às {{2}}.

Clique abaixo para confirmar presença."

[Buttons: CONFIRMAR (QR) | REMARCAR (QR)]
```

### Reprovado 4 — Dados Sensíveis Solicitados
```
NOME SUBMETIDO: util_payment_verify_v1
CATEGORIA SUBMETIDA: UTILITY

BODY (rejeitado):
"{{1}}, para confirmar seu pagamento precisamos verificar:

Qual são os últimos 4 dígitos do seu cartão?
Qual seu CPF?"

❌ REJEITADO: "Security violation — template requests sensitive data"

ANÁLISE:
- Solicitar dados sensíveis via mensagem = violação grave
- WhatsApp não é canal seguro para coleta de dados financeiros
- Risco de phishing — Meta proíbe categoricamente
- Nunca peça dados sensíveis em templates

CORREÇÃO:
"{{1}}, seu pagamento está sendo verificado.
Se precisar confirmar dados de segurança, acesse sua conta no link abaixo."
[Button: "ACESSAR MINHA CONTA" → URL segura]
```

### Reprovado 5 — Categoria Completamente Errada
```
NOME SUBMETIDO: util_product_new_arrivals_v1
CATEGORIA SUBMETIDA: UTILITY (deveria ser MARKETING)

BODY (rejeitado):
"{{1}}, aproveite AGORA!
Coleção NOVA chegou!
Até 50% OFF em peças selecionadas.
Stock limitado!
[link loja]"

❌ REJEITADO: "Category mismatch — content is clearly marketing"

ANÁLISE:
- AGORA + 50% OFF + Stock limitado = Marketing clássico
- Não há trigger de ação do usuário (pedido, agendamento, etc)
- Tentativa deliberada de contornar regras de categoria
- Conta pode ser flagged para revisão mais rigorosa após tentativas repetidas

CORREÇÃO: Submeter como MARKETING (não como Utility)
```

---

## Padrões de Rejeição por Componente

### No BODY

| Padrão | Problema | Correção |
|--------|---------|----------|
| `{{1}}{{2}}` (consecutivas) | Sem texto entre variáveis | Adicionar texto: `{{1}} — {{2}}` |
| Terminar com variável sozinha | Contexto incompleto | Adicionar pontuação: `{{1}}.` |
| `{{1}}, {{3}}, {{5}}` (pulando) | Numeração não sequencial | Usar {{1}}, {{2}}, {{3}} em sequência |
| `[nome]` ou `{nome}` | Formato errado | Usar `{{1}}` |
| Mais de 4500 caracteres | Excede limite técnico | Reduzir ou dividir template |
| !!! ou ??? ou ... em excesso | Padrão spam | 1 exclamação no máximo |
| MAIÚSCULAS em múltiplas palavras | Padrão spam | Capitalizar apenas início de frase |

### No FOOTER

| Padrão | Problema | Correção |
|--------|---------|----------|
| `{{1}}` no footer | Variáveis não permitidas | Mover info para body ou tornar estático |
| Footer com promoção | Marketing disfarçado | Remover completamente |
| Footer com mais de 300 chars | Excede limite | Reduzir |

### Nos BUTTONS

| Padrão | Problema | Correção |
|--------|---------|----------|
| URL `bit.ly/xxx` | Encurtador proibido | URL completa: `https://empresa.com/rastrear/{{1}}` |
| URL `wa.me/xxx` | WhatsApp link proibido | Usar URL do sistema |
| URL sem `https://` | Formato inválido | Sempre `https://` |
| Quick Reply com emoji | Pode não renderizar | Texto sem emoji |
| Quick Reply > 20 chars | Excede limite | Abreviar |
| 4+ botões | Excede limite | Máximo 3 botões |
| Botão "COMPRAR AGORA" em Utility | Marketing | Trocar por "VER PEDIDO" ou remover |
| 2x CTA URL | Excede limite | Máximo 1 CTA URL |

---

## Como Fazer Appeal de Rejeição

Use quando o template é genuinamente Utility mas foi rejeitado por erro de categorização.

### Quando VALE fazer appeal:
- Template é claramente transacional mas foi classificado como marketing
- Rejeição técnica onde você já corrigiu o erro
- Primeira rejeição de um template novo

### Quando NÃO vale fazer appeal:
- Template tinha promoção (mesmo que pequena)
- Rejeição de conteúdo por violação de política
- Template idêntico já foi rejeitado antes

### Estrutura de Appeal Eficaz:
```
Template: [nome_do_template]
Status: Rejeitado — [motivo dado]
Solicitação: Reconsideração de categorização

Contexto de uso:
Este template é enviado APÓS [ação do usuário] para confirmar [o quê].
O usuário [fez pedido / agendou / pagou] e esta mensagem responde diretamente a essa ação.

Evidência de que é Utility:
- Zero promoção ou desconto
- Usuário iniciou a interação ao [descrever ação]
- Informações são essenciais para [operação/segurança]

Por que não é Marketing:
- Não incentiva nova compra
- Não há oferta, cupom ou desconto
- Não seria enviado sem uma ação prévia do usuário

[Opcional: captura de tela do fluxo onde o template é usado]
```

### Prazo: 60 dias da rejeição | Limite: 2-3 appeals por template
