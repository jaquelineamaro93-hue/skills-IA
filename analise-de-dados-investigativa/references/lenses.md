# As 6 Lentes Analiticas — Detalhamento

Para cada lente: conceito, tecnica passo a passo, pergunta-chave, mini-case pratico e armadilhas a evitar.

---

## Lente 1: Deteccao de Sinais Fracos

**Conceito:** Padroes pequenos que se repetem de forma consistente mas que seriam ignorados por ter baixo volume. O sinal fraco de hoje pode ser a tendencia dominante de amanha.

**Tecnica passo a passo:**
1. Segmente os dados por todas as variaveis categoricas disponiveis
2. Para cada segmento, calcule a metrica-alvo (conversao, satisfacao, ticket medio)
3. Ordene por performance relativa — nao por volume
4. Identifique segmentos com performance 2x+ acima ou abaixo do grupo geral
5. Verifique se o padrao se mantem ao longo do tempo (nao e pontual)

**Pergunta-chave:** *Existe alguma subpopulacao nos dados que esta performando de forma radicalmente diferente do grupo maior?*

**Mini-case:** Em uma planilha com 2000 leads, o canal "indicacao" representa apenas 45 leads (2.2%) mas tem taxa de conversao de 38% vs. 8% do total. Uma analise convencional focaria nos canais de maior volume (Google Ads com 800 leads). A Lente 1 identifica que "indicacao" e o canal mais eficiente e sugere investigar como escalar.

**Armadilhas:**
- Segmentos com N < 10 podem gerar falsos positivos. Sinalize sempre o tamanho da amostra.
- Performance extrema em um unico periodo pode ser outlier temporal, nao padrao real. Verifique consistencia ao longo do tempo.

---

## Lente 2: Analise de Inversao

**Conceito:** Casos que vao contra o padrao esperado — outliers que "nao deveriam" ter dado certo (ou errado). Esses casos frequentemente revelam processos ocultos que podem ser replicados ou corrigidos.

**Tecnica passo a passo:**
1. Identifique o padrao geral (ex: leads de canal X convertem Y%)
2. Encontre os casos que contradizem o padrao:
   - Leads "ruins" (score baixo, canal fraco) que converteram
   - Campanhas de baixo custo com clientes de alto valor
   - Atendimentos longos com alta satisfacao (ou curtos com churn)
3. Agrupe os casos invertidos e procure o que eles tem em comum
4. Formule a hipotese: qual variavel oculta explica a inversao?

**Pergunta-chave:** *Quem "nao deveria" ter dado certo mas deu? O que esses casos tem em comum?*

**Mini-case:** Em dados de atendimento, 12 chamados marcados como "reclamacao grave" (tipicamente churn) resultaram em upgrade do plano. Investigando: todos tiveram atendimento pela operadora Maria, que usa empatia + oferta proativa. O achado nao e "reclamacao e boa" — e que existe um processo de recuperacao que funciona e pode ser replicado.

**Armadilhas:**
- Nao confunda inversao com erro de dados. Verifique se os valores sao reais antes de interpretar.
- Inversoes com N muito baixo (2-3 casos) sao anedotas, nao padroes. Precisam de mais dados para validar.

---

## Lente 3: Analise Temporal de Segunda Ordem

**Conceito:** Nao a tendencia em si, mas a aceleracao ou desaceleracao da tendencia. E defasagens (lags) entre eventos.

**Tecnica passo a passo:**
1. Calcule a taxa de variacao periodo a periodo (derivada primeira)
2. Calcule a aceleracao: a taxa de variacao esta crescendo ou diminuindo? (derivada segunda)
3. Procure pontos de inflexao — onde a aceleracao muda de sinal
4. Busque defasagens: um evento no periodo T correlaciona com resultado no periodo T+N?
5. Identifique leading indicators: metricas que se movem antes do resultado final

**Pergunta-chave:** *O que esta mudando de velocidade, nao apenas de direcao?*

**Mini-case:** Conversoes mensais: Jan=100, Fev=105, Mar=112, Abr=121, Mai=133. Analise simples: "crescimento estavel de ~8%". A Lente 3 mostra que a taxa esta acelerando (5-7-9-12) — algo esta funcionando cada vez melhor e merece ser identificado antes que o efeito se estabilize.

**Outro exemplo (lag):** Aumento de reclamacoes no suporte precede queda de conversao em 2 semanas. As reclamacoes sao um leading indicator — monitorar reclamacoes permite agir antes da queda.

**Armadilhas:**
- Aceleracao com poucos pontos de dados e muito ruidosa. Precisa de pelo menos 5-6 periodos para ser confiavel.
- Cuidado com sazonalidade: uma "aceleracao" pode ser simplesmente o padrao sazonal normal (ex: Black Friday).

---

## Lente 4: Correlacao Quali-Quanti Cruzada

**Conceito:** Conexoes entre dados textuais (conversas, feedbacks, respostas abertas) e resultados numericos. Onde a linguagem encontra o resultado.

**Tecnica passo a passo:**
1. Separe os casos em dois grupos: sucesso vs. fracasso (pela metrica-alvo)
2. Para cada grupo, extraia os termos/expressoes mais frequentes
3. Identifique termos que aparecem significativamente mais em um grupo que no outro
4. Se possivel, use contagem simples ou TF-IDF para quantificar
5. Analise tom/sentimento e cruze com desfechos
6. Procure "palavras-gatilho" que precedem acoes importantes

**Pergunta-chave:** *Que palavras ou temas aparecem nos casos de sucesso mas nao nos de fracasso?*

**Mini-case:** Em 500 conversas de vendas, leads que usaram "urgente" ou "prazo" nos primeiros 3 turnos tiveram conversao 2.3x maior. Hipotese: leads com necessidade imediata convertem mais rapido. Acao: priorizar esses leads e reduzir tempo de resposta para <5min.

**Armadilhas:**
- Palavras frequentes em ambos os grupos (artigos, saudacoes) geram ruido. Foque nas diferencas, nao nas frequencias absolutas.
- Sentimento negativo nem sempre e ruim. "Estou insatisfeito com meu provedor atual" pode ser sinal de compra.

---

## Lente 5: Analise de Proporcoes vs. Absolutos

**Conceito:** Oportunidades ocultas nos denominadores. Muitas analises erram ao olhar apenas volumes absolutos. A normalizacao muda a historia.

**Tecnica passo a passo:**
1. Para cada metrica-chave, crie a versao normalizada:
   - Custo por lead qualificado (nao so por lead)
   - Taxa de conversao por canal (nao so volume)
   - Tempo medio por tipo de solicitacao (nao so por atendente)
   - Receita por cliente ativo (nao so receita total)
2. Compare o ranking por volume vs. ranking por taxa
3. Onde o ranking muda drasticamente, ha um insight

**Pergunta-chave:** *Se eu normalizar essa metrica, a historia muda?*

**Mini-case:** Canal A: 500 leads a R$10/lead (R$5.000 investidos). Canal B: 80 leads a R$25/lead (R$2.000). Por volume, A ganha. Mas A converte 2% (10 clientes, R$500/cliente) e B converte 15% (12 clientes, R$167/cliente). Canal B traz mais clientes por menos custo total. A decisao de investimento muda completamente.

**Armadilhas:**
- Taxas com denominadores pequenos flutuam muito. Uma taxa de 50% com N=2 nao e confiavel.
- Sempre apresente taxa E volume juntos para dar contexto completo.

---

## Lente 6: Mapeamento de Lacunas

**Conceito:** O que deveria estar nos dados mas nao esta. A ausencia e o dado. Lacunas revelam oportunidades inexploradas ou problemas de cobertura.

**Tecnica passo a passo:**
1. Crie uma matriz de todas as combinacoes esperadas (segmento x canal, hora x dia, produto x regiao)
2. Identifique celulas com zero ocorrencias
3. Para cada lacuna, investigue: e ausencia real ou falha de registro?
4. Verifique se ha demanda reprimida adjacente (a celula vizinha tem pico?)
5. Classifique: oportunidade inexplorada, problema de cobertura, ou irrelevante

**Pergunta-chave:** *Que segmento, horario, pergunta ou cruzamento tem zero registros — e por que?*

**Mini-case:** Heatmap de atendimentos por hora x dia: domingo 10h-14h tem zero registros, mas segunda 8h tem pico de 3x a media. Hipotese: demanda reprimida do domingo explode na segunda. Acao: testar atendimento dominical para distribuir a carga.

**Armadilhas:**
- Nem toda lacuna e oportunidade. Alguns cruzamentos simplesmente nao fazem sentido.
- Lacunas em dados de registro podem significar falha de sistema, nao ausencia de eventos reais. Investigue a causa antes de concluir.
