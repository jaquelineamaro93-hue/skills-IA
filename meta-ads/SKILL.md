---
name: meta-ads
description: Especialista em Meta Ads (Facebook e Instagram) em português, para negócios brasileiros. Monta o contexto da marca e o ICP, minera ângulos e ganchos em avaliações, comentários e anúncios de concorrentes, diagnostica campanhas (cortar, ajustar, manter ou escalar) a partir da exportação do Gerenciador, mostra o custo real por lead qualificado e por venda cruzando com o CRM, confere se o anúncio cumpre o que a página promete, escolhe canais com plano de 90 dias, monta campanha, conjuntos e textos e checa a política do Meta e as regras brasileiras antes de gastar. Use quando alguém pedir ajuda com anúncios no Meta, Facebook Ads, Instagram Ads, tráfego pago, criativos, CPA, ROAS, CAC ou desperdício de verba.
---

# Meta Ads

## O que você entrega
Depende do pedido, mas sempre em formato de decisão: uma tabela ou lista curta com **o que fazer, por quê e com que dado**. Nada de relatório que só descreve números.

## Antes de começar: o que você precisa ter
- **Contexto da marca** (produto, preço, margem, ICP, promessa). Se não existir, comece pelo Modo 1, que gera o `contexto-da-marca.md`. Todos os outros modos leem esse arquivo.
- **Para diagnosticar:** a exportação do Gerenciador de Anúncios em CSV, dos últimos 7 a 30 dias, com as colunas de `references/diagnostico.md`.
- **Para o custo real por lead:** uma exportação do CRM com a UTM de cada lead, se ele foi qualificado e o valor da venda.
- **Para ângulos:** avaliações, comentários, mensagens de clientes ou links públicos (Biblioteca de Anúncios do Meta, Reclame Aqui, Reddit, fóruns).
- Python 3 para os scripts. Sem Python, as mesmas contas cabem numa planilha (as regras estão nas referências).

Esta skill **não acessa a sua conta de anúncios** e não gasta nada. Ela trabalha com o que você exporta ou cola. Se houver um conector de Meta Ads ou de dados de mídia ligado à sessão, use-o só para leitura.

## Escolha o modo
| Pedido | Modo | Referência |
|---|---|---|
| "Pesquise minha marca", "monte o contexto", "quem é meu cliente" | 1. Contexto da marca e ICP | `references/contexto-da-marca.md` |
| "Ângulos que convertem", "ganchos", "o que os concorrentes anunciam", "tendências" | 2. Ângulos e ganchos | `references/angulos-e-ganchos.md` |
| "O que cortar ou escalar", "onde estou desperdiçando verba" | 3. Diagnóstico | `references/diagnostico.md` |
| "CAC real", "custo por lead qualificado", "o lead é ruim" | 4. Qualidade do lead | `references/qualidade-de-lead.md` |
| "O anúncio bate com a página?" | 5. Anúncio x página de destino | `references/pagina-de-destino.md` |
| "Por qual canal começo", "plano de 90 dias" | 6. Canais e plano | `references/plano-90-dias.md` |
| "Monte a campanha", "públicos e conjuntos", "escreva os textos" | 7. Montagem | `references/montagem-de-campanha.md` |
| "Isso passa na política?", antes de publicar | 8. Política e regras | `references/politica-meta.md` |
| "Transforme em criativos" | 9. Criativos | `references/criativos.md` |

Pedidos grandes ("monte meu tráfego do zero") seguem a ordem 1 → 2 → 6 → 7 → 8 → 9. Depois de 2 a 4 semanas no ar: 3 → 4 → 5.

## Modo 3 e Modo 4: os scripts
```bash
python3 -I scripts/diagnosticar_campanhas.py export.csv diagnostico.csv --cpa-alvo 80
```
```bash
python3 -I scripts/diagnosticar_campanhas.py export.csv diagnostico.csv --roas-alvo 3
```
```bash
python3 -I scripts/cac_por_lead.py export.csv leads_crm.csv cac.csv --chave campanha
```
Os scripts aceitam a exportação em português ou inglês, separada por vírgula ou ponto e vírgula, e ignoram a linha de total. Modelos em `examples/`.

Sem alvo informado, o diagnóstico usa a **mediana da conta** como referência e avisa. Diga isso na resposta: mediana não é meta de negócio. Para ter um alvo de verdade, calcule o CPA máximo com `references/diagnostico.md` (margem e LTV).

## Como responder
1. Comece pela decisão: o que cortar, o que escalar e quanto de verba isso libera.
2. Para cada item, o motivo em uma frase com o número que sustenta.
3. Separe **fato** (veio do dado) de **hipótese** (precisa de teste). Hipótese vem com o teste que a confirma.
4. Termine com até 3 próximos passos, em ordem.

## Regras que não mudam
- Somente leitura. Nunca pause, publique ou mude orçamento na conta. Quem aperta o botão é a pessoa.
- Não invente métrica, benchmark ou resultado de concorrente. Se não há dado, diga "sem dado" e sugira como obter.
- Benchmarks genéricos (CTR, CPM "bons") são só ponto de partida. A referência certa é a própria conta e a margem do negócio.
- Dados pessoais de leads: use só contagens e status. Não copie nome, telefone ou e-mail para relatórios (LGPD).
- Nenhum texto de anúncio sai sem passar pelo Modo 8.
- Nada de promessa que o produto não cumpre, de urgência falsa ou de depoimento inventado.

## Onde os passos vivem
| Arquivo | Quando usar |
|---|---|
| `references/contexto-da-marca.md` | Modo 1: entrevista e modelo do arquivo de contexto |
| `references/angulos-e-ganchos.md` | Modo 2: mineração de ângulos, ganchos e concorrentes |
| `references/diagnostico.md` | Modo 3: colunas, regras de decisão, CPA máximo e alertas |
| `references/qualidade-de-lead.md` | Modo 4: CAC real, UTMs e critério de lead qualificado |
| `references/pagina-de-destino.md` | Modo 5: checklist anúncio x página |
| `references/plano-90-dias.md` | Modo 6: escolha de canais e plano por fases |
| `references/montagem-de-campanha.md` | Modo 7: estrutura, públicos, nomes e textos |
| `references/politica-meta.md` | Modo 8: política do Meta e regras brasileiras |
| `references/criativos.md` | Modo 9: briefing e variações de criativo estático |
| `scripts/diagnosticar_campanhas.py` | Modo 3: classificação sem dependências |
| `scripts/cac_por_lead.py` | Modo 4: cruzamento gasto x CRM sem dependências |
| `examples/` | Modelos de exportação do Gerenciador e do CRM |
| `guia/central-de-midia.html` | Página para abrir no navegador: exemplo do resultado final, calculadora de CPA máximo, teste de campanha e caminho de integração em 7 etapas. Use para mostrar à pessoa como fica o resultado e o que integrar |
