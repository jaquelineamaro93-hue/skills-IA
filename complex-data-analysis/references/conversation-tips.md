# Dicas para Analise de Dados de Conversas

Quando o dataset incluir conversas (WhatsApp, chatbot, atendimento ao vivo), aplique estas tecnicas alem das 6 lentes.

---

## Metricas Especificas de Conversas

- **Indice de complexidade:** Numero de mensagens por conversa. Cruze com desfecho (conversao, satisfacao, resolucao). Conversas mais longas convertem mais ou menos? A resposta depende do contexto e quase sempre surpreende.

- **Pontos de desistencia:** Em qual mensagem a conversa tende a morrer? Agrupe por fase do funil (saudacao, qualificacao, proposta, fechamento). Identifique as "mensagens assassinas" — a mensagem apos a qual o abandono dispara.

- **Padrao de turnos:** Quem fala mais — cliente ou atendente/bot? Calcule a proporcao e cruze com conversao. Em vendas consultivas, atendentes que "ouvem mais" tendem a converter mais. Em suporte, o inverso pode ser verdade.

- **Perguntas-gatilho:** Perguntas do cliente que correlacionam com conversao positiva (ex: "qual o prazo?", "tem desconto?", "como funciona o contrato?"). Liste as top 10 e calcule a taxa de conversao de quem fez cada pergunta. Essas perguntas sao sinais de intencao de compra.

- **Tempo de resposta:** Tempo entre mensagem do cliente e resposta do atendente/bot. Cruze com satisfacao e conversao. Existe um limiar a partir do qual o tempo de resposta mata a conversao? Em muitos casos, >5min ja impacta.

- **Curva de engajamento:** Mapeie o numero de mensagens do cliente ao longo da conversa. Conversas onde o cliente vai "esfriando" (mensagens mais curtas, menos frequentes) sao sinais de perda iminente.

---

## Analise de Linguagem

- Identifique as 20 palavras/expressoes mais frequentes em conversas que converteram vs. que nao converteram
- Analise o uso de emojis, audios e imagens como sinais de engajamento
- Procure momentos de "virada" na conversa — a mensagem apos a qual o tom/direcao muda
- Classifique sentimento por mensagem e mapeie a curva emocional da conversa
- Identifique perguntas que o bot/atendente nao conseguiu responder — essas lacunas sao oportunidades de melhoria

---

## Analise de Fluxo (Bots)

- Mapeie a arvore de decisoes **real** (nao a projetada) — quais caminhos os usuarios realmente seguem?
- Identifique loops (usuario voltando ao mesmo ponto) — indica confusao ou informacao insuficiente
- Calcule a taxa de transbordo para humano por no do fluxo — quais perguntas o bot nao resolve?
- Mensagens de "fuga" (usuario digitando texto livre quando esperava botao) revelam necessidades nao mapeadas
- Compare o funil projetado vs. o funil real — onde a divergencia e maior?

---

## Integracao com as 6 Lentes

| Lente | Aplicacao em conversas |
|---|---|
| Sinais Fracos | Operadores/bots com conversao radicalmente diferente da media |
| Inversao | Conversas que pareciam perdidas mas converteram — o que aconteceu? |
| Temporal 2a Ordem | Horarios/dias onde a taxa de conversao esta acelerando ou desacelerando |
| Quali-Quanti | Palavras em conversas de sucesso vs. fracasso |
| Proporcoes | Taxa de resolucao por tipo de problema (nao so volume) |
| Lacunas | Horarios sem cobertura, perguntas sem resposta, segmentos sem atendimento |
