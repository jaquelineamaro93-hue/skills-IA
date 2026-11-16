# Vetores, pesos e fases

## Motor genérico
Cada vetor responde a uma pergunta de negócio. Cada um tem duas notas:
- **P1 (0 a 3): situação agora.** Existe sinal bom ou ruim? Com que intensidade?
- **P2 (0 a 2): profundidade ou tendência.** Quão sólido é isso? Relação, tendência, autonomia.

A nota do vetor vai de 0 a 5. O peso diz quanto o vetor pesa no score final.

## Vetores-base (adapte, não copie)

| Vetor | Pergunta | Peso típico | Exemplo de P1 |
|---|---|---|---|
| Risco | Esse cliente vai renovar? | 2 (3 na renovação) | 3 = cliente falou em expandir; 1 = sinal de alerta |
| Uso | Ele usa o produto de verdade? | 2 | 3 = uso alto e estável; 0 = sem uso no período |
| Adoção por módulo ou área | Quantas partes do produto ele já usa? | 2 | 3 = usa três ou mais; 1 = usa uma |
| Valor | Ele está vendo o resultado que comprou? | 2 (zero na fase de implantação) | 3 = resultado medido e reconhecido |
| Relação | Ele recebe e usa o acompanhamento? | 1 | 3 = responde e age sobre as reuniões |
| Atrito técnico (opcional) | Ele trava no produto? | 1 | 3 = nenhum erro; 0 = erros recorrentes |

Até seis vetores. Se precisar de mais, o negócio tem duas leituras misturadas.

## Como escolher pesos
- **Operação de alto toque** (relacionamento pesa mais): Relação e Risco com peso maior.
- **Self-serve**, muitos clientes pequenos: Uso e Valor pesam mais; Relação pode sair (não há contato por cliente).
- **Implantação pesada ou serviço**: Atrito e Adoção pesam mais, porque o processo do cliente trava a adoção.
- **Infraestrutura ou ferramenta técnica**: Atrito pesa mais, porque estabilidade é o produto.
- **Contrato de consumo variável**: crie um vetor de consumo financeiro.

## Fases
Cada fase pode mudar os pesos e até tirar um vetor de cena. Regras:
- Implantação ou onboarding: o vetor de valor não pesa (zero peso). Não há resultado para mostrar ainda.
- Renovação (últimos 60 dias de contrato): o vetor de risco ganha peso.
- Acesso vencido ou pagamento em atraso: risco explícito, faixa vermelha, independente do número.

Quando um vetor sai, o divisor acompanha a soma dos pesos ativos. A conta é sempre `soma(nota × peso) ÷ (soma dos pesos ativos ÷ 2)`.

## Duas adaptações reais (anonimizadas)
**Operação de alto toque, com renovação anual e contato por cliente:** Risco 2 (3 na renovação), Uso 2, Adoção 2, Valor 2, Relação 1. A faixa vermelha dispara com risco explícito.

**Plataforma de mentoria com agenda e trilhas:** Risco 2 (3 na renovação), Uso 2, Entregas por módulo 2, Valor de carreira 2 (zero em onboarding), Relação com a mentoria 1, Atrito técnico 1. Aqui "entrega" é algo produzido dentro do módulo, e não visita.

Duas leituras diferentes, o mesmo motor. Isso é o que faz o modelo servir a outros negócios.
