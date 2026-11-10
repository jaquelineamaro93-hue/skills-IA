---
name: achar-e-corrigir-erro
description: Sessão organizada para achar e corrigir um erro no sistema - reproduzir, isolar, descobrir a causa e corrigir. Use com uma mensagem de erro ou stack trace, "funciona em homologação mas não em produção", "quebrou depois do deploy", "está dando erro 500", ou quando o sistema faz algo diferente do esperado e a causa não é óbvia (debug).
argument-hint: "<mensagem de erro ou descrição do problema>"
---

# Achar e corrigir erro

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Uma sessão passo a passo para achar e corrigir problemas sem chute.

## Como usar

```
/desenvolvimento-de-software:achar-e-corrigir-erro $ARGUMENTS
```

## Como funciona

```
Passo 1: REPRODUZIR
  ✓ Entender o que deveria acontecer x o que acontece
  ✓ Descobrir os passos exatos para o erro aparecer
  ✓ Ver o tamanho (quando começou? quem é afetado?)

Passo 2: ISOLAR
  ✓ Achar a parte do sistema, serviço ou trecho de código
  ✓ Ver o que mudou (deploys, configurações, dependências)
  ✓ Ler logs e mensagens de erro

Passo 3: DESCOBRIR A CAUSA
  ✓ Levantar hipóteses e testar cada uma
  ✓ Seguir o caminho do código
  ✓ Achar a causa de verdade (não só o sintoma)

Passo 4: CORRIGIR
  ✓ Propor a correção explicando o porquê
  ✓ Pensar em efeitos colaterais e casos extremos
  ✓ Sugerir testes para o erro não voltar
```

## O que preciso de você

Conte o problema. Qualquer um destes ajuda:
- Mensagem de erro ou stack trace
- Passos para reproduzir
- O que mudou recentemente
- Logs ou prints
- O que deveria acontecer x o que acontece

## Entrega

```markdown
## Relatório do erro: [resumo]

### Como reproduzir
- **Esperado**: [o que deveria acontecer]
- **O que acontece**: [o que acontece no lugar]
- **Passos**: [como reproduzir]

### Causa
[Por que o erro acontece]

### Correção
[Mudanças de código ou de configuração]

### Para não voltar
- [Teste a adicionar]
- [Proteção a colocar]
```

## Se houver ferramentas conectadas

Se **~~monitoring** (monitoramento) estiver conectado:
- Puxe logs, taxa de erros e métricas do horário do problema
- Mostre deploys e mudanças de configuração recentes que possam estar ligados

Se **~~source control** (repositório de código) estiver conectado:
- Ache os commits e PRs recentes que mexeram no código afetado
- Veja se o problema começou com uma mudança específica

Se **~~project tracker** (gestão de tarefas) estiver conectado:
- Procure relatos parecidos ou problemas já conhecidos
- Crie uma tarefa para a correção quando a causa for achada

## Dicas

1. **Mande a mensagem de erro exata.** Não resuma: o texto exato importa.
2. **Diga o que mudou.** Deploys, atualização de dependências e mudança de configuração são os primeiros suspeitos.
3. **Dê contexto.** "Funciona em homologação mas não em produção" ou "só com arquivos grandes" ajuda muito.
