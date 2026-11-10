#!/usr/bin/env python3
"""Monta a Análise de Cohort (.xlsx) a partir de uma base de receita por cliente.

Uso:
    python3 montar_cohort.py config.json saida.xlsx

O config.json diz onde está a base e como ler as colunas (veja examples/config-exemplo.json).
Base aceita (CSV ou XLSX), formato longo, uma linha por cliente x data (ou pedido):
    cliente | data | receita | [quantidade] | [colunas de segmento: canal, plano...]

Criado por Jaqueline Amaro (CC BY-NC 4.0). Requer: pandas, openpyxl.
"""
import json
import sys

import pandas as pd
from openpyxl import Workbook
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

MARROM = "4B342C"
CREME = "FFF8E9"
CINZA = "EFEAE4"
VERDE = "DCEFD9"
VERMELHO = "F8D7D3"
F_TIT = Font(bold=True, size=14, color=MARROM)
F_CAB = Font(bold=True, color="FFFFFF")
F_SUB = Font(italic=True, color="756359")
FILL_CAB = PatternFill("solid", fgColor=MARROM)
FILL_IN = PatternFill("solid", fgColor=CREME)
FILL_CALC = PatternFill("solid", fgColor=CINZA)
QUEBRA = Alignment(wrap_text=True, vertical="top")
MOEDA = '"R$" #,##0.00'
MOEDA0 = '"R$" #,##0'


def cab(ws, linha, cols, larg=None, col0=1):
    for i, n in enumerate(cols):
        c = ws.cell(row=linha, column=col0 + i, value=n)
        c.font = F_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(wrap_text=True, vertical="center")
        if larg:
            ws.column_dimensions[get_column_letter(col0 + i)].width = larg[i]


def tit(ws, t, sub=None):
    ws["A1"] = t
    ws["A1"].font = F_TIT
    if sub:
        ws["A2"] = sub
        ws["A2"].font = F_SUB


def mes_txt(d):
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    return f"{meses[d.month - 1]}/{d.year}"


# ---------------- leitura e preparo ----------------
def ler_base(cfg):
    caminho = cfg["base"]
    df = pd.read_excel(caminho, sheet_name=cfg.get("aba", 0)) if caminho.lower().endswith((".xlsx", ".xls")) else pd.read_csv(caminho, sep=cfg.get("separador", ","))
    col = cfg["colunas"]
    ren = {col["cliente"]: "cliente", col["data"]: "data", col["receita"]: "receita"}
    if col.get("quantidade"):
        ren[col["quantidade"]] = "qtd"
    segs = cfg.get("segmentos", {})
    for nome, c in segs.items():
        ren[c] = f"seg_{nome}"
    df = df.rename(columns=ren)
    df["data"] = pd.to_datetime(df["data"], dayfirst=cfg.get("dia_primeiro", True))
    df["receita"] = pd.to_numeric(df["receita"], errors="coerce").fillna(0)
    if "qtd" in df:
        df["qtd"] = pd.to_numeric(df["qtd"], errors="coerce").fillna(0)
    elif cfg.get("tipo") == "pedidos":
        df["qtd"] = 1
    df["mes"] = df["data"].dt.to_period("M").dt.to_timestamp()
    if cfg.get("ate"):
        df = df[df["mes"] <= pd.Timestamp(cfg["ate"])]
    if cfg.get("desde"):
        df = df[df["mes"] >= pd.Timestamp(cfg["desde"])]
    return df


def montar_dados(df, cfg):
    pos = df[df["receita"] > 0]
    primeira = pos.groupby("cliente")["mes"].min().rename("cohort")
    df = df.join(primeira, on="cliente")
    df = df[df["cohort"].notna()]
    fim = df["mes"].max()
    agg = {"receita": "sum"}
    if "qtd" in df:
        agg["qtd"] = "sum"
    por_cli_mes = df.groupby(["cohort", "mes", "cliente"]).agg(agg).reset_index()
    ativos = por_cli_mes[por_cli_mes["receita"] > 0]
    base = primeira.reset_index().groupby("cohort")["cliente"].nunique()
    linhas = []
    for coh, n0 in base.items():
        mes = coh
        idx = 0
        while mes <= fim:
            a = ativos[(ativos["cohort"] == coh) & (ativos["mes"] == mes)]
            linhas.append({
                "cohort": coh, "mes": mes, "mes_indice": idx,
                "clientes_ativos": a["cliente"].nunique(), "clientes_cohort": n0,
                "qtd": float(a["qtd"].sum()) if "qtd" in a else None,
                "receita": float(a["receita"].sum()),
            })
            mes = mes + pd.offsets.MonthBegin(1)
            idx += 1
    return pd.DataFrame(linhas), df, primeira, fim


def faixa_ticket(v, faixas):
    for nome, lim in faixas:
        if lim is None or v <= lim:
            return nome
    return faixas[-1][0]


# ---------------- abas ----------------
def aba_leia_me(wb, cfg, fim, dados):
    ws = wb.active
    ws.title = "Leia-me"
    tit(ws, f"Análise de Cohort — {cfg.get('empresa', 'Sua empresa')}", f"Período: {mes_txt(dados['cohort'].min())} a {mes_txt(fim)}")
    tipo = cfg.get("tipo", "recorrente")
    blocos = [
        ("COMO LER", [
            ("Cohort (safra)", "Grupo de clientes que fez a primeira compra (ou começou a pagar) no mesmo mês."),
            ("Mês 0, mês 1, mês 2...", "Não é o calendário: é quanto tempo passou desde a entrada daquele grupo."),
            ("Retenção", "De cada 100 clientes que entraram juntos, quantos ainda compram/pagam depois de N meses."),
            ("Receita acumulada", "Tudo o que o grupo deixou de receita até aquele mês."),
            ("LTV", "Receita acumulada ÷ clientes que entraram: quanto cada cliente conquistado deixou, em média."),
            ("LTV (margem)", "O mesmo, mas só com a margem: é o que sobra para pagar a aquisição."),
            ("CAC", "Investimento de aquisição do mês ÷ clientes que entraram naquele mês."),
            ("LTV / CAC", "Quantas vezes o cliente já devolveu o custo de conquistá-lo. Acima de 1 na margem = já se pagou."),
        ]),
        ("DEFINIÇÕES DESTE MODELO", [
            ("Entrada no cohort", "Mês da primeira receita maior que zero do cliente."),
            ("Cliente ativo no mês", "Cliente do cohort com receita maior que zero naquele mês."),
            ("Ticket médio", "Receita do mês ÷ quantidade (pedidos/uso) do mês." if tipo == "pedidos" or cfg["colunas"].get("quantidade") else "Receita do mês ÷ clientes ativos no mês."),
            ("Receita por cliente ativo", "Receita do mês ÷ clientes ativos no mês."),
            ("Receita por cliente adquirido", "Receita do mês ÷ clientes que entraram no cohort."),
            ("Margem", "Percentual na aba Premissas, aplicado sobre a receita. Troque pela margem real."),
            ("Horizonte", f"Até {mes_txt(fim)}. Meses futuros (projetados ou contratados) ficam fora."),
        ]),
        ("O QUE VOCÊ PRECISA PREENCHER", [
            ("Premissas", "A margem bruta real (célula B4)."),
            ("Investimento", "O investimento de aquisição de cada mês (mídia, comissões de venda, eventos). Sem isso CAC e LTV/CAC ficam em branco."),
        ]),
    ]
    r = 4
    for titulo_bloco, itens in blocos:
        ws.cell(row=r, column=1, value=titulo_bloco).font = Font(bold=True, color=MARROM)
        r += 1
        for a, b in itens:
            ws.cell(row=r, column=1, value=a).font = Font(bold=True)
            ws.cell(row=r, column=2, value=b).alignment = QUEBRA
            r += 1
        r += 1
    fontes = cfg.get("fontes", [])
    if fontes:
        ws.cell(row=r, column=1, value="FONTES DE DADOS").font = Font(bold=True, color=MARROM)
        r += 1
        for f in fontes:
            ws.cell(row=r, column=2, value=f).alignment = QUEBRA
            r += 1
        r += 1
    lim = cfg.get("limitacoes", [])
    if lim:
        ws.cell(row=r, column=1, value="LIMITAÇÕES CONHECIDAS").font = Font(bold=True, color=MARROM)
        r += 1
        for f in lim:
            ws.cell(row=r, column=2, value=f).alignment = QUEBRA
            r += 1
        r += 1
    ws.cell(row=r + 1, column=1, value="Criado com a skill Análise de Cohort, por Jaqueline Amaro (CC BY-NC 4.0).").font = F_SUB
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 110


def aba_premissas(wb, cfg):
    ws = wb.create_sheet("Premissas")
    tit(ws, "Premissas", "Células creme: troque pelo valor real da empresa.")
    ws["A4"] = "Margem bruta %"
    ws["B4"] = cfg.get("margem", None)
    ws["B4"].number_format = "0%"
    ws["B4"].fill = FILL_IN
    ws["C4"] = "Usada em Margem, LTV (margem) e LTV/CAC (margem)."
    ws["A5"] = "Meta de LTV/CAC"
    ws["B5"] = cfg.get("meta_ltv_cac", 3)
    ws["B5"].fill = FILL_IN
    ws["C5"] = "Referência comum: 3x. Abaixo de 1x na margem, o cliente ainda não pagou o próprio custo."
    for c in ("A4", "A5"):
        ws[c].font = Font(bold=True)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["C"].width = 80


def aba_investimento(wb, cfg, cohorts):
    ws = wb.create_sheet("Investimento")
    tit(ws, "Investimento de aquisição por mês", "Mídia, comissão de vendas, eventos, ferramentas de prospecção: o que foi gasto para conquistar clientes no mês.")
    cab(ws, 4, ["Cohort (mês)", "Investimento"], [16, 16])
    inv = {pd.Timestamp(k): v for k, v in cfg.get("investimento", {}).items()}
    for i, c in enumerate(cohorts, start=5):
        ws.cell(row=i, column=1, value=c.to_pydatetime()).number_format = "MMM/YYYY"
        cel = ws.cell(row=i, column=2, value=inv.get(c))
        cel.number_format = MOEDA
        cel.fill = FILL_IN
    return len(cohorts)


COLS_DADOS = ["cohort", "mes", "mes_indice", "clientes_ativos", "clientes_cohort", "retencao", "qtd", "qtd_por_cliente",
              "receita_mes", "margem", "receita_acum", "margem_acum", "ticket_medio", "receita_por_ativo",
              "receita_por_adquirido", "ltv", "ltv_margem", "cac", "ltv_cac", "ltv_cac_margem"]


def aba_dados(wb, dados, n_inv, tem_qtd):
    ws = wb.create_sheet("Dados Cohorts")
    cab(ws, 1, COLS_DADOS, [11, 11, 9, 10, 10, 9, 10, 10, 13, 12, 14, 14, 12, 12, 12, 12, 12, 12, 9, 9])
    ws.freeze_panes = "D2"
    for i, row in enumerate(dados.itertuples(index=False), start=2):
        r = i
        ws.cell(row=r, column=1, value=row.cohort.to_pydatetime()).number_format = "MMM/YYYY"
        ws.cell(row=r, column=2, value=row.mes.to_pydatetime()).number_format = "MMM/YYYY"
        ws.cell(row=r, column=3, value=row.mes_indice)
        ws.cell(row=r, column=4, value=row.clientes_ativos)
        ws.cell(row=r, column=5, value=row.clientes_cohort)
        ws.cell(row=r, column=6, value=f"=D{r}/E{r}").number_format = "0.0%"
        if tem_qtd:
            ws.cell(row=r, column=7, value=row.qtd)
            ws.cell(row=r, column=8, value=f'=IF(D{r}=0,"",G{r}/D{r})').number_format = "0.00"
        ws.cell(row=r, column=9, value=row.receita).number_format = MOEDA
        ws.cell(row=r, column=10, value=f"=I{r}*Premissas!$B$4").number_format = MOEDA
        ws.cell(row=r, column=11, value=f"=IF(C{r}=0,I{r},I{r}+K{r-1})").number_format = MOEDA
        ws.cell(row=r, column=12, value=f"=IF(C{r}=0,J{r},J{r}+L{r-1})").number_format = MOEDA
        if tem_qtd:
            ws.cell(row=r, column=13, value=f'=IF(N(G{r})=0,"",I{r}/G{r})').number_format = MOEDA
        else:
            ws.cell(row=r, column=13, value=f'=IF(D{r}=0,"",I{r}/D{r})').number_format = MOEDA
        ws.cell(row=r, column=14, value=f'=IF(D{r}=0,"",I{r}/D{r})').number_format = MOEDA
        ws.cell(row=r, column=15, value=f"=I{r}/E{r}").number_format = MOEDA
        ws.cell(row=r, column=16, value=f"=K{r}/E{r}").number_format = MOEDA
        ws.cell(row=r, column=17, value=f"=L{r}/E{r}").number_format = MOEDA
        ws.cell(row=r, column=18, value=f'=IFERROR(IF(INDEX(Investimento!$B$5:$B${n_inv+4},MATCH(A{r},Investimento!$A$5:$A${n_inv+4},0))="","",INDEX(Investimento!$B$5:$B${n_inv+4},MATCH(A{r},Investimento!$A$5:$A${n_inv+4},0))/E{r}),"")').number_format = MOEDA
        ws.cell(row=r, column=19, value=f'=IF(N(R{r})=0,"",P{r}/R{r})').number_format = '0.00"x"'
        ws.cell(row=r, column=20, value=f'=IF(N(R{r})=0,"",Q{r}/R{r})').number_format = '0.00"x"'
    ws.auto_filter.ref = f"A1:T{len(dados)+1}"
    return len(dados) + 1


MATRIZES = [
    ("Clientes", "D", "0", "Clientes ativos em cada mês desde a entrada."),
    ("Retenção", "F", "0%", "Clientes ativos ÷ clientes que entraram. Verde = segura mais; vermelho = perde mais."),
    ("Receita", "I", MOEDA0, "Receita do cohort em cada mês."),
    ("Receita Acumulada", "K", MOEDA0, "Receita somada desde o mês 0."),
    ("Ticket Médio", "M", MOEDA, "Receita ÷ pedidos (ou ÷ clientes ativos, sem quantidade)."),
    ("Receita por Ativo", "N", MOEDA, "Quanto cada cliente que ficou deixou no mês."),
    ("Receita por Adquirido", "O", MOEDA, "Receita do mês ÷ clientes que entraram (dilui o churn)."),
    ("LTV", "P", MOEDA0, "Receita acumulada ÷ clientes que entraram."),
    ("LTV (margem)", "Q", MOEDA0, "Margem acumulada ÷ clientes que entraram."),
    ("LTV-CAC", "S", '0.0"x"', "LTV ÷ CAC. Fica vazio enquanto a aba Investimento não for preenchida."),
    ("LTV-CAC (margem)", "T", '0.0"x"', "LTV (margem) ÷ CAC. Quando passa de 1x, o cliente já pagou o custo de conquista."),
]


def aba_matriz(wb, nome, col, fmt, sub, cohorts, max_idx, linhas, tem_qtd):
    if nome == "Ticket Médio" and not tem_qtd:
        sub = "Receita do mês ÷ clientes ativos."
    ws = wb.create_sheet(nome)
    tit(ws, nome, sub)
    cab(ws, 4, ["Cohort", "Clientes"] + [f"mês {i}" for i in range(max_idx + 1)], [11, 9] + [10] * (max_idx + 1))
    ws.freeze_panes = "C5"
    for i, coh in enumerate(cohorts, start=5):
        ws.cell(row=i, column=1, value=coh.to_pydatetime()).number_format = "MMM/YYYY"
        ws.cell(row=i, column=2, value=f"='Dados Cohorts'!E{linhas[(coh, 0)]}")
        for k in range(max_idx + 1):
            r = linhas.get((coh, k))
            if r is None:
                continue
            ref = f"'Dados Cohorts'!{col}{r}"
            c = ws.cell(row=i, column=3 + k, value=f'=IF({ref}="","",{ref})')
            c.number_format = fmt
    ult = 4 + len(cohorts)
    fim = get_column_letter(3 + max_idx)
    if nome == "Retenção":
        ws.conditional_formatting.add(f"D5:{fim}{ult}", ColorScaleRule(start_type="num", start_value=0, start_color="F4B6AE", mid_type="num", mid_value=0.5, mid_color="FFF3C4", end_type="num", end_value=1, end_color="B9DFB3"))
    elif nome.startswith("LTV-CAC"):
        ws.conditional_formatting.add(f"C5:{fim}{ult}", FormulaRule(formula=['AND(C5<>"",C5>=1)'], fill=PatternFill("solid", fgColor=VERDE)))
    else:
        ws.conditional_formatting.add(f"C5:{fim}{ult}", ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color="D9C7B8"))


def curva_grupo(df_cli, ativos_cm, fim, max_idx):
    """Retenção mês a mês de um grupo de clientes, com base só em quem já teve tempo de viver o mês."""
    out = []
    for k in range(max_idx + 1):
        elegiveis = df_cli[df_cli["cohort"] + pd.DateOffset(months=k) <= fim]
        if len(elegiveis) == 0:
            out.append(None)
            continue
        alvo = set(zip(elegiveis["cliente"], elegiveis["cohort"] + pd.DateOffset(months=k)))
        vivos = sum(1 for p in alvo if p in ativos_cm)
        out.append(vivos / len(elegiveis))
    return out


def aba_segmento(wb, titulo_seg, coluna, df, primeira, fim, max_idx, sub):
    ws = wb.create_sheet(titulo_seg[:31])
    tit(ws, titulo_seg, sub)
    cli = primeira.reset_index()
    seg = df.groupby("cliente")[coluna].agg(lambda s: s.dropna().iloc[0] if s.dropna().size else "Sem informação")
    cli = cli.join(seg, on="cliente").rename(columns={coluna: "grupo"})
    cm = df[df["receita"] > 0].groupby(["cliente", "mes"]).size().reset_index()
    ativos_cm = set(zip(cm["cliente"], cm["mes"]))
    vida = cm.groupby("cliente").size()
    rec_fim = df[df["mes"] == fim].groupby("cliente")["receita"].sum()
    cab(ws, 4, ["Grupo", "Clientes", "Ativos no último mês", "Retenção atual", "Vida média (meses com receita)", f"Receita em {mes_txt(fim)}", "Receita total no período"], [30, 10, 12, 12, 14, 16, 18])
    r = 5
    grupos = cli.groupby("grupo")
    ordem = sorted(grupos.groups.keys(), key=lambda g: -len(grupos.get_group(g)))
    for g in ordem:
        gcli = grupos.get_group(g)
        ids = set(gcli["cliente"])
        ativos = sum(1 for c in ids if (c, fim) in ativos_cm)
        ws.cell(row=r, column=1, value=str(g))
        ws.cell(row=r, column=2, value=len(ids))
        ws.cell(row=r, column=3, value=ativos)
        ws.cell(row=r, column=4, value=ativos / len(ids)).number_format = "0%"
        ws.cell(row=r, column=5, value=float(vida.reindex(list(ids)).fillna(0).mean())).number_format = "0.0"
        ws.cell(row=r, column=6, value=float(rec_fim.reindex(list(ids)).fillna(0).sum())).number_format = MOEDA0
        ws.cell(row=r, column=7, value=float(df[df["cliente"].isin(ids)]["receita"].sum())).number_format = MOEDA0
        r += 1
    r += 2
    ws.cell(row=r, column=1, value="Retenção mês a mês por grupo").font = Font(bold=True, color=MARROM)
    ws.cell(row=r + 1, column=1, value="Cada linha é o grupo inteiro (todas as safras juntas). A base de cada mês tem só os clientes que já tiveram tempo de chegar nele; por isso os últimos meses têm poucos clientes.").font = F_SUB
    r0 = r + 2
    cab(ws, r0, ["Grupo"] + [f"mês {k}" for k in range(max_idx + 1)], None)
    for i, g in enumerate(ordem, start=r0 + 1):
        curva = curva_grupo(grupos.get_group(g), ativos_cm, fim, max_idx)
        ws.cell(row=i, column=1, value=str(g))
        for k, v in enumerate(curva):
            if v is not None:
                ws.cell(row=i, column=2 + k, value=v).number_format = "0%"
    fimc = get_column_letter(2 + max_idx)
    ws.conditional_formatting.add(f"B{r0+1}:{fimc}{r0+len(ordem)}", ColorScaleRule(start_type="num", start_value=0, start_color="F4B6AE", mid_type="num", mid_value=0.5, mid_color="FFF3C4", end_type="num", end_value=1, end_color="B9DFB3"))
    for k in range(max_idx + 1):
        ws.column_dimensions[get_column_letter(2 + k)].width = max(ws.column_dimensions[get_column_letter(2 + k)].width or 0, 9)


def aba_resumo(wb, cfg, dados, df, primeira, fim, max_idx):
    ws = wb.create_sheet("Resumo", 1)
    tit(ws, f"Resumo do cohort — {cfg.get('empresa', '')}", f"{mes_txt(dados['cohort'].min())} a {mes_txt(fim)} · {primeira.size} clientes em {dados['cohort'].nunique()} safras")
    cm = df[df["receita"] > 0].groupby(["cliente", "mes"]).size().reset_index()
    ativos_cm = set(zip(cm["cliente"], cm["mes"]))
    cli = primeira.reset_index()

    def ret_pond(k):
        el = cli[cli["cohort"] + pd.DateOffset(months=k) <= fim]
        if len(el) == 0:
            return None
        return sum(1 for c, co in zip(el["cliente"], el["cohort"]) if (c, co + pd.DateOffset(months=k)) in ativos_cm) / len(el)

    ind = [
        ("Clientes adquiridos (com receita)", primeira.size, "0"),
        ("Safras (cohorts)", dados["cohort"].nunique(), "0"),
        ("Receita total no período", float(df["receita"].sum()), MOEDA0),
        (f"Receita em {mes_txt(fim)}", float(df[df["mes"] == fim]["receita"].sum()), MOEDA0),
        (f"Clientes ativos em {mes_txt(fim)}", int(sum(1 for c in cli["cliente"] if (c, fim) in ativos_cm)), "0"),
        ("LTV médio por cliente adquirido", float(df["receita"].sum()) / primeira.size, MOEDA0),
    ]
    for k in (1, 3, 6, 12):
        if k <= max_idx:
            v = ret_pond(k)
            if v is not None:
                ind.append((f"Retenção no mês {k} (ponderada)", v, "0%"))
    cab(ws, 4, ["Indicador", "Valor"], [40, 18])
    r = 5
    for a, v, f in ind:
        ws.cell(row=r, column=1, value=a)
        ws.cell(row=r, column=2, value=v).number_format = f
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Safras por receita acumulada").font = Font(bold=True, color=MARROM)
    r += 1
    cab(ws, r, ["Cohort", "Clientes", "Receita acumulada", "LTV por cliente", "Retenção atual"], [40, 18, 18, 16, 14])
    r += 1
    ult = dados.sort_values("mes").groupby("cohort").tail(1)
    tot = dados.groupby("cohort")["receita"].sum()
    for coh in tot.sort_values(ascending=False).index:
        linha = ult[ult["cohort"] == coh].iloc[0]
        ws.cell(row=r, column=1, value=mes_txt(coh))
        ws.cell(row=r, column=2, value=int(linha["clientes_cohort"]))
        ws.cell(row=r, column=3, value=float(tot[coh])).number_format = MOEDA0
        ws.cell(row=r, column=4, value=float(tot[coh]) / linha["clientes_cohort"]).number_format = MOEDA0
        ws.cell(row=r, column=5, value=linha["clientes_ativos"] / linha["clientes_cohort"]).number_format = "0%"
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="CAC, LTV/CAC e payback aparecem nas abas de matriz assim que a aba Investimento for preenchida.").font = F_SUB


def aba_auditoria(wb, dados, df, primeira, fim, base_bruta):
    ws = wb.create_sheet("Auditoria")
    tit(ws, "Testes de conferência", "Cada teste recalcula um número por outro caminho e compara com o modelo.")
    cab(ws, 4, ["Teste", "Esperado", "Obtido", "Como foi conferido", "Resultado"], [36, 18, 18, 60, 12])
    testes = []
    rec_bruta = float(base_bruta["receita"].sum())
    rec_mod = float(dados["receita"].sum())
    testes.append(("Receita total do período", rec_bruta, rec_mod, "Soma da receita da base, sem passar pelas safras", abs(rec_bruta - rec_mod) < 0.01))
    n_cli = base_bruta[base_bruta["receita"] > 0]["cliente"].nunique()
    n_mod = int(dados.groupby("cohort")["clientes_cohort"].first().sum())
    testes.append(("Clientes: soma das safras", n_cli, n_mod, "Clientes com pelo menos um mês de receita maior que zero", n_cli == n_mod))
    rec_fim = float(base_bruta[base_bruta["mes"] == fim]["receita"].sum())
    rec_fim_mod = float(dados[dados["mes"] == fim]["receita"].sum())
    testes.append((f"Receita de {mes_txt(fim)}", rec_fim, rec_fim_mod, "Soma da base no último mês", abs(rec_fim - rec_fim_mod) < 0.01))
    mx = float((dados["clientes_ativos"] / dados["clientes_cohort"]).max())
    testes.append(("Retenção nunca acima de 100%", "<= 100%", f"{mx:.0%}", "Maior valor de ativos ÷ base em todas as linhas", mx <= 1.0000001))
    dup = int(primeira.index.duplicated().sum())
    testes.append(("Cada cliente em uma única safra", 0, dup, "Clientes repetidos entre safras", dup == 0))
    m0 = dados[dados["mes_indice"] == 0]
    ok0 = bool((m0["clientes_ativos"] == m0["clientes_cohort"]).all())
    testes.append(("Mês 0 com 100% dos clientes", "todas as safras", "todas" if ok0 else "há diferença", "Ativos no mês 0 = clientes da safra", ok0))
    r = 5
    for nome, esp, obt, como, ok in testes:
        ws.cell(row=r, column=1, value=nome)
        c1 = ws.cell(row=r, column=2, value=esp)
        c2 = ws.cell(row=r, column=3, value=obt)
        if isinstance(esp, float):
            c1.number_format = c2.number_format = MOEDA
        ws.cell(row=r, column=4, value=como).alignment = QUEBRA
        c = ws.cell(row=r, column=5, value="PASSOU" if ok else "FALHOU")
        c.fill = PatternFill("solid", fgColor=VERDE if ok else VERMELHO)
        r += 1
    ok_n = sum(1 for t in testes if t[4])
    ws.cell(row=r + 1, column=1, value=f"{ok_n} de {len(testes)} testes passaram.").font = Font(bold=True)
    # buracos de receita
    cm = base_bruta[base_bruta["receita"] > 0].groupby("cliente")["mes"].apply(sorted)
    voltas = [c for c, ms in cm.items() if any((b.year * 12 + b.month) - (a.year * 12 + a.month) > 1 for a, b in zip(ms, ms[1:]))]
    ws.cell(row=r + 3, column=1, value="Pontos de atenção").font = Font(bold=True, color=MARROM)
    ws.cell(row=r + 4, column=1, value=f"Clientes que pararam e voltaram a pagar: {len(voltas)}. Eles contam como inativos nos meses sem receita e voltam a contar quando retornam.").alignment = QUEBRA
    return testes


def aba_insights(wb, cfg):
    ins = cfg.get("insights")
    if not ins:
        return
    ws = wb.create_sheet("Insights", 2)
    tit(ws, "Leitura dos dados", "O que os números mostram, o que significa e o que fazer.")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 110
    r = 4
    for i, item in enumerate(ins, start=1):
        ws.cell(row=r, column=1, value=f"{i}. {item['titulo']}").font = Font(bold=True, color=MARROM)
        r += 1
        for rot in ("o_numero", "o_que_significa", "o_que_fazer"):
            if item.get(rot):
                ws.cell(row=r, column=1, value={"o_numero": "O número", "o_que_significa": "O que significa", "o_que_fazer": "O que fazer"}[rot]).font = Font(bold=True)
                ws.cell(row=r, column=2, value=item[rot]).alignment = QUEBRA
                r += 1
        r += 1


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    df = ler_base(cfg)
    dados, df, primeira, fim = montar_dados(df, cfg)
    cohorts = sorted(dados["cohort"].unique())
    cohorts = [pd.Timestamp(c) for c in cohorts]
    max_idx = int(dados["mes_indice"].max())
    tem_qtd = "qtd" in df and dados["qtd"].notna().any()

    wb = Workbook()
    aba_leia_me(wb, cfg, fim, dados)
    aba_resumo(wb, cfg, dados, df, primeira, fim, max_idx)
    aba_insights(wb, cfg)
    aba_premissas(wb, cfg)
    n_inv = aba_investimento(wb, cfg, cohorts)
    n_dados = aba_dados(wb, dados, n_inv, tem_qtd)
    linhas = {(pd.Timestamp(c), int(k)): i for i, (c, k) in enumerate(zip(dados["cohort"], dados["mes_indice"]), start=2)}
    for nome, col, fmt, sub in MATRIZES:
        aba_matriz(wb, nome, col, fmt, sub, cohorts, max_idx, linhas, tem_qtd)
    segs = cfg.get("segmentos", {})
    for nome in segs:
        aba_segmento(wb, f"Por {nome.capitalize()}", f"seg_{nome}", df, primeira, fim, max_idx, f"Retenção e receita por {nome}.")
    faixas = cfg.get("faixas_ticket")
    if faixas:
        pico = df[df["receita"] > 0].groupby(["cliente", "mes"])["receita"].sum().groupby("cliente").max()
        fx = [(f["nome"], f.get("ate")) for f in faixas]
        df["seg_faixa"] = df["cliente"].map(lambda c: faixa_ticket(pico.get(c, 0), fx))
        aba_segmento(wb, "Por Faixa de Ticket", "seg_faixa", df, primeira, fim, max_idx, "Faixa pelo maior valor mensal (pico) de cada cliente.")
    testes = aba_auditoria(wb, dados, df, primeira, fim, df)
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
    wb.save(sys.argv[2])
    ok = sum(1 for t in testes if t[4])
    print(f"Análise criada: {sys.argv[2]} | {primeira.size} clientes, {len(cohorts)} safras, até mês {max_idx} | testes: {ok}/{len(testes)} passaram")


if __name__ == "__main__":
    main()
