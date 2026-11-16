# Mapa de sistemas: o que conectar e por quê

Para cada sinal, anote o sistema, a chave de ligação e a lacuna conhecida. Nem todo negócio tem todos os sistemas. Use só o que existir.

## Sinais e onde eles costumam estar

| Sinal | Onde costuma estar | Chave de ligação | Lacuna comum |
|---|---|---|---|
| Uso do produto (ações, dias ativos) | Ferramenta de analytics de produto, banco da plataforma, logs | id da conta ou do usuário | Eventos sem id do cliente; login sem ação real |
| Assinatura e cobrança (status, data de fim, atraso) | Gateway de pagamento, banco da plataforma, ERP | id do cliente no gateway, CPF/CNPJ | Assinatura cancelada que continua ativa no cadastro |
| Contrato e licenças (quantidade, validade) | Sistema de contratos, banco, planilha | CNPJ, id do contrato | Contratos em papel ou PDF sem data estruturada |
| Agenda e aulas (agendamentos, presença) | Agenda (Google Calendar, Calendly), plataforma de aulas | e-mail do participante, id do aluno | Presença não verificada; agendamento sem comparecimento |
| Suporte (tickets, tempo de resposta, reclamações) | Help desk, chat, WhatsApp | e-mail, telefone, id do cliente | Conversas em canal que ninguém registra |
| Relacionamento (responsável, reuniões, último contato) | CRM | id do cliente no CRM, domínio do e-mail | Campo de responsável vazio |
| Satisfação (NPS, pesquisa de uso) | Ferramenta de pesquisa | e-mail | Respostas anônimas, sem como ligar ao cliente |
| Engajamento de conteúdo (cursos, trilhas) | Plataforma de cursos ou LMS | id do aluno | Progresso sem data de conclusão |
| Volume de conversa com IA ou atendimento | Ferramenta de IA, chatbot | id do usuário | Conversa sem id; histórico que expira |

## Dez perguntas para o mapa
1. Este sinal existe hoje em algum sistema? Se não, ele sai do score.
2. Onde ele fica e quem tem acesso?
3. Qual chave liga esse dado ao cliente? Essa chave é a mesma em todos os sistemas?
4. Quanto histórico existe? (Mês a mês é o mínimo para tendência.)
5. Há cliente sem essa chave? Quantos?
6. O dado é atualizado com que frequência?
7. Quem pode ler sem ferir privacidade? (Conteúdo de conversa e diário costumam ficar fora.)
8. Há registro de saída (cancelamento, não renovação)?
9. O dado mudou de sistema recentemente? Quando?
10. Qual é a lacuna que mais vai confundir a leitura?

## Ordem de conexão recomendada
1. Chave de ligação e lista de clientes ativos (sem isso, nada se junta).
2. Status de cobrança e data de fim de acesso.
3. Uso do produto por cliente, em janelas de 14 e 28 dias.
4. Entregas ou resultados (o que o cliente produziu ou conquistou).
5. Relação com a equipe (reuniões, pedidos de ajuda, responsável).
6. Histórico de saídas, para calibrar.

Conecte um sistema por vez e valide a chave com 10 clientes antes de seguir.
