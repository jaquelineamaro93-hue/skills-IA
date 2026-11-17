# Meta Ads

Especialista em anúncios no Facebook e no Instagram, em português e para o mercado brasileiro. Nove modos num só lugar: contexto da marca e ICP, ângulos e ganchos, diagnóstico de campanhas, custo real por lead qualificado, anúncio x página de destino, escolha de canais com plano de 90 dias, montagem de campanha, checagem de política e briefing de criativos.

Não acessa a sua conta de anúncios e não gasta créditos: trabalha com o que você exporta do Gerenciador e do CRM, ou cola na conversa.

## Checklist: o que você precisa antes de começar
- [ ] Informações do negócio: produto, preço, margem e quem é o cliente ideal (a skill faz a entrevista)
- [ ] Para diagnosticar: exportação CSV do Gerenciador de Anúncios, últimos 7 a 30 dias
- [ ] Para o custo real por lead: exportação do CRM com a UTM de cada lead, se foi qualificado e o valor da venda
- [ ] Para ângulos: avaliações, comentários e mensagens de clientes, ou links públicos (Biblioteca de Anúncios, Reclame Aqui)
- [ ] Python 3 instalado para os scripts, ou uma planilha (as regras estão nas referências)

## Como usar
Peça em linguagem normal, por exemplo:
- "Monte o contexto da minha marca para anúncios"
- "Ache os ângulos que convertem nessas avaliações"
- "Diagnostique minhas campanhas: o que cortar, manter ou escalar" (anexe o CSV)
- "Qual o custo real por lead qualificado?" (anexe o CSV do Gerenciador e o do CRM)
- "Esse anúncio passa na política do Meta?"

Os scripts também rodam sozinhos:
```bash
python3 -I scripts/diagnosticar_campanhas.py examples/export_exemplo.csv diagnostico.csv --roas-alvo 3
```
```bash
python3 -I scripts/cac_por_lead.py examples/export_exemplo.csv examples/leads_crm_exemplo.csv cac.csv
```

## Instalação no Claude Code
Copie a pasta `meta-ads` para `~/.claude/skills/` (para todos os projetos) ou para `.claude/skills/` dentro do projeto.

## Licença
CC BY-NC 4.0, com crédito à autora. Uso comercial mediante autorização. Veja `LICENSE.md`.
