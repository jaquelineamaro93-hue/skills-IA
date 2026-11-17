"""Mostra o custo real por lead qualificado e por venda, cruzando o gasto do Meta com o CRM.

Uso:
    python3 -I cac_por_lead.py gasto.csv leads.csv saida.csv [--chave campanha|conjunto|anuncio]

gasto.csv: exportação do Gerenciador de Anúncios no mesmo nível da chave
           (nome + valor usado + resultados; os nomes de coluna em português ou inglês servem).
leads.csv: exportação do CRM, uma linha por lead. Colunas reconhecidas:
    campanha | utm_campaign      (chave = campanha)
    conjunto | utm_term          (chave = conjunto)
    anuncio  | utm_content       (chave = anuncio)
    qualificado                  sim/não, 1/0, true/false (lead que passou no seu critério)
    venda | valor_venda          valor da venda; vazio ou 0 = não comprou

Saída, por item: leads do Meta (o que o Gerenciador conta), leads no CRM, qualificados, vendas,
receita, gasto, CPL do Meta, custo por lead qualificado, CAC e ROAS real.
Leads do CRM sem UTM aparecem na linha "(sem utm)", para você ver o tamanho do buraco.
Sem dependências externas.
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # funciona também com python3 -I
from diagnosticar_campanhas import SINONIMOS, mapear_colunas, normalizar, numero, div

CHAVES_CRM = {
    "campanha": ["campanha", "utm_campaign", "utm campaign", "campaign"],
    "conjunto": ["conjunto", "conjunto de anuncios", "utm_term", "utm term", "ad set"],
    "anuncio": ["anuncio", "utm_content", "utm content", "ad"],
}
NOME_GASTO = {
    "campanha": ["nome da campanha", "campaign name"],
    "conjunto": ["nome do conjunto de anuncios", "ad set name"],
    "anuncio": ["nome do anuncio", "ad name"],
}
SIM = {"sim", "s", "1", "true", "verdadeiro", "yes", "y", "x", "qualificado", "mql", "sql"}


def ler(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096)
        f.seek(0)
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        leitor = csv.DictReader(f, dialect=dialeto)
        return leitor.fieldnames or [], list(leitor)


def achar(cabecalho, opcoes):
    normal = {normalizar(c): c for c in cabecalho}
    for o in opcoes:
        if normalizar(o) in normal:
            return normal[normalizar(o)]
    return None


def chave(texto):
    return normalizar(texto)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("gasto")
    p.add_argument("leads")
    p.add_argument("saida")
    p.add_argument("--chave", choices=list(CHAVES_CRM), default="campanha")
    args = p.parse_args()

    cab_g, linhas_g = ler(args.gasto)
    mapa_g = mapear_colunas(cab_g)
    col_nome = achar(cab_g, NOME_GASTO[args.chave]) or mapa_g.get("nome")
    if not col_nome or "gasto" not in mapa_g:
        sys.exit("No arquivo de gasto, não achei o nome do item e o valor usado.")

    cab_l, linhas_l = ler(args.leads)
    col_k = achar(cab_l, CHAVES_CRM[args.chave])
    col_q = achar(cab_l, ["qualificado", "qualified", "lead qualificado", "mql"])
    col_v = achar(cab_l, ["venda", "valor_venda", "valor da venda", "receita", "valor", "revenue"])
    if not col_k:
        sys.exit(f"No CRM, não achei a coluna da chave '{args.chave}' "
                 f"(tente uma destas: {', '.join(CHAVES_CRM[args.chave])}).")
    print(f"Chave: {args.chave} | gasto: '{col_nome}' | CRM: '{col_k}', "
          f"qualificado: '{col_q or 'sem dado'}', venda: '{col_v or 'sem dado'}'")

    itens = {}
    for linha in linhas_g:
        nome = (linha.get(col_nome) or "").strip()
        if not nome or normalizar(nome).startswith(("total", "resultados de")):
            continue
        it = itens.setdefault(chave(nome), {"nome": nome, "gasto": 0.0, "leads_meta": 0.0,
                                            "leads_crm": 0, "qualificados": 0, "vendas": 0, "receita": 0.0})
        it["gasto"] += numero(linha.get(mapa_g["gasto"])) or 0
        if "resultados" in mapa_g:
            it["leads_meta"] += numero(linha.get(mapa_g["resultados"])) or 0

    for linha in linhas_l:
        k = chave(linha.get(col_k))
        if k not in itens:
            nome = (linha.get(col_k) or "").strip() or "(sem utm)"
            k = k or "(sem utm)"
            itens.setdefault(k, {"nome": nome, "gasto": 0.0, "leads_meta": 0.0,
                                 "leads_crm": 0, "qualificados": 0, "vendas": 0, "receita": 0.0})
        it = itens[k]
        it["leads_crm"] += 1
        if col_q and normalizar(linha.get(col_q)) in SIM:
            it["qualificados"] += 1
        valor = numero(linha.get(col_v)) if col_v else None
        if valor:
            it["vendas"] += 1
            it["receita"] += valor

    def fmt(x):
        return f"{x:.2f}" if x is not None else ""

    saida = []
    for it in sorted(itens.values(), key=lambda i: -i["gasto"]):
        if not it["gasto"]:  # lead sem gasto ligado (ex.: sem utm): custo não se calcula
            it_div = lambda a, b: None  # noqa: E731
        else:
            it_div = div
        saida.append({
            "item": it["nome"], "gasto": fmt(it["gasto"]),
            "leads_meta": f"{it['leads_meta']:g}", "leads_crm": it["leads_crm"],
            "qualificados": it["qualificados"],
            "taxa_qualificacao_%": fmt(div(100 * it["qualificados"], it["leads_crm"])),
            "vendas": it["vendas"], "receita": fmt(it["receita"]),
            "cpl_meta": fmt(it_div(it["gasto"], it["leads_meta"])),
            "custo_por_qualificado": fmt(it_div(it["gasto"], it["qualificados"])),
            "cac": fmt(it_div(it["gasto"], it["vendas"])),
            "roas_real": fmt(it_div(it["receita"], it["gasto"])),
        })
    with open(args.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(saida[0].keys()))
        w.writeheader()
        w.writerows(saida)

    print()
    print(f"{'item':32} {'gasto':>10} {'CPL Meta':>9} {'custo/qualif':>12} {'CAC':>10} {'ROAS':>6}")
    for r in saida:
        print(f"{r['item'][:32]:32} {r['gasto']:>10} {r['cpl_meta'] or '-':>9} "
              f"{r['custo_por_qualificado'] or '-':>12} {r['cac'] or '-':>10} {r['roas_real'] or '-':>6}")
    tot_g = sum(i["gasto"] for i in itens.values())
    tot_q = sum(i["qualificados"] for i in itens.values())
    tot_v = sum(i["vendas"] for i in itens.values())
    print(f"\nTotal: gasto {tot_g:.2f} | custo por qualificado {fmt(div(tot_g, tot_q)) or '-'} "
          f"| CAC {fmt(div(tot_g, tot_v)) or '-'}")
    print(f"Tabela completa em {args.saida}")


if __name__ == "__main__":
    main()
