# Regras de Copywriting — Templates Utility WhatsApp

Referência técnica completa para escrever templates que passam na revisão da Meta.

---

## Limites de Caracteres por Componente

| Componente | Limite Técnico | Recomendado | Notas |
|-----------|----------------|-------------|-------|
| Header (texto) | 60 chars | 40-50 | Inclui espaços |
| Body | 4.500 chars | 400-1.000 | Templates longos têm mais chance de revisão humana |
| Footer | 300 chars | 100-200 | Sem variáveis dinâmicas |
| Quick Reply (texto) | 20 chars | 12-18 | Sem emojis |
| CTA Button (texto) | 25 chars | 15-20 | Testável em ambos iOS e Android |
| Template Name | 512 chars | 30-50 | Lowercase + underscore + números |
| Emojis (total body) | Sem limite formal | 2-5 | Mais que 8 aumenta risco de spam |

---

## Regras de Variáveis — Obrigatórias

### Formato Único Aceito
```
✅ CERTO:  {{1}}  {{2}}  {{3}}  {{4}}
❌ ERRADO: [1]  {1}  ${1}  @1  [[1]]  {{name}}  [nome]
```

### Numeração Sequencial (sem pular)
```
✅ CERTO:  {{1}}, {{2}}, {{3}}, {{4}}
❌ ERRADO: {{1}}, {{3}}, {{5}}   ← números pulados = rejeição
```

### Sem Variáveis Consecutivas
```
✅ CERTO:  "Olá {{1}}, seu pedido {{2}} foi enviado"
❌ ERRADO: "Olá {{1}}{{2}}, seu pedido foi enviado"
❌ ERRADO: "Status: {{1}}: {{2}}"  ← texto de separação necessário
```

### Posicionamento no Body
```
✅ OK terminar com variável + pontuação: "Código: {{1}}."
✅ OK terminar com variável + texto: "{{1}} em breve."
⚠️ EVITAR terminar só com variável: "Código: {{1}}"  ← tecnicamente ok, mas pode dar problema
❌ ERRADO: Variável no footer
```

### Limites de Quantidade
| Componente | Máximo de Variáveis |
|-----------|---------------------|
| Header | 1 |
| Body | 20 |
| Footer | 0 (proibido) |
| CTA URL button | 1 (no final da URL) |

### Quantidade Ideal por Contexto
- 0-2 variáveis: Simples, alta aprovação (confirmações básicas)
- 3-5 variáveis: Ideal (agendamentos, pedidos)
- 6-9 variáveis: Aceitável (templates detalhados)
- 10+ variáveis: Documente bem os samples, considere dividir

---

## Sample Values — A Regra Mais Importante

Os sample values que você fornece treinam o modelo de aprovação da Meta. Genéricos = rejeição.

### Padrão
```
❌ RUIM:
{{1}} = "name"
{{2}} = "order_id"
{{3}} = "date"
{{4}} = "amount"

✅ BOM:
{{1}} = "Maria Silva"
{{2}} = "PED-2026-001234"
{{3}} = "25 de abril de 2026"
{{4}} = "R$ 199,90"
```

### Regras para Sample Values Eficazes

1. **Comprimento realista**: Use o comprimento que o dado real terá
   ```
   ❌ {{1}} = "Jo"  (muito curto)
   ✅ {{1}} = "João Paulo Rodrigues"  (comprimento real)
   ```

2. **Formato correto**: O formato deve corresponder ao dado real
   ```
   ❌ {{1}} = "123"  (para CPF)
   ✅ {{1}} = "123.456.789-00"  (formato real)
   
   ❌ {{1}} = "hoje"  (para data)
   ✅ {{1}} = "15 de abril de 2026"  (formato real)
   ```

3. **Sem dados inventados suspeitamente**: Nada que pareça placeholder
   ```
   ❌ {{1}} = "XXXXXXXXXXXXX"
   ❌ {{1}} = "test_value_123"
   ❌ {{1}} = "variavel_nome"
   ```

4. **Consistência**: Se {{1}} é nome, o sample deve ser um nome
   ```
   ❌ {{1}} = "12345"  (quando {{1}} é usado como "Olá {{1}},")
   ✅ {{1}} = "Maria"  (quando {{1}} é usado como "Olá {{1}},")
   ```

---

## Tom de Voz por Vertical

### E-commerce / Varejo
- **Tom:** Amigável e direto
- **Você ou Seu/Sua:** Use "Seu pedido", "Sua entrega"
- **Saudação:** "Oi {{1}}," ou "Olá {{1}},"
- **Cuidado:** Não use "Incrível!", "Que ótimo!", "Maravilhoso!"

### Saúde / Healthcare
- **Tom:** Formal, respeitoso, claro
- **Você ou Seu/Sua:** Prefira "Sua consulta", "Seu exame"
- **Saudação:** "Olá {{1}}," ou simplesmente "{{1}},"
- **Cuidado:** Nunca mencione diagnóstico ou resultado diretamente (privacidade)

### Financeiro / Bancos
- **Tom:** Profissional, seguro, preciso
- **Você ou Seu/Sua:** "Seu pagamento", "Sua transação"
- **Saudação:** "{{1}}," ou "Prezado(a) {{1}},"
- **Cuidado:** Nunca peça dados sensíveis. Nunca mencione valores de forma casual.

### Logística / Transportes
- **Tom:** Direto, operacional, informativo
- **Você ou Seu/Sua:** "Seu pedido", "Sua encomenda"
- **Saudação:** "Oi {{1}}," é adequado
- **Cuidado:** Não prometa horários que o sistema não garante

### Imobiliário
- **Tom:** Profissional, mas acolhedor
- **Você ou Seu/Sua:** "Sua visita", "Seu interesse"
- **Saudação:** "Olá {{1}},"
- **Cuidado:** Não mencione preços ou negociações no Utility

### Educação
- **Tom:** Motivacional-neutro (encorajador sem ser entusiasmado)
- **Você ou Seu/Sua:** "Sua matrícula", "Seu acesso"
- **Saudação:** "Olá {{1}}," ou "{{1}},"
- **Cuidado:** "Parabéns" é ok para confirmação de inscrição, não para promoção

---

## Uso de Emojis — Guia Prático

### Emojis Seguros para Utility
```
✓ ✅ ☑️     → Status positivo, confirmação
📦 📫 📬    → Logística, entrega
📅 🗓️        → Data, agendamento
📍 🗺️        → Localização
💰 💳        → Financeiro
👨‍⚕️ 🏥      → Saúde
📋 📄        → Documentos
⏰ 🕐        → Horário
🆔           → Número de identificação
🏠 🏢        → Imobiliário
🎓           → Educação
🔐 🔒       → Segurança
```

### Emojis que Aumentam Risco de Rejeição em Utility
```
🎉 🎊 🥳    → Festivos, associados a marketing
💥 🔥 ⚡    → Urgência/impacto visual = spam
🛒 🛍️        → Compras = marketing
🤑 💵 💎    → Dinheiro de forma informal
❗ ‼️         → Urgência excessiva
👑 ⭐ 🌟    → Grandiosidade = marketing
```

### Regra de Ouro dos Emojis
- Use 1-2 emojis para identificar seções (📦 = envio, ⏰ = horário)
- Máximo 5 emojis por template
- Nunca 2+ emojis consecutivos em Utility

---

## Estrutura Recomendada de BODY

### Padrão Geral (funciona para 80% dos casos)
```
[Saudação com nome]

[Confirmação da ação — 1 linha]

[Detalhes essenciais — 3-6 linhas com variáveis]

[Próximo passo ou instrução — 1 linha]

[Opcional: nota de rodapé curta]
```

### Exemplos de Abertura Aprovados
```
"Olá {{1}},"
"Oi {{1}},"
"{{1}},"
"Prezado(a) {{1}},"
"Olá {{1}}, tudo bem?"  ← OK em contextos informais
```

### Exemplos de Confirmação de Ação (1 linha)
```
"Seu pedido foi confirmado! ✓"
"Sua consulta está agendada."
"Pagamento recebido com sucesso. ✓"
"Sua entrega saiu agora! 📦"
"Sua inscrição foi concluída. 🎓"
"Detectamos uma atividade em sua conta."
"Sua fatura está disponível."
```

### Blocos de Detalhes — Formatação Recomendada
```
Opção 1 — Com emoji de categoria:
📦 Pedido: {{1}}
📅 Data: {{2}}
💰 Valor: {{3}}

Opção 2 — Com negrito (se BSP suportar):
*Pedido:* {{1}}
*Data:* {{2}}
*Valor:* {{3}}

Opção 3 — Simples
Pedido: {{1}}
Data: {{2}}
Valor: {{3}}
```

### Fechamentos Aprovados
```
"Se tiver dúvidas, entre em contato com nosso SAC."
"Acompanhe tudo pelo botão abaixo."
"Guarde este comprovante."
"Até logo!"
"Obrigado."
"Qualquer questão, estamos à disposição."
```

---

## Naming Convention de Templates

### Padrão Obrigatório
```
[categoria]_[vertical]_[tipo_de_acao]_[versao]

util_ecommerce_order_confirmation_v1
util_healthcare_appointment_reminder_v1
util_logistics_delivery_tracking_v2
util_financial_payment_confirmation_v1
auth_otp_login_v1
```

### Regras do Nome
- Sempre lowercase (minúsculas)
- Apenas underscore `_` para separar (sem hífen, sem espaço)
- Apenas letras, números e underscores
- Máximo 512 chars (use no máximo 50 na prática)
- Único dentro da WABA (não pode duplicar)
- Não pode ser editado após aprovação (apenas via nova versão)

### Boas Práticas de Versioning
```
v1 = versão inicial
v2 = primeira revisão significativa
v3 = segunda revisão

util_order_confirm_v1  →  aprovado, em uso
util_order_confirm_v2  →  novo com header adicionado
util_order_confirm_v3  →  versão com botão de rastreamento
```

---

## Processo de Aprovação — Tempos e Estratégias

### Fluxo de Revisão
```
1. VALIDAÇÃO TÉCNICA (automática, < 1 min)
   → Formato correto? Variáveis bem formadas?
   → Se falhar: rejeição imediata com motivo técnico

2. ANÁLISE DE CONTEÚDO (automática, 2-10 min)
   → Palavras-chave proibidas? Padrões de spam?
   → Se ok: aprovado
   → Se flag: fila para revisão humana

3. REVISÃO HUMANA (24-48h)
   → Especialista avalia intenção + categoria
   → Resultado: Aprovado, Rejeitado ou Reclassificado
```

### Tempos Médios em 2025-2026
| Cenário | Tempo | Taxa de Sucesso |
|---------|-------|----------------|
| Utility bem formado, sem flags | 5-15 min | 95%+ |
| Utility com palavras suspeitas | 24-48h | 70-80% |
| Marketing padrão | 24-72h | 60-70% |
| Appeal de rejeição | 48-72h | 40-60% |

### Dicas para Aprovação Mais Rápida

1. **Submeta em lote pequeno** (1-3 templates por vez, não 10-20)
2. **Horário:** Submeta de segunda a quinta, entre 8h-16h (horário de Brasília)
3. **Nome descritivo:** `util_healthcare_appointment_reminder_v1` vs `template_001`
4. **Samples realistas:** Aumenta taxa de aprovação automática para 95%+
5. **Zero ambiguidade:** Template onde a intenção é 100% óbvia passa automaticamente
6. **Evite modificações repetidas:** Cada edição pós-rejeição reinicia o processo

---

## Componentes de Buttons — Referência Completa

### Quick Reply
```json
{
  "type": "QUICK_REPLY",
  "text": "CONFIRMAR"
}
```
- Texto: 1-20 chars, estático, sem variáveis, sem emojis
- Limit: 3 Quick Replies por template
- Payload (invisível ao usuário): até 256 chars, string identificadora

### CTA URL (dinâmica)
```json
{
  "type": "URL",
  "text": "RASTREAR PEDIDO",
  "url": "https://empresa.com/track/{{1}}",
  "example": ["PED-2026-001234"]
}
```
- URL: deve começar com https://
- Variável: no final da URL, apenas {{1}} (máximo 1)
- Máximo 1 CTA URL por template
- Texto: até 25 chars

### CTA Telefone
```json
{
  "type": "PHONE_NUMBER",
  "text": "LIGAR PARA SUPORTE",
  "phone_number": "+5511300000000"
}
```
- Número no formato E.164 (+55...)
- Máximo 1 CTA Phone por template
- Texto: até 25 chars

### FLOW Button
```json
{
  "type": "FLOW",
  "text": "ESCOLHER NOVA DATA",
  "flow_id": "FLOW_ID_AQUI",
  "flow_action": "navigate",
  "navigate_screen": "SCREEN_ID"
}
```
- Use para interações complexas (escolha de data/hora, múltiplas opções)
- Requer Flow previamente criado e publicado

### Combinações Válidas
```
✅ 3x Quick Reply
✅ 1x CTA URL + 2x Quick Reply
✅ 1x CTA URL + 1x CTA Phone
✅ 1x FLOW button
✅ 1x CTA URL (sozinho)
✅ Sem botões

❌ 2x CTA URL (limite: 1)
❌ 2x CTA Phone (limite: 1)
❌ 4+ Quick Replies (limite: 3)
❌ 4+ botões total (limite: 3)
```

---

## Payload JSON Completo — Template de Referência

```json
{
  "name": "util_vertical_action_v1",
  "language": "pt_BR",
  "category": "UTILITY",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Título do Header"
    },
    {
      "type": "BODY",
      "text": "Olá {{1}},\n\nSeu {{2}} foi confirmado.\n\nDetalhes:\n📅 Data: {{3}}\n💰 Valor: {{4}}\n\nAcompanhe pelo botão abaixo.",
      "example": {
        "body_text": [["Maria Silva", "pedido", "13 de abril de 2026", "R$ 199,90"]]
      }
    },
    {
      "type": "FOOTER",
      "text": "Empresa ABC | SAC: 0800-000-0000"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "VER DETALHES",
          "url": "https://empresa.com/pedidos/{{5}}",
          "example": ["PED-2026-001234"]
        },
        {
          "type": "QUICK_REPLY",
          "text": "PRECISO DE AJUDA"
        }
      ]
    }
  ]
}
```

**Nota sobre `\n`:** No JSON, quebras de linha no body devem ser representadas como `\n`. No WhatsApp Manager (interface web), use Enter normalmente.
