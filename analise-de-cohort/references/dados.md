# Dados: o que pedir, onde achar e como preparar

## O mínimo
Uma tabela com **cliente, data e receita**. Uma linha por cliente por mês (assinatura) ou por pedido (e-commerce).

| cliente | data | receita |
|---|---|---|
| C001 | 2025-03-01 | 2500 |
| C001 | 2025-04-01 | 2500 |
| C002 | 2025-03-15 | 189,90 |

## Onde achar, por tipo de empresa
| Tipo | Onde está a receita por cliente | Onde estão canal / plano |
|---|---|---|
| SaaS / assinatura | sistema de cobrança (Stripe, Iugu, Vindi, Asaas, Pagar.me), ERP, planilha de MRR | CRM (HubSpot, Pipedrive, RD Station, Salesforce): campo de origem e plano |
| E-commerce | plataforma da loja (Shopify, Nuvemshop, VTEX, Tray), exportação de pedidos | UTM/origem do primeiro pedido, cupom usado, categoria comprada |
| Serviços / B2B | ERP ou planilha financeira (notas emitidas por cliente) | CRM |
| App / marketplace | banco de dados ou ferramenta de BI (consulta por cliente e mês) | atribuição de instalação, plano |

**Investimento de aquisição:** financeiro ou plataformas de anúncio (Meta, Google, TikTok), mais comissões de venda,
eventos e ferramentas de prospecção. Some por mês.

**Margem bruta:** financeiro (receita menos custo direto de entregar: produto, frete, servidor, atendimento).
Referências comuns: software 70 a 85%; e-commerce 20 a 50%; serviços 30 a 60%.

## Cuidados de preparação
- **Mesmo cliente, mesmo ID.** "ACME", "Acme Ltda" e "ACME S.A." viram um cliente só. Prefira CNPJ, e-mail ou ID do sistema.
- **Grade para lista.** Planilha com clientes nas linhas e meses nas colunas: transforme em uma linha por cliente x mês.
- **Meses futuros fora.** Contratos assinados para os próximos meses, propostas e negociações não são receita.
- **Pedidos cancelados ou devolvidos:** retire ou lance o valor negativo no mês do estorno; diga qual escolheu.
- **Contas de teste, internas ou gratuitas:** fora.
- **Clientes que pararam e voltaram:** ficam na safra original; contam como inativos nos meses sem receita.
- **Fontes que discordam** (cobrança diz 63 clientes, CRM diz 87 vendas): não junte em silêncio. Liste a diferença
  como limitação e pergunte qual é a fonte da verdade. Se precisar completar com outra fonte, marque quem veio de onde.
- **Anonimização:** se a planilha for sair do time, troque nomes por IDs.

## Perguntas para fazer à pessoa
1. Até que mês os dados são reais (fechados)?
2. Qual identificador de cliente é confiável?
3. Existe investimento de aquisição por mês? E a margem bruta?
4. Quais cortes importam: canal, plano, segmento, região, vendedor?
5. Algum cliente ou período que você já sabe que tem dado estranho?
