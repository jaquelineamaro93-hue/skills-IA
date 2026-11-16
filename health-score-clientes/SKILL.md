---
name: health-score-clientes
description: Monta um health score de clientes para qualquer negócio recorrente (SaaS, plataforma, escola, mentoria, serviço, e-commerce com assinatura). Começa por uma entrevista e um mapa dos sistemas que guardam os dados, depois define vetores, pesos e fases, calcula o score com um script simples, calibra com o histórico e deixa a rotina pronta para rodar automaticamente. Use quando alguém pedir health score, saúde de carteira, risco de churn, priorização de clientes, score de sucesso do cliente ou quiser automatizar essa leitura.
---

# Health score de clientes

## O que você entrega
Uma tabela com **uma linha por cliente**: fase da jornada, notas por vetor, score de 0 a 10, faixa (verde, amarelo ou vermelho) e o motivo em uma frase. Mais o caminho para rodar isso sozinho todo mês.

## Antes de começar: o que você precisa ter
- Acesso de leitura aos sistemas onde o cliente deixa rastro: plataforma (uso), cobrança, CRM, agenda, suporte ou planilha.
- Uma chave que ligue um cliente a todos esses sistemas (id da conta, e-mail, CNPJ ou id do CRM). Sem chave, não há score.
- Uma pessoa que conheça o negócio para responder a entrevista e revisar o resultado.
- Opcional: histórico de quem renovou e quem saiu, dos últimos 6 a 12 meses. Sem ele, o score fica sem calibração.

## Passo 1: entrevista (não pule)
Faça as perguntas de `references/entrevista.md`, em ordem. Anote as respostas antes de montar qualquer coisa. Principais:
1. Qual resultado concreto faz o cliente sentir que vale pagar? (esse é o vetor de valor)
2. Qual ação dentro do produto prova uso de verdade? Login sozinho não conta.
3. O que é autonomia para esse cliente? O que ele deveria conseguir fazer sem acionar o time?
4. Quais são as fases da jornada e quanto tempo cada uma dura?
5. Quem resolve o quê, e o que conta como pedido de ajuda do cliente?
6. Como um cliente que saiu aparece nos sistemas? Existe registro de cancelamento?

## Passo 2: mapa de sistemas
Use `references/sistemas.md`. Para cada vetor, responda: de onde vem o dado, qual é a chave de ligação e se o dado está saudável (com quantos meses de histórico e com que lacunas conhecidas). Documente as lacunas: elas explicam notas estranhas depois.

## Passo 3: vetores e pesos
Use `references/vetores-e-pesos.md`. Regra geral:
- Cada vetor tem **P1 (situação agora, 0 a 3)** e **P2 (profundidade ou tendência, 0 a 2)**. A nota do vetor vai de 0 a 5.
- Peso de 1 a 3, conforme a importância para a renovação. Até 6 vetores; mais que isso ninguém explica.
- Se um vetor não se aplica (ex.: não existe contato mapeado por cliente), deixe a nota **em branco**. O vetor sai do cálculo, numerador e denominador. Nunca preencha com zero.
- Fases podem mudar pesos. Cliente em implantação não deve ter o vetor de valor pesando contra ele.

## Passo 4: calcular
Preencha o CSV no formato de `examples/entrada_exemplo.csv` e rode:

```bash
python3 -I scripts/calcular_score.py entrada.csv saida.csv
```

O script aplica a fórmula: `score = soma(nota × peso) ÷ (soma dos pesos ativos ÷ 2)`, numa escala de 0 a 10. Faixa: risco explícito fica vermelho, independente do número; acima de 7,5 é verde; de 5 a 7,5 é amarelo; abaixo de 5 é vermelho.

Se a pessoa não tiver Python, a mesma conta funciona numa planilha: uma coluna por vetor, uma coluna de soma ponderada, e a faixa por fórmula.

## Passo 5: validar e calibrar
Não use a faixa para decidir atendimento antes de calibrar.
1. **Separação:** calcule o score de quem saiu e de quem renovou, alguns meses antes do desfecho. Se os dois grupos não se separam, ajuste pesos ou critérios e refaça.
2. **Paralelo com quem conhece o cliente:** por um ou dois ciclos, compare o score com a percepção do time. Quando discordarem, investigue antes de mudar o número.
3. **Notas com evidência:** cada nota precisa de um exemplo do que a justifica. Sem exemplo, cada pessoa interpreta de um jeito.

Detalhes em `references/calibracao.md`.

## Passo 6: rotina automática
Quando o score estiver calibrado, a rotina é:
1. Uma consulta (ou exportação) por sistema, com a chave de ligação.
2. O cálculo, com o script ou a planilha.
3. Gravar a foto do mês (cliente, fase, faixa, notas e desfecho em aberto) num histórico.
4. Enviar para o time só os vermelhos e os que caíram de faixa, com o motivo.

Pode rodar como tarefa agendada no Claude Code, numa automação do n8n, num notebook ou como agente. O que muda é onde ficam as consultas. A regra não muda: uma linha por cliente por mês, histórico nunca sobrescrito, e nenhuma ação automática sobre o cliente sem revisão humana.

## Regras que não mudam
- Somente leitura nos sistemas dos clientes.
- Dados pessoais no mínimo necessário. Não copie conteúdo de conversa, diário ou feedback para o score; use só contagens e datas.
- Nenhuma inferência psicológica sobre a pessoa a partir do score.
- Zero explicado pela fase não é punido. Ausência de dado vira "sem dado", nunca zero silencioso.

## Onde os passos vivem
| Arquivo | Quando usar |
|---|---|
| `references/entrevista.md` | Passo 1: perguntas para a pessoa que conhece o negócio |
| `references/sistemas.md` | Passo 2: que sistema guarda cada sinal, com chaves e lacunas comuns |
| `references/vetores-e-pesos.md` | Passo 3: vetores, pesos e fases, com dois exemplos de adaptação |
| `references/calibracao.md` | Passo 5: como validar antes de usar para decidir |
| `scripts/calcular_score.py` | Passo 4: cálculo sem dependências |
| `examples/entrada_exemplo.csv` | Modelo de entrada |
