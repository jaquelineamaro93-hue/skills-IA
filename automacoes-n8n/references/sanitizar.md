# Limpar um fluxo do n8n antes de compartilhar ou vender

## Rodar o script
```
python3 scripts/sanitizar_n8n.py fluxo.json fluxo-limpo.json --nomes nomes.txt --relatorio relatorio.txt
python3 scripts/sanitizar_n8n.py --pasta fluxos/ fluxos-limpos/ --nomes nomes.txt --relatorio relatorio.txt
```
`nomes.txt` (uma troca por linha; troca em todo o fluxo, inclusive nomes de nós e referências a eles):
```
# Nome real => Substituto
Nome do Cliente => Sua Empresa
Fulana => Conta B
```

## O que o script faz sozinho
| Item | Vira |
|---|---|
| Dados de teste salvos (pinData), staticData, ID da instalação, ID e versão do fluxo | removidos |
| Credenciais (ID e nome) | `SUA_CREDENCIAL_ID` e `[Reconfigurar] <nome>` |
| webhookId e caminhos de webhook com cara de ID | `SEU_WEBHOOK_ID` / `SEU_WEBHOOK_PATH` |
| URLs de webhook da sua instalação | `https://SUA_URL_N8N/webhook/SEU_WEBHOOK_PATH` |
| Fluxo de erro (errorWorkflow) | `SEU_ID_WORKFLOW_DE_ERRO` |
| E-mails reais | `email@exemplo.com` (mantém endereços de sistema, como `postmaster@msging.net`) |
| Telefones | `5511999999999` |
| IPs | `0.0.0.0` |
| Tokens longos (fora de fórmulas) | `SEU_TOKEN_AQUI` |
| IDs de conta com 5+ dígitos (funil, campo, pixel, contato) e identificadores únicos (UUID) em valores | `SEU_ID_AQUI` |
| IDs de 6+ dígitos dentro de códigos | `0 /* SEU_ID_AQUI */` (o código continua válido) |
| ID e aba de planilhas Google; esquema de colunas cacheado | `SEU_ID_DA_PLANILHA_GOOGLE`, `SEU_GID_DA_ABA`; esquema apagado |
| Fluxo ativo | desligado |

No fim ele refaz a busca e lista em **"Para revisar"** o que ainda precisa de olho humano.

## Conferências depois do script
1. **Códigos válidos:** extraia cada `jsCode` e rode `node --check` (ou abra o fluxo no n8n e veja se algum nó de
   código acusa erro).
2. **Ligações:** toda chave de `connections` e todo `$('Nome do nó')` precisa apontar para um nó que existe.
3. **Revisão humana (o script não pega tudo):**
   - nomes de pessoas, empresas, clientes, produtos e eventos em nomes de nós, notas, mensagens e perguntas de formulário;
   - nomes de canais do Slack, listas, tags, etapas de funil e campos personalizados que revelem o cliente;
   - textos de mensagens de WhatsApp ou e-mail com dados reais;
   - links para documentos, planilhas, vídeos ou páginas internas.
4. **Tokens que já circularam:** trocar por texto de exemplo não invalida a chave. Gere uma nova na ferramenta e
   revogue a antiga.

## Dica de busca rápida
Procure no JSON por: `@`, `http`, `Bearer`, `token`, `key`, `secret`, `senha`, sequências longas de números e
palavras com inicial maiúscula que não sejam nomes de ferramentas.
