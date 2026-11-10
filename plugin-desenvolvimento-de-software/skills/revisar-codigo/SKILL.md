---
name: revisar-codigo
description: Revisa mudanças de código procurando falhas de segurança, lentidão e erros. Use com o link de um PR ou um diff, "revisa isso antes de eu juntar", "esse código é seguro?", "code review", ou para checar uma mudança atrás de consultas N+1, risco de injeção, casos esquecidos ou falta de tratamento de erro.
argument-hint: "<link do PR, diff ou caminho do arquivo>"
---

# Revisar código

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Revisa mudanças de código olhando segurança, desempenho, se está correto e se é fácil de manter.

## Como usar

```
/desenvolvimento-de-software:revisar-codigo <link do PR ou caminho do arquivo>
```

Revise as mudanças informadas: @$1

Se nenhum arquivo ou link for informado, pergunte o que revisar.

## Como funciona

```
SEMPRE FUNCIONA
  ✓ Cole um diff, o link do PR ou aponte os arquivos
  ✓ Segurança (OWASP top 10, injeção, autenticação)
  ✓ Desempenho (N+1, vazamento de memória, complexidade)
  ✓ Correção (casos extremos, tratamento de erro, concorrência)
  ✓ Estilo (nomes, estrutura, leitura)
  ✓ Sugestões práticas com exemplo de código

MELHOR COM AS SUAS FERRAMENTAS
  + Repositório de código: puxa o diff do PR sozinho
  + Gestão de tarefas: liga os achados às tarefas
  + Base de conhecimento: confere com o padrão de código do time
```

## O que olhar

### Segurança
- Injeção de SQL, XSS, CSRF
- Falhas de autenticação e de permissão
- Senhas ou chaves no código
- Desserialização insegura
- Acesso a caminhos de arquivo indevidos (path traversal)
- SSRF

### Desempenho
- Consultas N+1
- Uso de memória desnecessário
- Complexidade alta (O(n²) em trechos muito usados)
- Índices faltando no banco de dados
- Consultas ou laços sem limite
- Recursos que não são liberados

### Correção
- Casos extremos (entrada vazia, nulo, estouro)
- Concorrência e condições de corrida
- Tratamento e repasse de erros
- Erros de "um a mais / um a menos"
- Tipos

### Manutenção
- Nomes claros
- Cada parte com uma responsabilidade
- Duplicação
- Cobertura de testes
- Comentários no que não é óbvio

## Entrega

```markdown
## Revisão de código: [título do PR ou arquivo]

### Resumo
[1 a 2 frases sobre as mudanças e a qualidade geral]

### Problemas críticos
| # | Arquivo | Linha | Problema | Gravidade |
|---|---------|-------|----------|-----------|
| 1 | [arquivo] | [linha] | [descrição] | 🔴 Crítico |

### Sugestões
| # | Arquivo | Linha | Sugestão | Categoria |
|---|---------|-------|----------|-----------|
| 1 | [arquivo] | [linha] | [descrição] | Desempenho |

### O que está bom
- [pontos positivos]

### Veredito
[Aprovar / Pedir mudanças / Precisa conversar]
```

## Se houver ferramentas conectadas

Se **~~source control** (repositório de código) estiver conectado:
- Puxe o diff do PR pelo link
- Veja a situação do CI e dos testes

Se **~~project tracker** (gestão de tarefas) estiver conectado:
- Ligue os achados às tarefas relacionadas
- Confira se o PR atende ao que a tarefa pedia

Se **~~knowledge base** (base de conhecimento) estiver conectada:
- Confira as mudanças com o padrão de código e o guia de estilo do time

## Dicas

1. **Dê contexto.** "Esse trecho é muito usado" ou "isso mexe com dados pessoais" ajuda a focar.
2. **Diga a preocupação.** "Foca em segurança" deixa a revisão mais direta.
3. **Inclua os testes.** Eu confiro a cobertura e a qualidade deles também.
