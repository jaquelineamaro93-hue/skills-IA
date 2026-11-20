---
name: agente-buscador-de-vagas
description: Monta um agente que busca vagas todo dia a partir do currículo da pessoa, filtra por cargo, senioridade, modelo, local, idioma e pisos salariais, dá uma nota de compatibilidade e acompanha a conversão (candidaturas, entrevistas e aprovações). Use quando alguém quiser buscar vagas com IA, montar um agente de recolocação, automatizar a busca de emprego, ou acompanhar o retorno das candidaturas. Funciona no ChatGPT, Claude, Gemini, Grok, OpenBot, Rerun ou Zapia.
---

# Agente buscador de vagas

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
