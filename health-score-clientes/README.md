# Health score de clientes

Monta um health score para qualquer negócio recorrente: plataforma, escola, mentoria, serviço ou assinatura. Começa pela entrevista e pelo mapa de sistemas, depois calcula o score e deixa a rotina pronta para rodar sozinha.

## Checklist: o que você precisa antes de começar
- [ ] Uma pessoa que conheça o negócio e o produto, para responder a entrevista (`references/entrevista.md`)
- [ ] Acesso de leitura aos sistemas onde o cliente deixa rastro: uso, cobrança, contrato, agenda, suporte ou relacionamento
- [ ] Uma chave que ligue um cliente a todos esses sistemas (id da conta, e-mail, CNPJ ou id do CRM)
- [ ] Histórico de quem renovou e quem saiu, dos últimos 6 a 12 meses (opcional, mas necessário para calibrar)
- [ ] Python 3 instalado, ou uma planilha (a fórmula está no `SKILL.md`)

## Como usar
1. Responda a entrevista e anote as respostas.
2. Preencha o mapa de sistemas com `references/sistemas.md`.
3. Defina vetores e pesos com `references/vetores-e-pesos.md`.
4. Preencha um CSV no formato de `examples/entrada_exemplo.csv` e rode:

```bash
python3 -I scripts/calcular_score.py entrada.csv saida.csv
```

5. Valide com `references/calibracao.md` antes de usar a faixa para decidir.

## Onde rodar
A skill é só texto e um script de Python sem dependências. Funciona no Claude Code, no Codex, em qualquer notebook ou como tarefa agendada, desde que o agente consiga ler os sistemas listados no mapa.

## Licença
CC BY-NC 4.0, com crédito à autora. Uso comercial mediante autorização. Veja `LICENSE.md`.
