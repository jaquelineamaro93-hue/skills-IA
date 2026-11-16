"""Calcula o health score de clientes a partir de um CSV de notas.

Uso:
    python3 -I calcular_score.py entrada.csv saida.csv [--pesos "v1=2,v2=2,v3=2,v4=2,v5=1"]

Entrada (uma linha por cliente):
    cliente, fase, risco_explicito, v1_p1, v1_p2, v2_p1, v2_p2, ...
    - v?_p1 vai de 0 a 3; v?_p2 vai de 0 a 2. Deixe em branco quando o vetor não se aplica.
    - risco_explicito: 1 se há risco explícito (acesso vencido, inadimplência, pedido de saída).

Regras:
    - Nota do vetor = P1 + P2 (0 a 5). Vetor sem nota (em branco) sai do cálculo.
    - score = soma(nota x peso) / (soma dos pesos ativos / 2), escala 0 a 10.
    - Faixa: risco explícito = vermelho; score >= 7,5 = verde; >= 5 = amarelo; senão vermelho.
Sem dependências externas.
"""
import argparse
import csv
import sys

PESOS_PADRAO = {"v1": 2, "v2": 2, "v3": 2, "v4": 2, "v5": 1}


def ler_pesos(texto):
    if not texto:
        return dict(PESOS_PADRAO)
    pesos = {}
    for parte in texto.split(","):
        chave, valor = parte.split("=")
        pesos[chave.strip()] = float(valor)
    return pesos


def numero(valor):
    valor = (valor or "").strip()
    return float(valor) if valor else None


def calcular(linha, pesos):
    notas = {}
    for vetor in pesos:
        p1 = numero(linha.get(f"{vetor}_p1"))
        p2 = numero(linha.get(f"{vetor}_p2"))
        if p1 is None and p2 is None:
            continue
        notas[vetor] = (p1 or 0) + (p2 or 0)

    soma_ponderada = sum(notas[v] * pesos[v] for v in notas)
    soma_pesos = sum(pesos[v] for v in notas)
    if soma_pesos == 0:
        return None, "sem_dados", notas

    score = round(soma_ponderada / (soma_pesos / 2), 1)
    if (linha.get("risco_explicito") or "").strip() == "1":
        faixa = "vermelho"
    elif score >= 7.5:
        faixa = "verde"
    elif score >= 5:
        faixa = "amarelo"
    else:
        faixa = "vermelho"
    return score, faixa, notas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--pesos", default="", help="ex.: v1=2,v2=2,v3=2,v4=2,v5=1")
    args = ap.parse_args()
    pesos = ler_pesos(args.pesos)

    with open(args.entrada, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))

    colunas = ["cliente", "fase", "score", "faixa"] + [f"{v}_nota" for v in pesos]
    with open(args.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas)
        w.writeheader()
        for linha in linhas:
            score, faixa, notas = calcular(linha, pesos)
            saida = {"cliente": linha.get("cliente", ""), "fase": linha.get("fase", ""),
                     "score": score if score is not None else "", "faixa": faixa}
            for v in pesos:
                saida[f"{v}_nota"] = notas.get(v, "")
            w.writerow(saida)
    print(f"{len(linhas)} clientes calculados em {args.saida}", file=sys.stderr)


if __name__ == "__main__":
    main()
