# Planilha de Growth — skill para Claude Code, Claude.ai e Codex

> Criado por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

Monta a **planilha central de growth da sua marca**, pronta para o time usar no dia a dia: tarefas, calendário
comercial, custo, preço e margem, concorrentes, influenciadores, conteúdo, anúncios, réguas de CRM, eventos e brindes.
Tudo com fórmulas, listas de opções e alertas, já preenchido com o que você contar.

Feita a partir de uma planilha real usada no lançamento de uma marca de e-commerce, transformada em método para
qualquer empresa.

## O que vem na planilha
| Aba | O que resolve |
|---|---|
| Tarefas | Plano de trabalho por frente, com prazo e responsável (fica vermelho quando atrasa) |
| Calendário | Feriados e datas comerciais do Brasil já calculados para o ano, com a ação de cada data |
| Custo do produto + Preço e margem | Preço mínimo, preço sugerido e a margem **com cupom** (fica vermelho se cair abaixo do mínimo) |
| Concorrentes | Preço por grama, ml ou unidade, diferenciais e promoções |
| Influenciadores | Do mapeamento ao retorno de cada parceria (receita com cupom ÷ custo) |
| Regras de parceria | UGC, influenciador, presente, afiliado; fluxos e níveis de comissão |
| Demandas de conteúdo | Fila de peças para design e conteúdo |
| Briefing de criativos | Pedidos de anúncio por objetivo, com 6 modelos prontos |
| Criativos | CTR, custo por conversão e ROAS de cada anúncio |
| Réguas de CRM | 22 réguas prontas (cadastral, transacional, relacional, promocional, datas) |
| Eventos e ativações | Orçamento por item e total por evento |
| Brindes e estoque | Estoque de envios com alerta e lista de espera de produtos esgotados |

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O passo a passo: entender a marca, escolher as abas, gerar, conferir e ensinar a usar |
| `scripts/montar_planilha.py` | Gera a planilha a partir de um arquivo de configuração |
| `references/` | Como funciona cada aba, preço e margem, influenciadores e criativos, réguas e calendário |
| `examples/` | Configuração e planilha de exemplo com uma marca fictícia |

## Antes de começar: checklist
- [ ] **Claude** (Claude Code, Cowork ou claude.ai com execução de código) — ou **Codex**.
- [ ] Python com `openpyxl` (`pip install -r requirements.txt`). O Claude instala se precisar.
- [ ] (Opcional) LibreOffice, para conferir as fórmulas antes de entregar.
- [ ] O que você já tiver: lista de produtos e custos, concorrentes, nomes do time, datas importantes.

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `planilha-de-growth/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/planilha-de-growth/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/planilha-de-growth/`.

Depois é só pedir: *"Monta a planilha de growth da minha marca de cosméticos, vamos lançar em março."*

## Licença e crédito
Criado por **Jaqueline Amaro**. Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0).
Para vender ou usar com clientes pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
