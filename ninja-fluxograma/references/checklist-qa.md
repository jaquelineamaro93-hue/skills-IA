# Checklist de qualidade

Rode antes de entregar e no modo Auditoria. Cada item reprovado: corrija ou liste em "Confirmar com o responsável".

## Qualquer processo
- [ ] Começo (o que dispara) e todos os finais possíveis desenhados.
- [ ] Toda etapa tem dono (pessoa, time ou sistema).
- [ ] Toda decisão tem critério escrito e todas as saídas, inclusive "sem resposta".
- [ ] Toda espera tem prazo; todo laço tem limite.
- [ ] Toda passagem entre áreas avisa quem está do outro lado.
- [ ] Cada etapa tem como medir se funcionou.
- [ ] Lifecycle: toda régua tem regra de saída e limite de contatos por pessoa.

## Processo de vendas / agente
- [ ] Contexto antes e depois do SDR escrito (1 parágrafo cada).
- [ ] Nenhuma regra de negócio inventada; premissas listadas.
- [ ] Lead muito quente perguntado (existe ou "não se aplica" confirmado).
- [ ] Destino do qualificado definido (humano, reunião, continua conversando).

## Funil
- [ ] Recepção leva para a Triagem no mesmo turno da primeira resposta.
- [ ] Cada critério eliminatório tem pergunta própria e motivo de desqualificação próprio.
- [ ] Qualificação liga a dor do lead a uma solução real do catálogo.
- [ ] Agenda (se existir) valida data passada, fim de semana, horário indisponível, e tem limite de voltas.
- [ ] Qualificado tem sub-tipos e não tem follow-up automático.
- [ ] Desqualificado é reativo e reabre quando o lead corrige a informação.

## Etapas (texto)
- [ ] Todo passo tem Regras, Objetivo e Fallback.
- [ ] Uma ação por linha; nada escondido dentro de regra.
- [ ] Toda mudança de etapa, transferência ou encerramento tem mensagem antes.
- [ ] Todo laço tem limite.
- [ ] Templates nomeados em `snake_case` e escritos na seção Templates.
- [ ] Nenhuma mensagem com 2 perguntas.
- [ ] `etapa_atual` atualizado no início de cada etapa; `subtipo_resultado` e `motivo_desqualificacao` nos terminais.

## Prompt
- [ ] Persona não finge ser humana.
- [ ] Comunicação com tamanho de mensagem, 1 pergunta por vez, regra de desvio, regra de emoji.
- [ ] Catálogo sem recurso inventado; preços só se autorizados.
- [ ] Objeções principais cobertas (preço, concorrente, timing, "manda por e-mail", decisor).
- [ ] Fora do escopo, limitações e escalonamento para humano escritos.
- [ ] Informação de produto não repetida nas etapas.
- [ ] Sem dado pessoal, senha, token ou URL interna.

## Auditoria de expansão
Para cada etapa, conte as ações descritas e compare com as linhas do Objetivo:
```
✅ Triagem: 4 critérios → 4 passos + 4 sub-passos de desqualificação
⚠️ Qualificação: Passo 2 tem 3 ações escondidas (template de desq, campo, mudança de etapa) → quebrar
```

## Conversas de teste (escreva e "rode" mentalmente contra as etapas)
1. Caminho feliz até Qualificado.
2. Um teste por motivo de desqualificação.
3. Lead desqualificado que corrige o dado e volta.
4. Lead que responde 3 perguntas de uma vez (o agente não repete).
5. Lead muito quente.
6. Objeção de preço e de concorrente.
7. Pedido de falar com humano.
8. Desvio de assunto no meio da Qualificação.
9. Resposta vaga ("depende", "mais ou menos").
10. Agenda: escolhe sábado, depois horário que já passou.

Para cada teste, mostre: mensagens do lead, resposta esperada, etapa e campos no final.
