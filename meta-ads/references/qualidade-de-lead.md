# Modo 4: qualidade do lead e CAC real

O Gerenciador mostra o custo por lead. O que paga as contas é o custo por **lead qualificado** e por **venda**. Uma campanha com lead barato e ninguém qualificado é a mais cara da conta.

## O que você precisa
1. **UTMs em todos os anúncios.** Modelo para colar no campo "Parâmetros de URL" do anúncio:
   ```
   utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}
   ```
   O CRM precisa guardar esses valores no lead (campo oculto no formulário, integração do formulário instantâneo ou automação do n8n).
2. **Critério de lead qualificado escrito.** Ex.: "tem empresa, fatura acima de R$ X e respondeu em até 48 h". Sem critério escrito, cada vendedor marca de um jeito.
3. **Exportação do CRM** com: a UTM (campanha, conjunto ou anúncio), qualificado (sim ou não) e valor da venda.

## Rodar
```bash
python3 -I scripts/cac_por_lead.py export.csv leads_crm.csv cac.csv --chave campanha
```
Use `--chave conjunto` ou `--chave anuncio` se a exportação do Gerenciador e as UTMs estiverem nesse nível. O nome no CRM precisa ser igual ao nome no Gerenciador (maiúsculas e acentos não importam).

## Leitura
| Sinal | O que significa | O que fazer |
|---|---|---|
| CPL baixo, custo por qualificado alto | Público ou formulário atrai curioso | Formulário com pergunta de filtro, oferta menos genérica, otimizar por lead qualificado via API de Conversões |
| Leads no Meta muito maior que leads no CRM | Integração perdendo lead ou duplicando no Meta | Conferir a integração antes de qualquer decisão de mídia |
| Linha "(sem utm)" grande | Parte dos leads não tem origem | Corrigir UTMs; até lá, o CAC por campanha está subestimado |
| Qualificado alto, venda baixa | Problema no comercial (tempo de resposta, abordagem), não na mídia | Medir tempo até o primeiro contato |
| Poucas vendas por campanha | Amostra pequena | Agrupar por período maior antes de cortar |

## Próximo nível
Enviar ao Meta o evento de **lead qualificado** e de **venda** pela API de Conversões (CAPI), para o algoritmo otimizar para quem compra, não para quem preenche. A skill `automacoes-n8n` deste repositório tem fluxos de Meta CAPI.

## Regra
Relatório com contagens e status. Não copie nome, telefone ou e-mail de lead para a análise.
