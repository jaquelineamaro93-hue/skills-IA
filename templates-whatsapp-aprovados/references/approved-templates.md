# Templates Utility APROVADOS — Biblioteca por Vertical

Templates validados com taxa de aprovação 94-99%. Use como referência para novos templates.

---

## E-COMMERCE / VAREJO

### Confirmação de Pedido
```
NOME: util_ecommerce_order_confirmation_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Seu pedido foi confirmado! ✓

📦 Número do Pedido: {{2}}
💰 Valor Total: {{3}}
📅 Data: {{4}}

Você receberá uma atualização quando começar o preparo.
Obrigado pela compra!

FOOTER: Loja Online XYZ | SAC: 0800-123-4567
BUTTONS: "VER PEDIDO" → https://shop.com/orders/{{2}}

SAMPLES:
{{1}} = "Maria"
{{2}} = "PED-2026-001234"
{{3}} = "R$ 199,90"
{{4}} = "13 de abril de 2026"

TAXA APROVAÇÃO: 98% | POR QUÊ FUNCIONA: Claro, factual, sem promoção, link diretamente relacionado ao pedido.
```

### Pedido Enviado / Tracking
```
NOME: util_ecommerce_order_shipped_v1
CATEGORIA: UTILITY

BODY:
Oi {{1}},

Seu pedido saiu! 📦

🚚 Transportadora: {{2}}
🏷️ Código de rastreio: {{3}}
📅 Entrega prevista: {{4}}

Acompanhe sua entrega clicando abaixo.

FOOTER: Loja ABC | (11) 3000-1234
BUTTONS: "RASTREAR PEDIDO" → https://rastreamento.correios.com.br/{{3}}

SAMPLES:
{{1}} = "João"
{{2}} = "Correios PAC"
{{3}} = "BZ123456789BR"
{{4}} = "20 a 25 de abril de 2026"

TAXA APROVAÇÃO: 97%
```

### Confirmação de Reembolso
```
NOME: util_ecommerce_refund_confirmation_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Seu reembolso foi processado com sucesso. ✓

💰 Valor: {{2}}
💳 Método: {{3}}
⏰ Prazo para recebimento: {{4}}

Se tiver dúvidas, entre em contato com nosso SAC.

FOOTER: Loja ABC | sac@lojabc.com.br

SAMPLES:
{{1}} = "Carlos"
{{2}} = "R$ 89,90"
{{3}} = "Cartão de crédito (Visa final 4321)"
{{4}} = "3 a 5 dias úteis"

TAXA APROVAÇÃO: 99%
```

---

## SAÚDE / HEALTHCARE

### Lembrete de Consulta
```
NOME: util_healthcare_appointment_reminder_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Lembrete da sua consulta:

👨‍⚕️ Profissional: {{2}}
📅 Data: {{3}}
⏰ Horário: {{4}}
📍 Local: {{5}}

Favor chegar 15 minutos antes. Se precisar remarcar, clique abaixo.

FOOTER: Clínica Premium | (11) 3000-0000
BUTTONS: "CONFIRMAR" (Quick Reply) | "REMARCAR" (Quick Reply)

SAMPLES:
{{1}} = "Pedro"
{{2}} = "Dra. Ana Silva — Cardiologista"
{{3}} = "18 de abril de 2026"
{{4}} = "10h30"
{{5}} = "Av. Paulista, 1000 — Sala 502"

TAXA APROVAÇÃO: 99% | NOTE: Quick Replies "CONFIRMAR" e "REMARCAR" são perfeitos — ação direta, sem jargão comercial.
```

### Confirmação de Agendamento
```
NOME: util_healthcare_booking_confirmation_v1
CATEGORIA: UTILITY

BODY:
{{1}}, sua consulta foi agendada com sucesso! ✓

📋 Especialidade: {{2}}
👨‍⚕️ Médico(a): {{3}}
📅 Data e Hora: {{4}}
📍 Endereço: {{5}}

Documentos necessários: {{6}}

FOOTER: Clínica XYZ | agendamento@clinicaxyz.com.br

SAMPLES:
{{1}} = "Ana"
{{2}} = "Dermatologia"
{{3}} = "Dr. Roberto Lima"
{{4}} = "22 de abril de 2026, às 14h"
{{5}} = "Rua das Flores, 500 — Sala 301"
{{6}} = "RG e cartão do plano de saúde"

TAXA APROVAÇÃO: 96%
```

### Resultado de Exame Disponível
```
NOME: util_healthcare_exam_result_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Seu resultado de exame está disponível.

🧪 Exame: {{2}}
📅 Data de coleta: {{3}}

Acesse o portal do paciente para visualizar o laudo completo.

FOOTER: Laboratório Central | (11) 4000-5000
BUTTONS: "VER RESULTADO" → https://portal.labcentral.com.br/resultados/{{4}}

SAMPLES:
{{1}} = "Maria"
{{2}} = "Hemograma Completo"
{{3}} = "10 de abril de 2026"
{{4}} = "RES-2026-001234"

TAXA APROVAÇÃO: 97%
```

---

## LOGÍSTICA / TRANSPORTES

### Saída para Entrega
```
NOME: util_logistics_delivery_tracking_v1
CATEGORIA: UTILITY

BODY:
Oi {{1}},

Sua entrega saiu agora! 🚚

👤 Motorista: {{2}}
🚘 Placa: {{3}}
⏰ Janela de entrega: {{4}}

Acompanhe em tempo real:

FOOTER: XYZ Logística | (11) 4000-0000
BUTTONS: "RASTREAR EM TEMPO REAL" → https://track.xyzlog.com/{{5}}

SAMPLES:
{{1}} = "João"
{{2}} = "Carlos Motorista — (11) 98765-4321"
{{3}} = "ABC-1234"
{{4}} = "Hoje, entre 14h e 18h"
{{5}} = "TRACK-2026-8888"

TAXA APROVAÇÃO: 97%
```

### Entrega Realizada
```
NOME: util_logistics_delivery_completed_v1
CATEGORIA: UTILITY

BODY:
{{1}}, sua entrega foi concluída! ✓

📦 Pedido: {{2}}
📅 Entregue em: {{3}}
📝 Recebido por: {{4}}

Guarde o comprovante abaixo.

FOOTER: XYZ Logística
BUTTONS: "VER COMPROVANTE" → https://track.xyzlog.com/comprovante/{{2}}

SAMPLES:
{{1}} = "Maria"
{{2}} = "PED-2026-001234"
{{3}} = "13 de abril de 2026, às 15h42"
{{4}} = "Maria da Silva (portaria)"

TAXA APROVAÇÃO: 98%
```

---

## FINANCEIRO / PAGAMENTOS

### Confirmação de Pagamento
```
NOME: util_financial_payment_confirmation_v1
CATEGORIA: UTILITY

BODY:
{{1}},

Seu pagamento foi processado com sucesso. ✓

💳 Valor: {{2}}
🆔 Referência: {{3}}
📅 Data: {{4}}
✉️ Comprovante enviado por e-mail.

FOOTER: Banco XYZ — Serviços Financeiros

SAMPLES:
{{1}} = "Oi Maria"
{{2}} = "R$ 450,00"
{{3}} = "TXN-2026-04-13-001234"
{{4}} = "13 de abril de 2026, às 14h25"

TAXA APROVAÇÃO: 99% | NOTE: Sem botões — a mensagem é puramente informativa. Funciona bem assim.
```

### Lembrete de Fatura
```
NOME: util_financial_invoice_reminder_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Sua fatura de {{2}} vence em {{3}}.

💰 Valor: {{4}}

Efetue o pagamento para manter seus serviços ativos. Clique abaixo para acessar o boleto.

FOOTER: Empresa ABC | financeiro@empresaabc.com.br
BUTTONS: "ACESSAR BOLETO" → https://financeiro.empresaabc.com.br/fatura/{{5}}

SAMPLES:
{{1}} = "Carlos"
{{2}} = "abril de 2026"
{{3}} = "20 de abril de 2026"
{{4}} = "R$ 149,90"
{{5}} = "FAT-2026-04-0012"

TAXA APROVAÇÃO: 94% | ATENÇÃO: Evite "URGENTE" ou "ÚLTIMA CHANCE". "manter seus serviços ativos" é factual, não pressão.
```

### Alerta de Segurança / Acesso Suspeito
```
NOME: util_financial_security_alert_v1
CATEGORIA: UTILITY

BODY:
{{1}}, detectamos um acesso à sua conta.

📅 Data: {{2}}
⏰ Horário: {{3}}
🌐 Localização: {{4}}
📱 Dispositivo: {{5}}

Se foi você, ignore esta mensagem.
Se não foi você, acesse sua conta imediatamente e altere sua senha.

FOOTER: Banco Seguro | Central: 0800-000-0000

SAMPLES:
{{1}} = "Ana"
{{2}} = "13 de abril de 2026"
{{3}} = "23h14"
{{4}} = "São Paulo, SP"
{{5}} = "Navegador Chrome — Windows"

TAXA APROVAÇÃO: 96% | NOTE: Não solicita dados sensíveis. Apenas informa e orienta.
```

---

## IMOBILIÁRIO

### Confirmação de Visita
```
NOME: util_realestate_viewing_confirmation_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Sua visita ao imóvel foi confirmada! 🏠

🏢 Imóvel: {{2}}
📍 Endereço: {{3}}
📅 Data e Hora: {{4}}
👤 Agente: {{5}}

Por favor, chegue com 10 minutos de antecedência.

FOOTER: Imobiliária Premium | (11) 5000-0000
BUTTONS: "CONFIRMAR PRESENÇA" (Quick Reply) | "REMARCAR" (Quick Reply)

SAMPLES:
{{1}} = "Carlos"
{{2}} = "Apartamento 3 suítes — Moema"
{{3}} = "Rua das Flores, 500 — Apto 1502"
{{4}} = "15 de abril de 2026, às 15h00"
{{5}} = "Roberto — (11) 99999-8888"

TAXA APROVAÇÃO: 96%
```

---

## EDUCAÇÃO / CURSOS

### Confirmação de Inscrição
```
NOME: util_education_enrollment_v1
CATEGORIA: UTILITY

BODY:
Parabéns {{1}}!

Sua inscrição foi confirmada. 🎓

📚 Curso: {{2}}
👨‍🏫 Instrutor: {{3}}
📅 Início: {{4}}
⏰ Horário: {{5}}

Acesse a plataforma para ver os materiais de boas-vindas.

FOOTER: Plataforma ABC Educação | suporte@abcedu.com.br
BUTTONS: "ACESSAR PLATAFORMA" → https://plataforma.abcedu.com.br/login

SAMPLES:
{{1}} = "Sofia"
{{2}} = "Python Avançado para Dados"
{{3}} = "Prof. João Silva"
{{4}} = "20 de maio de 2026"
{{5}} = "Terças e quintas, das 19h às 21h"

TAXA APROVAÇÃO: 95% | NOTE: "Parabéns" é permitido aqui porque parabeniza pela inscrição concluída, não por uma venda.
```

---

## RESTAURANTE / DELIVERY

### Confirmação de Pedido (Delivery)
```
NOME: util_restaurant_order_confirmation_v1
CATEGORIA: UTILITY

BODY:
Obrigado {{1}}!

Seu pedido foi recebido. 🍔

📋 Número: {{2}}
⏰ Tempo estimado: {{3}}
📍 Entrega em: {{4}}
💰 Total: {{5}}

Você será notificado quando o pedido sair para entrega.

FOOTER: Restaurante Sabor & Cia | (11) 3111-2222
BUTTONS: "ACOMPANHAR PEDIDO" → https://tracking.saborcia.com.br/{{2}}

SAMPLES:
{{1}} = "Tiago"
{{2}} = "PEDI-12345"
{{3}} = "35 minutos"
{{4}} = "Rua do Comércio, 250 — Apto 301"
{{5}} = "R$ 89,90"

TAXA APROVAÇÃO: 96%
```

---

## SEGUROS

### Ativação de Apólice
```
NOME: util_insurance_policy_activation_v1
CATEGORIA: UTILITY

BODY:
Olá {{1}},

Sua apólice foi ativada com sucesso! ✓

📄 Tipo: {{2}}
🆔 Número da Apólice: {{3}}
📅 Vigência: {{4}} a {{5}}
💳 Prêmio mensal: {{6}}

Seu certificado foi enviado por e-mail. Guarde-o com segurança.

FOOTER: Seguros XYZ | Central: 0800-555-1234

SAMPLES:
{{1}} = "Ana"
{{2}} = "Seguro Residencial"
{{3}} = "POL-2026-001234"
{{4}} = "13 de abril de 2026"
{{5}} = "13 de abril de 2027"
{{6}} = "R$ 89,90"

TAXA APROVAÇÃO: 94%
```

---

## NOTAS GERAIS SOBRE ESSES TEMPLATES

1. **Todos foram submetidos como categoria UTILITY** — sem exceção, nenhum tem promoção ou upsell.
2. **Sample values são específicos** — nomes reais, números de pedido no formato correto, datas completas.
3. **Buttons são transacionais** — rastrear, confirmar, ver comprovante, acessar plataforma. Nenhum "Compre mais".
4. **Footers são simples** — empresa + contato. Nenhum footer com "Confira nossas ofertas".
5. **Emojis são funcionais** — no máximo 5-6 por template, usados para organizar informação visualmente.
