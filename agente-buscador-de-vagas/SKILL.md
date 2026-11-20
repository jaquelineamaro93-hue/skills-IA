---
name: agente-buscador-de-vagas
description: Monta um agente que busca vagas todo dia a partir do currículo da pessoa, filtra por cargo, senioridade, modelo, local, idioma e pisos salariais, dá uma nota de compatibilidade e acompanha a conversão (candidaturas, entrevistas e aprovações). Use quando alguém quiser buscar vagas com IA, montar um agente de recolocação, automatizar a busca de emprego, ou acompanhar o retorno das candidaturas. Funciona no ChatGPT, Claude, Gemini, Grok, OpenBot, Rerun ou Zapia.
---

# Agente buscador de vagas

## Como começar (faça isto antes de qualquer texto)
Quando a pessoa pedir para montar o agente, atue como um **construtor guiado**: não mande os textos de cara. Siga estas etapas, uma de cada vez, e espere a resposta antes de avançar.

**Etapa 0: o que você vai construir.** Diga em duas frases: "Vamos montar um agente que busca vagas todo dia, filtra pelo seu perfil e acompanha as candidaturas. São quatro passos e um teste. Leva cerca de 30 minutos."

**Etapa 1: o que você precisa ter.** Confira item por item, perguntando:
1. Você tem o currículo em PDF atualizado? Se não, ajudamos a atualizar antes.
2. Qual ferramenta você vai usar? (ChatGPT, Claude, Gemini, Grok, OpenBot, Rerun ou Zapia.) Confirme que ela tem busca na web e tarefas agendadas. Se não tiver, sugira outra.
3. Você tem uma planilha para as candidaturas? Se não, crie uma com as colunas de `references/acompanhamento.md`.
4. Quer usar pisos salariais de CLT e PJ? Se sim, peça os valores.

Se algum item faltar, pare aqui e resolva antes de seguir.

**Etapa 2: os seus critérios.** Pergunte, uma de cada vez: cargos que quer, senioridade (ex.: coordenação, gerência, especialista), modelo (remoto, híbrido ou presencial), cidade e região, idioma (inglês fluente é um filtro?), o que **não** quer, e a porcentagem mínima de match para receber a vaga. Só monte os textos depois de ter essas respostas.

**Etapa 3: os textos.** Gere os quatro passos de `references/passos-prontos.md` com os critérios preenchidos. Entregue um por vez.

**Etapa 4: guie cada passo.** Para cada passo: diga o que fazer, peça para colar o texto, e espere a pessoa contar o que apareceu. Se a resposta não bater com o esperado (sem link, sem match, lista repetida), ajude a corrigir antes de seguir.

**Etapa 5: teste de ponta a ponta.** Antes de agendar, peça uma rodada manual (sem agendar). Confira com a pessoa:
- as vagas têm link que abre;
- nenhuma vaga está repetida;
- cada vaga tem match e pontos de conexão;
- vagas sem salário não foram descartadas;
- a planilha recebeu o primeiro registro (ou a instrução de como registrar).

Se os cinco itens passarem, siga para o agendamento. Se algum falhar, ajuste e teste de novo.

**Etapa 6: agendar.** Só agora peça para agendar a rotina no horário escolhido, com o passo 3. Confirme que a primeira execução agendada foi criada.

**Critério de pronto.** O agente está pronto quando: o teste manual passou nos cinco itens, o agendamento existe, e a pessoa sabe onde registrar as candidaturas e quando revisar a conversão (a cada semana). Diga isso explicitamente no fim e pergunte se ficou algo sem resposta.

## O que você entrega
Um agente que, todo dia no horário escolhido:
1. busca até 30 vagas novas, alinhadas ao currículo da pessoa;
2. exclui as que já estavam na lista anterior, inclusive republicações;
3. dá para cada vaga um link, os pontos de conexão com a trajetória e uma porcentagem estimada de match;
4. mantém o acompanhamento da conversão: quantas candidaturas viraram entrevista e quantas entrevistas viraram aprovação, por tipo de vaga.

Para quem quer o caminho mais rápido, o método cabe em **três mensagens**. O quarto passo é o de acompanhamento.

## Antes de começar
- [ ] Currículo atualizado em PDF, com cargos, datas, resultados com números e ferramentas.
- [ ] Os seus critérios: cargos, senioridade, modelo (remoto, híbrido ou presencial), cidade e região, idioma e o que você **não** quer.
- [ ] Pisos salariais por contrato (CLT e PJ), se quiser que o agente use o filtro. Vagas sem salário divulgado não são descartadas.
- [ ] Uma IA com busca na web e tarefas agendadas (ChatGPT, Claude, Gemini, Grok, OpenBot, Rerun ou Zapia).
- [ ] Uma planilha para registrar as candidaturas, com as colunas de `references/acompanhamento.md`.

## Passo 1: o currículo vira cargos
Anexe o currículo e peça que a IA atue como headhunter e liste os cinco cargos mais alinhados à experiência. Peça também as perguntas que faltam para refinar a busca. Responda as perguntas antes de seguir.

Texto pronto: `references/passos-prontos.md`, passo 1.

## Passo 2: refinar com os seus critérios
Na mesma conversa, peça a busca com os seus pisos, exclusões e porcentagem mínima de match. Para cada vaga, peça o link, os pontos de conexão e o match estimado. Confira o link antes de se candidatar: a IA às vezes erra a data ou mistura vagas.

Texto pronto: `references/passos-prontos.md`, passo 2.

## Passo 3: agendar a rotina
Use a tarefa agendada da ferramenta e peça a repetição diária, com a regra de não repetir. Essa é a parte que faz o agente valer a pena: a lista de cada dia só mostra o que é novo.

Texto pronto: `references/passos-prontos.md`, passo 3.

## Passo 4: acompanhar a conversão
A cada semana, peça a leitura dos dados. Com algumas semanas, dá para ver em quais tipos de vaga a pessoa tem retorno e ajustar a busca. Peça um resumo de uma página quando a resposta vier grande.

Texto pronto: `references/passos-prontos.md`, passo 4. Planilha e colunas: `references/acompanhamento.md`.

## Regras que não mudam
- **Nunca repita vaga**: exclua o que já estava na lista anterior, incluindo republicações.
- **Nunca invente**: vaga, data, salário, empresa ou requisito. Se não estiver no anúncio, diga que não está.
- **Vaga sem salário não é descartada.** O filtro de piso só vale quando o salário é divulgado.
- **Confirme antes de se candidatar**: abra o link original e veja se a vaga ainda está aberta.
- **Quem candidata e quem responde é a pessoa.** O agente prepara; não envia candidatura nem mensagem a recrutador sem aprovação.
- **Dados pessoais no mínimo**: não cole CPF, endereço, senha nem código de verificação na conversa.

## Quando a tarefa não basta
Se a busca precisar cruzar mais de uma fonte e explicar o motivo de cada escolha, use um agente em vez de uma tarefa simples. O formato da mensagem continua o mesmo. O que muda é a ferramenta: agentes com conectores (e-mail, planilha, calendário) fazem o acompanhamento sozinhos, com aprovação antes de cada envio.

## Onde os passos vivem
| Arquivo | Quando usar |
|---|---|
| `references/passos-prontos.md` | Os textos dos quatro passos, para copiar |
| `references/acompanhamento.md` | Planilha de candidaturas e indicadores de conversão |
| `examples/resumo-diario.md` | Exemplo de resumo que o agente devolve todo dia |
