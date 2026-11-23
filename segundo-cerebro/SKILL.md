---
name: segundo-cerebro
description: Monta e mantém um segundo cérebro pessoal ou de negócio: captura o que você aprende (transcrições, notas, links, decisões), organiza por tema e fonte, consulta antes de decidir e gera um índice para nada se perder. Use quando alguém quiser uma central de conhecimento, organizar palestras e aulas, guardar decisões, criar uma base que a IA consulta, ou não perder o que já foi aprendido.
---

# Segundo cérebro

## O que você entrega
Uma central de conhecimento com três partes:
1. **Fichas**: uma por fonte ou ideia (palestra, aula, livro, post, decisão, método), com tema, data, fonte e o que foi aprendido.
2. **Índice**: uma lista única que mostra tudo o que existe, gerada a partir das fichas e das skills.
3. **Rotina**: uma revisão curta todo mês para manter o índice vivo e arquivar o que ficou velho.

## Como começar (para qualquer nível)
Em uma conversa só:
1. Diga: "Vamos organizar o que você já sabe num lugar só, para a IA consultar e você não perder nada."
2. Peça um texto livre: "Me conta em um parágrafo: sua área, os temas que mais estuda, onde guarda suas coisas hoje (pastas, apps, caderno) e o que mais te incomoda perder."
3. Monte a estrutura de `references/estrutura.md` com os temas que aparecerem, e entregue o modelo de ficha de `references/ficha-modelo.md`.
4. Mostre como colocar a primeira ficha: escolha uma fonte que você já tem (uma transcrição, uma nota) e preencha a ficha junto.
5. Gere o índice com `scripts/gerar_indice.py` e mostre o resultado.
6. Feche com a rotina: uma revisão por mês, com três perguntas: o que aprendi de novo, o que virou decisão, o que já não vale.

Pronto quando: a pessoa tem pelo menos uma ficha preenchida, o índice gerado e a rotina marcada.

## Quatro movimentos
- **Capturar:** cole a transcrição, a nota ou o link. Não precisa ser perfeito: depois a ficha organiza.
- **Organizar:** cada ficha tem tema, fonte, data e nível de confiança (fonte primária, comentário, opinião).
- **Consultar:** antes de decidir preço, oferta, conteúdo ou prioridade, peça para a IA buscar nas fichas o que já foi dito sobre o assunto, citando a fonte.
- **Manter:** o índice é gerado de novo todo mês. O que não é mais usado vai para `arquivo/`, nunca some.

## Regras que não mudam
- **Toda resposta cita a fonte** (ficha, data, autor). Sem fonte, é opinião, e a IA deve dizer isso.
- **Não invente conteúdo** de uma fonte que não está nas fichas.
- **Separe o público do privado.** Fichas com dados de pessoas (mentorados, clientes, alunos), contratos, senhas ou materiais confidenciais vão para um repositório privado, nunca para o público.
- **Permissão de terceiros.** Só guarde transcrição ou material de outra pessoa se ela autorizou ou se é público.
- **Não cole chave, senha ou código** de verificação em nenhuma ficha.

## Onde os passos vivem
| Arquivo | Quando usar |
|---|---|
| `references/estrutura.md` | Montar as pastas e os temas |
| `references/ficha-modelo.md` | Preencher cada ficha |
| `scripts/gerar_indice.py` | Gerar o índice a partir das fichas e das skills |
