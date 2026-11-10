# Tipos de processo: modelos de partida

Use o modelo do tipo de processo como régua. O processo real do cliente manda; o modelo serve para enxergar
o que está faltando.

## Perguntas que valem para qualquer processo
1. **O que dispara?** (um evento, uma data, uma ação de alguém)
2. **Qual é o resultado esperado?** E quais outros finais existem (perda, cancelamento, escalonamento)?
3. **Quem participa?** Cliente, times, sistemas. Cada um vira uma raia.
4. **Onde alguém decide algo?** Com qual critério?
5. **Onde alguém espera?** Por quanto tempo, e o que acontece se passar do prazo?
6. **Que dado entra ou sai** em cada etapa, e em qual sistema fica?
7. **Como se mede** que funcionou?

---

## 1. Vendas e pré-vendas
Modelo: Recepção → Triagem → Qualificação → Agenda (opcional) → Qualificado / Desqualificado.
Detalhes completos em `etapas-sdr.md`.

## 2. Lifecycle / jornada do cliente
Modelo de ciclo de vida:
```
Entrada → Onboarding → Ativação → Engajamento → Retenção / Renovação → Expansão
                │            │            │               │
                └────────────┴────────────┴──► Risco ──► Reativação ──► Perdido (porta aberta)
```

| Etapa | Pergunta-chave | Exemplos de ação |
|---|---|---|
| Entrada | Como a pessoa vira cliente/usuária? | boas-vindas, confirmação, primeiro acesso |
| Onboarding | O que ela precisa fazer para começar? | guia passo a passo, checklist, vídeo curto |
| Ativação | Qual é o "momento aha" (a primeira ação que mostra valor)? | lembrete de ação pendente, ajuda humana |
| Engajamento | O que mostra que ela continua usando? | conteúdo útil, novidades, conquistas |
| Risco | Quais sinais mostram que vai embora? | queda de uso, reclamação, pagamento falhou |
| Retenção / renovação | O que fazer antes do fim do contrato ou do ciclo? | contato de sucesso, oferta de renovação |
| Reativação | Como trazer de volta quem parou? | mensagem de saudade, oferta, pesquisa de motivo |
| Expansão | Quando oferecer mais? | upsell, indicação, plano maior |

**Desenho do lifecycle no quadro:** uma raia por canal (e-mail, WhatsApp, push, SMS, ligação, tarefa para o time)
ou por etapa, com o tempo correndo da esquerda para a direita. Cada mensagem mostra: gatilho, espera, público e a
saída ("abriu e fez a ação" segue, "não fez" recebe o próximo toque, "fez a ação" sai da régua).

**Régua (entregável do modo Lifecycle):**
| Etapa | Gatilho | Espera | Canal | Público | Objetivo | Mensagem (rascunho) | Métrica | Regra de saída |
|---|---|---|---|---|---|---|---|---|

Regras da régua:
- Toda régua tem **regra de saída** (quando a pessoa faz a ação, para de receber).
- **Limite de contato** por pessoa e por semana, somando todas as réguas.
- Mensagem útil antes de mensagem de venda. Respeite opt-out e LGPD.
- Uma métrica principal por etapa (ex.: ativação = % que fez a ação-chave em 7 dias).
- Segmente pelo comportamento (o que a pessoa fez), não só pelo cadastro.

## 3. Atendimento e suporte
```
Contato → Identificação → Triagem (tema e urgência) → Resolução no 1º nível ─► Resolvido → Pesquisa de satisfação
                                     │
                                     └► Escalonamento (2º nível / especialista) ─► Resolvido / Retorno ao cliente
```
- Defina o prazo de cada nível (SLA) e o que acontece quando estoura.
- Mostre o que o cliente recebe em cada passagem ("seu caso foi para o time X, retorno até Y").
- Reabertura: se o cliente responder depois de resolvido, para onde vai?
- Agente de IA de suporte: o que ele resolve sozinho, o que encaminha e para quem.

## 4. Operação interna
Exemplos: pedido até entrega, aprovação de compra, contratação, onboarding de colaborador, fechamento financeiro.
- Uma raia por área ou papel (solicitante, aprovador, financeiro, TI).
- Cada aprovação é um losango com: aprovado, reprovado (volta para quem com qual ajuste) e sem resposta (prazo e lembrete).
- Marque o que é manual e o que é automático (sistema): é onde costuma estar a oportunidade de melhoria.
- Entregável natural: o POP (passo a passo) com responsável, prazo e ferramenta.

## 5. Outro processo
Use as 7 perguntas do topo e desenhe em raias por participante. Se o processo tiver conversa com cliente, a parte
de conversa pode virar agente de IA (Fase 4).

---

## Gargalos para procurar em qualquer tipo
- Etapa sem dono.
- Espera sem prazo.
- Decisão sem critério escrito.
- Mesma informação pedida duas vezes.
- Passagem entre áreas sem aviso para o cliente.
- Etapa sem medição.
- Muita gente parada numa etapa (quando houver números): marque com nota e a taxa.
