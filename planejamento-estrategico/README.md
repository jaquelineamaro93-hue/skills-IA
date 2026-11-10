# Planejamento Estratégico — skill para Claude Code, Claude.ai e Codex

> Método e skill criados por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

Ajuda qualquer liderança a **pensar estrategicamente e planejar a área**, do porquê até o OKR de cada pessoa do
time. Passo a passo, com perguntas que provocam, e no fim uma planilha pronta para acompanhar mês a mês.
Serve para CRM, CX, growth, marketing, produto, vendas ou operações.

## O caminho (8 passos)
| Passo | O que sai |
|---|---|
| 1. Casa da Estratégia | Missão e visão ligadas às da empresa, metas, enablers (processo, experiência, produto, pessoas) e fundamento |
| 2. Jornada de ponta a ponta | Etapas, canais, tarefas, dores, oportunidades, momentos da verdade e métricas |
| 3. Contexto do projeto | Dados, sistemas, partes interessadas, fora do escopo, integrações e entregáveis |
| 4. Fases e métricas | Fases do ciclo com métricas de INPUT (o time controla) separadas das de OUTPUT (resultado) |
| 5. Árvore de objetivos | Objetivo central → pilar de input e pilar de output → grupos com objetivos e KRs |
| 6. OKR da área | Objetivos e KRs com peso, alvo e acompanhamento mensal, com status automático |
| 7. OKR por pessoa | Peso de cada pessoa em cada KR, com o **peso esperado de cada pessoa** (muda de pessoa para pessoa e de área para área) |
| 8. IA como parceira de pensamento | Hipóteses, perguntas que o time ainda não faz, objeções e cenários "e se" |

## O que você precisa para fazer
- [ ] **Claude** (Claude Code, Cowork ou claude.ai com execução de código) — ou **Codex**.
- [ ] Python com `openpyxl` para gerar a planilha (`pip install -r requirements.txt`). O Claude instala se faltar.
- [ ] (Opcional) LibreOffice para conferir as fórmulas; Miro ou FigJam para desenhar a casa e a árvore.

**Informações** (não precisa ter tudo; a skill pergunta e propõe um ponto de partida):
- Missão e valores da empresa e o que a liderança espera da área neste ano.
- O time: pessoas, funções e quanto do tempo de cada uma é desta área.
- Os números de hoje (mesmo aproximados) e onde estão os dados.
- Materiais que já existam: apresentações, planilhas, quadros, pesquisas com clientes.

## O que vem na planilha
| Aba | Destaque |
|---|---|
| Casa da Estratégia | A casa montada, pronta para apresentar |
| Contexto | O quadro do projeto em 11 blocos |
| Jornada | Etapas x camadas, com momento da verdade |
| Fases e Métricas | INPUT x OUTPUT por fase |
| Árvore de Objetivos | Do objetivo central até os KRs de cada grupo |
| OKR da Área | Acompanhamento mensal; pega o último mês preenchido, compara com o alvo e pinta No alvo / Atenção / Fora; confere os pesos |
| OKR por Pessoa | Pesos por pessoa, comparados com o peso esperado de cada uma, e alerta de KR sem dono |
| Perguntas e Cenários | Hipóteses, perguntas, objeções, cenários e riscos |

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O passo a passo com as perguntas de cada etapa |
| `references/` | Casa da Estratégia, jornada e contexto, fases e métricas, árvore e OKRs, IA como parceira |
| `scripts/montar_planejamento.py` | Gera a planilha a partir do que foi construído |
| `examples/` | Exemplo completo de uma área de CRM de uma rede fictícia (configuração e planilha) |

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `planejamento-estrategico/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/planejamento-estrategico/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/planejamento-estrategico/`.

Depois é só pedir: *"Me ajuda a planejar a área de CX para o ano que vem"* ou *"Desdobra os OKRs do meu time por pessoa"*.

## Licença e crédito
Método e skill de **Jaqueline Amaro**. Casa da Estratégia (Strategy House): modelo de origem no Sistema Toyota.
Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0). Para vender ou usar com clientes
pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
