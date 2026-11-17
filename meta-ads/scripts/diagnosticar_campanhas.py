"""Diagnostica campanhas do Meta Ads: o que cortar, ajustar, manter ou escalar.

Uso:
    python3 -I diagnosticar_campanhas.py export.csv saida.csv [--cpa-alvo 80] [--roas-alvo 3]
                                         [--freq-max 3] [--ctr-min 0.8]

Entrada:
    A exportação do Gerenciador de Anúncios (CSV), em português ou inglês, no nível que você
    quiser (campanha, conjunto ou anúncio). Colunas reconhecidas, pelo nome:
      nome            Nome da campanha / do conjunto de anúncios / do anúncio (ou Campaign/Ad set/Ad name)
      gasto           Valor usado (BRL) / Amount spent
      impressoes      Impressões / Impressions
      frequencia      Frequência / Frequency
      cliques         Cliques no link / Link clicks
      resultados      Resultados / Results  (ou Compras, Leads)
      receita         Valor de conversão de compras / Purchases conversion value  (opcional)
    Colunas que faltarem viram "sem dado"; o script avisa quais encontrou.

Regras (as mesmas de references/diagnostico.md):
    - Referência: --roas-alvo (se houver receita), senão --cpa-alvo, senão a mediana da conta.
    - Gastou 3x a referência de CPA sem nenhum resultado: CORTAR.
    - Gastou menos de 2x a referência e tem menos de 3 resultados: AGUARDAR (pouco dado).
    - CPA até 0,8x da referência (ou ROAS 1,25x do alvo), com 5+ resultados e frequência ok: ESCALAR.
    - CPA até 1,2x (ou ROAS 0,85x): MANTER.  Até 1,5x (ou ROAS 0,65x): AJUSTAR.  Pior que isso: CORTAR.
    - Alertas independentes: frequência alta (fadiga), CTR de link baixo (criativo), CPM caro (público).
Sem dependências externas.
"""
import argparse
import csv
import statistics
import sys
import unicodedata

SINONIMOS = {
    "nome": ["nome do anuncio", "nome do conjunto de anuncios", "nome da campanha",
             "ad name", "ad set name", "campaign name", "anuncio", "conjunto", "campanha",
             "nome", "name"],
    "gasto": ["valor usado", "amount spent", "gasto", "spend", "investimento"],
    "impressoes": ["impressoes", "impressions"],
    "frequencia": ["frequencia", "frequency"],
    "cliques": ["cliques no link", "link clicks", "cliques", "clicks"],
    "resultados": ["resultados", "results", "compras", "purchases", "leads", "conversoes",
                   "leads reportados", "compras reportadas"],
    "receita": ["valor de conversao de compras", "purchases conversion value",
                "valor de conversao", "conversion value", "receita", "revenue"],
}


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    texto = texto.lower().split("(")[0]
    return " ".join(texto.replace("_", " ").split())


def mapear_colunas(cabecalho):
    normal = {normalizar(c): c for c in cabecalho}
    mapa = {}
    extras = [normal[o] for o in ("leads reportados", "compras reportadas") if o in normal]
    if len(extras) > 1 and not any(o in normal for o in SINONIMOS["resultados"][:6]):
        mapa["resultados_somar"] = extras
    for campo, opcoes in SINONIMOS.items():
        for opcao in opcoes:  # ordem importa: o mais específico primeiro
            if opcao in normal:
                mapa[campo] = normal[opcao]
                break
    return mapa


def numero(valor):
    valor = (valor or "").strip().replace("R$", "").replace("%", "").strip()
    if not valor or valor in {"-", "—"}:
        return None
    if "," in valor and "." in valor:  # 1.234,56
        valor = valor.replace(".", "").replace(",", ".")
    elif "," in valor:
        valor = valor.replace(",", ".")
    try:
        return float(valor)
    except ValueError:
        return None


def div(a, b):
    return a / b if a is not None and b else None


def classificar(m, ref_cpa, roas_alvo, args):
    gasto, res, cpa, roas = m["gasto"] or 0, m["resultados"] or 0, m["cpa"], m["roas"]
    alertas = []
    if m["frequencia"] and m["frequencia"] > args.freq_max:
        alertas.append(f"fadiga: frequência {m['frequencia']:.1f}")
    if m["ctr"] is not None and m["ctr"] < args.ctr_min:
        alertas.append(f"criativo fraco: CTR de link {m['ctr']:.2f}%")
    if m.get("cpm_alto"):
        alertas.append(f"público caro: CPM {m['cpm']:.2f}")

    if ref_cpa and res == 0 and gasto >= 3 * ref_cpa:
        return "CORTAR", f"gastou {gasto:.2f} (3x+ o CPA de referência) sem resultado", alertas
    if ref_cpa and gasto < 2 * ref_cpa and res < 3:
        return "AGUARDAR", "pouco gasto e menos de 3 resultados: ainda não dá para julgar", alertas

    if roas_alvo and roas is not None:
        razao = roas / roas_alvo
        motivo = f"ROAS {roas:.2f} vs alvo {roas_alvo:.2f}"
        if razao >= 1.25 and res >= 5 and not any(a.startswith("fadiga") for a in alertas):
            return "ESCALAR", motivo, alertas
        if razao >= 0.85:
            return "MANTER", motivo, alertas
        if razao >= 0.65:
            return "AJUSTAR", motivo, alertas
        return "CORTAR", motivo, alertas

    if cpa is None or not ref_cpa:
        return "SEM DADO", "sem resultados ou sem referência de CPA", alertas
    razao = cpa / ref_cpa
    motivo = f"CPA {cpa:.2f} vs referência {ref_cpa:.2f}"
    if razao <= 0.8 and res >= 5 and not any(a.startswith("fadiga") for a in alertas):
        return "ESCALAR", motivo, alertas
    if razao <= 1.2:
        return "MANTER", motivo, alertas
    if razao <= 1.5:
        return "AJUSTAR", motivo, alertas
    return "CORTAR", motivo, alertas


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--cpa-alvo", type=float)
    p.add_argument("--roas-alvo", type=float)
    p.add_argument("--freq-max", type=float, default=3.0)
    p.add_argument("--ctr-min", type=float, default=0.8, help="CTR de link mínimo, em %%")
    args = p.parse_args()

    with open(args.entrada, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096)
        f.seek(0)
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        leitor = csv.DictReader(f, dialect=dialeto)
        mapa = mapear_colunas(leitor.fieldnames or [])
        linhas = list(leitor)

    if "nome" not in mapa or "gasto" not in mapa:
        sys.exit("Não achei as colunas de nome e de valor usado. Exporte de novo com elas.")
    faltando = [c for c in SINONIMOS if c not in mapa]
    print("Colunas usadas: " + ", ".join(f"{k} = '{v}'" for k, v in mapa.items() if k != "resultados_somar"))
    if "resultados_somar" in mapa:
        print("Resultados = soma de: " + ", ".join(mapa["resultados_somar"]))
    if faltando:
        print("Sem dado para: " + ", ".join(faltando))

    metricas = []
    for linha in linhas:
        m = {c: (numero(linha.get(mapa[c])) if c in mapa else None) for c in SINONIMOS if c != "nome"}
        if "resultados_somar" in mapa:
            valores = [numero(linha.get(c)) for c in mapa["resultados_somar"]]
            m["resultados"] = sum(v for v in valores if v) if any(v is not None for v in valores) else None
        m["nome"] = (linha.get(mapa["nome"]) or "").strip()
        if not m["nome"] or normalizar(m["nome"]).startswith(("total", "resultados de")):
            continue  # pula a linha de total que o Gerenciador inclui
        if m["gasto"] is None and m["impressoes"] is None:
            continue  # item sem nenhuma métrica no período (ex.: campanha antiga pausada)
        m["cpa"] = div(m["gasto"], m["resultados"])
        m["roas"] = div(m["receita"], m["gasto"])
        m["ctr"] = div((m["cliques"] or 0) * 100, m["impressoes"]) if m["cliques"] is not None else None
        m["cpm"] = div((m["gasto"] or 0) * 1000, m["impressoes"])
        metricas.append(m)

    cpas = [m["cpa"] for m in metricas if m["cpa"]]
    ref_cpa = args.cpa_alvo or (statistics.median(cpas) if cpas else None)
    origem = "alvo informado" if args.cpa_alvo else "mediana da conta (sem alvo informado)"
    cpms = [m["cpm"] for m in metricas if m["cpm"]]
    cpm_med = statistics.median(cpms) if cpms else None
    for m in metricas:
        m["cpm_alto"] = bool(cpm_med and m["cpm"] and m["cpm"] > 1.5 * cpm_med)
    roas_alvo = args.roas_alvo if "receita" in mapa else None

    saida = []
    for m in metricas:
        decisao, motivo, alertas = classificar(m, ref_cpa, roas_alvo, args)
        saida.append({
            "nome": m["nome"], "decisao": decisao, "motivo": motivo, "alertas": "; ".join(alertas),
            "gasto": f"{m['gasto'] or 0:.2f}", "resultados": f"{m['resultados'] or 0:g}",
            "cpa": f"{m['cpa']:.2f}" if m["cpa"] else "",
            "roas": f"{m['roas']:.2f}" if m["roas"] is not None else "",
            "ctr_link_%": f"{m['ctr']:.2f}" if m["ctr"] is not None else "",
            "cpm": f"{m['cpm']:.2f}" if m["cpm"] else "",
            "frequencia": f"{m['frequencia']:.2f}" if m["frequencia"] else "",
        })

    ordem = {"CORTAR": 0, "AJUSTAR": 1, "ESCALAR": 2, "MANTER": 3, "AGUARDAR": 4, "SEM DADO": 5}
    saida.sort(key=lambda r: (ordem[r["decisao"]], -float(r["gasto"])))
    with open(args.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(saida[0].keys()) if saida else ["nome"])
        w.writeheader()
        w.writerows(saida)

    total = sum(float(r["gasto"]) for r in saida)
    print(f"\nReferência de CPA: {ref_cpa:.2f} ({origem})" if ref_cpa else "\nSem referência de CPA.")
    if roas_alvo:
        print(f"ROAS alvo: {roas_alvo:.2f}")
    print(f"Itens analisados: {len(saida)} | gasto total: {total:.2f}\n")
    for decisao in ordem:
        grupo = [r for r in saida if r["decisao"] == decisao]
        if grupo:
            g = sum(float(r["gasto"]) for r in grupo)
            pct = 100 * g / total if total else 0
            print(f"{decisao:9} {len(grupo):3} itens  gasto {g:10.2f}  ({pct:4.1f}% do total)")
    cortar = [r for r in saida if r["decisao"] == "CORTAR"]
    if cortar:
        print("\nGasto em itens para cortar (desperdício provável):",
              f"{sum(float(r['gasto']) for r in cortar):.2f}")
    print(f"\nTabela completa em {args.saida}")


if __name__ == "__main__":
    main()
