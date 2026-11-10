---
name: plano-de-testes
description: Monta a estratégia e o plano de testes de um sistema. Use quando a pessoa perguntar "como devemos testar isso", "estratégia de testes para", "escreve os testes de", "plano de testes", "quais testes precisamos", ou precisar de ajuda com tipos de teste, cobertura ou organização dos testes.
---

# Plano de testes

Monta estratégias de teste que equilibram cobertura, velocidade e manutenção.

## Pirâmide de testes

```
        / Ponta a ponta \       Poucos, lentos, muita confiança
       /   Integração    \      Alguns, velocidade média
      /    Unitários      \     Muitos, rápidos, focados
```

## Estratégia por tipo de componente

- **Endpoints de API:** testes unitários para a regra de negócio, de integração para a camada HTTP, de contrato para quem consome
- **Fluxos de dados:** validação da entrada, transformação correta, rodar duas vezes dá o mesmo resultado (idempotência)
- **Telas (frontend):** testes de componente, de interação, de mudança visual e de acessibilidade
- **Infraestrutura:** testes rápidos de fumaça, testes de caos, testes de carga

## O que cobrir

Foque em: caminhos críticos para o negócio, tratamento de erros, casos extremos, limites de segurança, integridade dos dados.

Pule: getters e setters triviais, código do framework, scripts de uso único.

## Entrega

Um plano de testes com: o que testar, o tipo de teste de cada área, metas de cobertura e exemplos de casos de teste. Aponte o que falta na cobertura atual.
