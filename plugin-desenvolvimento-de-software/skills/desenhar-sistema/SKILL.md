---
name: desenhar-sistema
description: Ajuda a desenhar sistemas, serviços e arquiteturas. Use quando a pessoa disser "desenha um sistema para", "como devemos montar a arquitetura", "system design", "qual a arquitetura certa para", ou precisar de ajuda com desenho de API, modelo de dados ou divisão entre serviços.
---

# Desenhar sistema

Ajuda a desenhar sistemas e a avaliar decisões de arquitetura.

## Passo a passo

### 1. Levantar requisitos
- O que o sistema faz (requisitos funcionais)
- Como precisa se comportar: escala, velocidade, disponibilidade, custo
- Restrições: tamanho do time, prazo, tecnologias que já existem

### 2. Visão geral
- Desenho dos componentes
- Caminho dos dados
- Contratos de API
- Onde guardar os dados

### 3. Detalhes
- Modelo de dados
- Endpoints da API (REST, GraphQL, gRPC)
- Estratégia de cache
- Filas e eventos
- Tratamento de erros e novas tentativas

### 4. Escala e confiabilidade
- Estimativa de carga
- Crescer na horizontal x na vertical
- O que acontece se algo cair (redundância)
- Monitoramento e alertas

### 5. Prós e contras
- Toda decisão tem prós e contras. Deixe claro.
- Considere: complexidade, custo, o que o time conhece, prazo para lançar, manutenção

## Entrega

Documentos de desenho claros e organizados, com diagramas (em texto ou descritos), as suposições à mostra e a análise de prós e contras. Sempre diga o que você reveria quando o sistema crescer.
