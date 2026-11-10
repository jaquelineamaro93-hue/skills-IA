# Depois do cohort: transformar números em jornada e ação

O cohort mostra **quando** os clientes saem e **quem** fica. O passo seguinte é desenhar o que o time faz em cada
momento. Três entregáveis, nesta ordem.

## 1. Os três (ou quatro) caminhos depois da entrada
A aba **Caminhos** classifica cada cliente comparando a receita do último mês com a do mês de entrada:
| Caminho | O que é | O que fazer |
|---|---|---|
| Expandiu | paga mais que na entrada | casos de sucesso, indicação, champions, palco |
| Manteve | ativo, sem crescer | segundo produto, caso de uso avançado, mais usuários |
| Reduziu | ativo, pagando menos | entender o motivo antes da renovação |
| Saiu | não está ativo no último mês | em que mês saiu (Retenção) e por quê |

Mostre os números em blocos simples, como: "Expande: 18 clientes · Mantém: 55 contas ativas · Entrou em risco no
mês 4: 16 de 90 já saíram".

## 2. Jornada do cliente depois da compra
**As etapas vêm do cohort, não de um modelo pronto.** Use os pontos em que a curva de retenção muda:
- do mês 0 até o primeiro resultado (ativação);
- o mês em que a curva quebra (momento de risco);
- o mês de renovação ou de fim de contrato;
- quem passa desse ponto (expansão e advocacia).

Uma coluna por etapa, com período ("Semana 0", "Semanas 1 a 4", "Mês 1 a 2", "Mês 3 a 5", "Mês 6 a 8", "A partir do mês 6").
Linhas (camadas):
| Camada | Pergunta |
|---|---|
| Pontos de contato | Onde o cliente fala com a empresa nessa etapa? |
| Tarefas do cliente | O que ele precisa fazer? |
| Dor principal | O que costuma dar errado? (use o que o cohort e o time de atendimento mostram) |
| Sentimento | Como ele se sente? |
| Momento da verdade | O que, se der errado, faz ele ir embora? |
| O que entregar | O que a empresa (ou comunidade, conteúdo, produto) entrega para resolver |
| Métrica | Como saber se a etapa funcionou (ligada ao cohort: % ativo, retenção no mês N, uso por cliente) |
| Responsável | Quem faz, quem aprova, quem é consultado, quem é informado (RACI) |
| Ciclo de vida | Assinou · Ativou · Usando · Em risco · Expande · Champion |

Marque em destaque a etapa onde a curva quebra (por exemplo, em laranja) e cite o número no subtítulo:
"Base de N clientes, vida média de X meses, o mês Y é onde a curva quebra".

Para preencher no script, use o campo `jornada` do config (ver `examples/config-exemplo.json`): a aba
**Jornada do Cliente** sai pronta para o time completar.

## 3. Fases de implantação (do aceite à passagem para o sucesso do cliente)
Quando o cohort mostra que muita gente sai cedo, o problema costuma estar entre a venda e o primeiro resultado.
Proponha fases com marco de saída claro:
| Fase | Período | O que acontece | Dono | Marco de saída |
|---|---|---|---|---|
| 1. Kickoff e passagem da venda | semana 0 | escopo, operador nomeado, acessos | implantação, com vendas | ata com escopo, dono e data de go-live |
| 2. Configuração | semanas 1 a 3 | montar, integrar, testar | implantação, com produto | primeiro teste funcionando |
| 3. Homologação com o cliente | semanas 3 a 4 | cliente testa e aprova | cliente e implantação | aprovação registrada |
| 4. Go-live | semana 4 | em produção, monitoria diária | implantação | 7 dias sem incidente crítico e 1º número medido |
| 5. Passagem para sucesso do cliente | semanas 5 a 6 | contexto, health score, cadência | sucesso do cliente | conta com dono, health score e reunião marcada |

Se as datas de go-live e de passagem não existem no CRM, diga isso: sem elas não dá para medir onde o cliente trava.
Sugira criar esses campos.

## Desenhar
Para virar quadro visual (Miro, FigJam), use a skill **ninja-fluxograma** com a jornada e as fases como entrada.
Para uma apresentação, leve: a curva de retenção, os caminhos, a jornada e 3 ações com dono e prazo.
