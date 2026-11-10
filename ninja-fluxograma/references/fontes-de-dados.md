# Fontes de dados

O processo comercial do cliente costuma estar espalhado. Use todas as fontes disponíveis e cruze: quando duas fontes
discordam (o playbook diz 5 etapas, o CRM tem 7), isso é um achado para o quadro.

## 1. Documentos
Playbook, deck, scripts de SDR, FAQ comercial, tabela de preços, transcrições de calls, prints de conversas.
- Leia tudo antes de desenhar. PDF longo: leia por partes.
- Formato que não abre (pptx antigo, áudio): peça em PDF ou texto.
- Transcrições: extraia perguntas, objeções e motivos de perda. Não copie nome, telefone ou e-mail de lead.

## 2. CRM (pipeline)
O que procurar:
| No CRM | Vira no quadro |
|---|---|
| Funis / pipelines | Um quadro (ou uma raia) por funil |
| Etapas do funil | Frames de etapa, na ordem |
| Campos obrigatórios por etapa | Formas de "atualizar campo" na etapa |
| Motivos de perda | Círculos de desqualificação |
| Automações / tarefas | Ações entre etapas |
| Responsáveis / distribuição | Transbordo para humano, regra de roteamento |

Como obter:
- **Conector do CRM** já ligado no Claude (HubSpot, Salesforce, Pipedrive, RD Station, monday etc.): leia pipelines,
  etapas, propriedades e motivos de perda. Só leitura.
- **Export** (CSV/XLSX) de negócios e da configuração do funil: peça para a pessoa exportar.
- **Prints** da configuração do funil também servem.
- Com export de negócios, calcule por etapa: volume, conversão para a próxima e tempo médio. Gargalo vira nota no quadro.

## 3. Agente de IA ou chatbot que já existe
- **Export JSON** da plataforma (fluxo, etapas, prompts, campos, ferramentas): é a melhor fonte.
- **API da plataforma**: só com a documentação pública da plataforma e um token de leitura que a pessoa fornece.
  Faça apenas leituras (GET). Guarde o token só em variável de ambiente da sessão, nunca em arquivo, quadro ou
  commit. Não use credencial de administrador nem acesso "em nome de" outro usuário.
- **Texto do prompt e das etapas** copiado da plataforma: também funciona.
Mapeie: cada etapa → frame; cada passo → forma; cada ferramenta (atualizar campo, mudar etapa, transferir,
encerrar, agenda, webhook) → forma de ação; cada condição → losango.

## 4. Descrição da pessoa
Sem material nenhum: use o questionário de `briefing.md`, ou entreviste em blocos curtos (como o lead chega → quais
perguntas são feitas → o que desqualifica → o que acontece com quem passa).

## Registro de fontes
No entregável, liste de onde veio cada parte ("etapas: CRM; perguntas: playbook p. 4; motivos de perda: CRM +
transcrições"). Ajuda o cliente a confiar no quadro e a saber o que atualizar depois.
