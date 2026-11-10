#!/usr/bin/env python3
"""Monta a planilha do Planejamento Estratégico (.xlsx) a partir de um config JSON.

Uso:
    python3 montar_planejamento.py config.json saida.xlsx

Abas: Casa da Estratégia, Contexto, Jornada, Fases e Métricas, Árvore de Objetivos,
OKR da Área (acompanhamento mensal com status), OKR por Pessoa (pesos com checagem de 100%),
Perguntas e Cenários.

Método de Jaqueline Amaro (CC BY-NC 4.0). Requer: openpyxl.
"""
import json
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ESCURO = "2B2B2B"
VINHO = "7A5560"
CREME = "FFF8E9"
CINZA = "EFEAE4"
VERDE = "B9DFB3"
AMARELO = "FBE3C8"
VERMELHO = "F4B6AE"
F_TIT = Font(bold=True, size=16, color=ESCURO)
F_SUB = Font(italic=True, color="756359")
F_BRANCA = Font(bold=True, color="FFFFFF")
FILL_ESC = PatternFill("solid", fgColor=ESCURO)
FILL_VINHO = PatternFill("solid", fgColor=VINHO)
FILL_IN = PatternFill("solid", fgColor=CREME)
FILL_CALC = PatternFill("solid", fgColor=CINZA)
QUEBRA = Alignment(wrap_text=True, vertical="top")
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
BORDA = Border(*(Side(style="thin", color="D9CFC4"),) * 4)
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def tit(ws, t, sub=None):
    ws["A1"] = t
    ws["A1"].font = F_TIT
    if sub:
        ws["A2"] = sub
        ws["A2"].font = F_SUB


def rotulo(ws, r, c, texto, fill=FILL_ESC):
    cel = ws.cell(row=r, column=c, value=texto)
    cel.font = F_BRANCA
    cel.fill = fill
    cel.alignment = CENTRO
    return cel


def caixa(ws, r, c, texto, fill=FILL_IN, merge_ate=None, altura=None):
    cel = ws.cell(row=r, column=c, value=texto)
    cel.alignment = QUEBRA
    cel.fill = fill
    cel.border = BORDA
    if merge_ate:
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=merge_ate)
    if altura:
        ws.row_dimensions[r].height = altura
    return cel


def lista_txt(v):
    if isinstance(v, list):
        return "\n".join(f"• {x}" for x in v)
    return v or ""


def aba_casa(wb, cfg):
    ws = wb.active
    ws.title = "Casa da Estratégia"
    c = cfg.get("casa", {})
    tit(ws, f"Casa da Estratégia — {cfg.get('area', 'Área')}", "Missão e valores da empresa conectados à estratégia da área. Tudo abaixo se desdobra em OKRs.")
    ws.column_dimensions["A"].width = 16
    for col in "BCDE":
        ws.column_dimensions[col].width = 34
    linhas = [
        ("Missão", c.get("missao"), 40),
        ("Visão", c.get("visao"), 40),
        ("Metas", lista_txt(c.get("metas")), 110),
    ]
    r = 4
    for nome, txt, h in linhas:
        rotulo(ws, r, 1, nome)
        caixa(ws, r, 2, txt, merge_ate=5, altura=h)
        r += 1
    rotulo(ws, r, 1, "Enablers")
    enablers = c.get("enablers") or {"Processo": [], "Experiência": [], "Produto": [], "Pessoas": []}
    for k, (nome, itens) in enumerate(list(enablers.items())[:4], start=2):
        caixa(ws, r, k, f"{nome}\n{lista_txt(itens)}")
        ws.cell(row=r, column=k).font = Font(bold=False)
    ws.row_dimensions[r].height = 120
    r += 1
    rotulo(ws, r, 1, "Fundamento")
    caixa(ws, r, 2, c.get("fundamento"), merge_ate=5, altura=36)
    ws.cell(row=r + 2, column=1, value="Como ler: a missão é o teto (por que existimos), a visão é onde queremos chegar, as metas são os resultados do período, os enablers são as colunas que sustentam as metas (o que precisa existir) e o fundamento é a base (cultura e princípios).").alignment = QUEBRA
    ws.merge_cells(start_row=r + 2, start_column=1, end_row=r + 2, end_column=5)
    ws.row_dimensions[r + 2].height = 46


def aba_contexto(wb, cfg):
    ws = wb.create_sheet("Contexto")
    tit(ws, "Contexto do projeto", "O que garante que todo mundo está olhando para a mesma solução.")
    ctx = cfg.get("contexto", {})
    blocos = [
        ("Sobre o projeto", "sobre"), ("Dados que existem", "dados"), ("Ferramentas e sistemas", "ferramentas"),
        ("Fora do escopo e premissas", "fora_escopo"), ("Como o cliente se comporta hoje", "comportamento_cliente"),
        ("Como deveria ser", "como_deveria_ser"), ("Dores da área", "dores_area"),
        ("Partes interessadas", "stakeholders"), ("Necessidades", "necessidades"),
        ("Integrações", "integracoes"), ("Entregáveis", "entregaveis"),
    ]
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 100
    for i, (nome, chave) in enumerate(blocos, start=4):
        rotulo(ws, i, 1, nome)
        caixa(ws, i, 2, lista_txt(ctx.get(chave)), altura=48)


def aba_jornada(wb, cfg):
    ws = wb.create_sheet("Jornada")
    j = cfg.get("jornada", {})
    etapas = j.get("etapas") or ["Busca", "Primeiro contato", "Compra", "Uso", "Recompra", "Saída"]
    tit(ws, "Jornada do cliente de ponta a ponta", "Uma coluna por etapa. Inclua os canais: é onde o CRM enxerga e age.")
    linhas = ["Sentimento", "Citações reais", "Pontos de contato e canais", "Tarefas do cliente", "Dores",
              "Oportunidades (CRM / CX)", "Momento da verdade", "Métrica", "Duração da etapa"]
    ws.column_dimensions["A"].width = 26
    rotulo(ws, 4, 1, "Etapas")
    for k, e in enumerate(etapas, start=2):
        rotulo(ws, 4, k, e, FILL_VINHO)
        ws.column_dimensions[get_column_letter(k)].width = 28
    campos = j.get("campos", {})
    for i, linha in enumerate(linhas, start=5):
        rotulo(ws, i, 1, linha)
        for k, e in enumerate(etapas, start=2):
            caixa(ws, i, k, campos.get(e, {}).get(linha, ""), altura=58)
    dv = DataValidation(type="list", formula1='"★ Momento da verdade,—"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"B11:{get_column_letter(1+len(etapas))}11")


def aba_fases(wb, cfg):
    ws = wb.create_sheet("Fases e Métricas")
    f = cfg.get("fases", {})
    fases = f.get("fases") or [{"nome": "Captação", "publico": "Novos clientes"}, {"nome": "Maximização de valor", "publico": "Clientes ativos"}, {"nome": "Retenção / recuperação", "publico": "Sem compra há muito tempo / saindo"}]
    tit(ws, "Fases do ciclo e métricas", "INPUT = o que o time controla diretamente (causa). OUTPUT = o resultado que essas ações geram (consequência). Não misture.")
    ws.column_dimensions["A"].width = 30
    rotulo(ws, 4, 1, "Fase")
    for k, fa in enumerate(fases, start=2):
        rotulo(ws, 4, k, f"{fa['nome']}\n{fa.get('publico', '')}", FILL_VINHO)
        ws.column_dimensions[get_column_letter(k)].width = 36
    ws.row_dimensions[4].height = 36
    linhas = [("KPI de OUTPUT (principal)", "output"), ("KPI de INPUT (principal)", "input"), ("Indicadores secundários", "secundarios"), ("Indicadores de saúde", "saude"), ("Ações prioritárias", "acoes")]
    for i, (nome, chave) in enumerate(linhas, start=5):
        rotulo(ws, i, 1, nome)
        for k, fa in enumerate(fases, start=2):
            caixa(ws, i, k, lista_txt(fa.get(chave)), altura=60)
    r = 5 + len(linhas) + 1
    ws.cell(row=r, column=1, value="Objetivo da área").font = Font(bold=True)
    caixa(ws, r, 2, f.get("objetivo_area", ""), merge_ate=1 + len(fases), altura=30)


def aba_arvore(wb, cfg):
    ws = wb.create_sheet("Árvore de Objetivos")
    a = cfg.get("arvore", {})
    tit(ws, "Árvore de objetivos", "Objetivo central → pilares (um de INPUT, um de OUTPUT) → grupos → objetivo e key results de cada grupo.")
    cols = ["Nível", "Pilar", "Grupo", "Objetivo", "Key results", "Métrica / KPI ligado"]
    larg = [12, 22, 22, 40, 50, 26]
    for k, (cname, w) in enumerate(zip(cols, larg), start=1):
        rotulo(ws, 4, k, cname)
        ws.column_dimensions[get_column_letter(k)].width = w
    r = 5
    caixa(ws, r, 1, "Central")
    caixa(ws, r, 4, a.get("objetivo_central", ""))
    caixa(ws, r, 5, lista_txt(a.get("okrs_central")))
    for k in (2, 3, 6):
        caixa(ws, r, k, "")
    ws.row_dimensions[r].height = 46
    r += 1
    for p in a.get("pilares", []):
        caixa(ws, r, 1, "Pilar")
        caixa(ws, r, 2, p.get("nome"))
        caixa(ws, r, 3, "")
        caixa(ws, r, 4, p.get("objetivo"))
        caixa(ws, r, 5, lista_txt(p.get("krs")))
        caixa(ws, r, 6, p.get("tipo", ""))
        ws.row_dimensions[r].height = 40
        r += 1
        for g in p.get("grupos", []):
            caixa(ws, r, 1, "Grupo")
            caixa(ws, r, 2, p.get("nome"))
            caixa(ws, r, 3, g.get("nome"))
            caixa(ws, r, 4, g.get("objetivo"))
            caixa(ws, r, 5, lista_txt(g.get("krs")))
            caixa(ws, r, 6, g.get("metrica", ""))
            ws.row_dimensions[r].height = 40
            r += 1
    ws.cell(row=r + 1, column=1, value="Para ver como árvore desenhada, peça o diagrama (Mermaid, Miro ou FigJam).").font = F_SUB


def aba_okr(wb, cfg):
    ws = wb.create_sheet("OKR da Área")
    o = cfg.get("okr", {})
    c = cfg.get("casa", {})
    tit(ws, f"OKRs — modelo de acompanhamento {cfg.get('ano', '')}", "Preencha o realizado de cada mês. 'Atual' pega o último mês preenchido; o status compara com o alvo.")
    ws.column_dimensions["A"].width = 9
    ws.column_dimensions["B"].width = 9
    ws.column_dimensions["C"].width = 46
    meses = o.get("meses", MESES)
    c0 = 4
    for k in range(len(meses)):
        ws.column_dimensions[get_column_letter(c0 + k)].width = 8
    cA = c0 + len(meses)
    cols_fim = ["Atual", "Alvo", "Direção", "% do alvo", "Status"]
    for k, w in enumerate([9, 9, 12, 10, 12]):
        ws.column_dimensions[get_column_letter(cA + k)].width = w
    ultima = cA + len(cols_fim) - 1
    r = 4
    for nome, txt in (("MISSÃO", c.get("missao")), ("VISÃO", c.get("visao")), ("ESTRATÉGIA", o.get("estrategia"))):
        rotulo(ws, r, 1, nome, FILL_VINHO)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        caixa(ws, r, 3, txt, merge_ate=ultima, altura=30)
        r += 1
    r += 1
    rotulo(ws, r, 1, "Peso")
    rotulo(ws, r, 2, "Código")
    rotulo(ws, r, 3, "Objetivo / Key result")
    for k, m in enumerate(meses):
        rotulo(ws, r, c0 + k, m)
    for k, n in enumerate(cols_fim):
        rotulo(ws, r, cA + k, n)
    cab = r
    r += 1
    linhas_obj = []
    dv_dir = DataValidation(type="list", formula1='"Maior é melhor,Menor é melhor"', allow_blank=True)
    ws.add_data_validation(dv_dir)
    for i, obj in enumerate(o.get("objetivos", []), start=1):
        rotulo(ws, r, 1, obj.get("peso"), FILL_VINHO).number_format = "0%"
        rotulo(ws, r, 2, f"O{i}", FILL_VINHO)
        cel = ws.cell(row=r, column=3, value=obj.get("nome"))
        cel.font = F_BRANCA
        cel.fill = FILL_VINHO
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=cA - 1)
        linha_obj = r
        r += 1
        ini = r
        for j, kr in enumerate(obj.get("krs", []), start=1):
            ws.cell(row=r, column=1, value=kr.get("peso")).number_format = "0%"
            ws.cell(row=r, column=2, value=f"KR {i}.{j}")
            ws.cell(row=r, column=3, value=kr.get("nome")).alignment = QUEBRA
            for k in range(len(meses)):
                cel = ws.cell(row=r, column=c0 + k, value=(kr.get("realizado") or {}).get(meses[k]))
                cel.fill = FILL_IN
                cel.border = BORDA
            fx = get_column_letter(c0)
            lx = get_column_letter(cA - 1)
            atual = get_column_letter(cA)
            alvo = get_column_letter(cA + 1)
            dire = get_column_letter(cA + 2)
            pct = get_column_letter(cA + 3)
            ws.cell(row=r, column=cA, value=f'=IFERROR(LOOKUP(2,1/({fx}{r}:{lx}{r}<>""),{fx}{r}:{lx}{r}),"")').fill = FILL_CALC
            a = ws.cell(row=r, column=cA + 1, value=kr.get("alvo"))
            a.fill = FILL_IN
            d = ws.cell(row=r, column=cA + 2, value=kr.get("direcao", "Maior é melhor"))
            d.fill = FILL_IN
            dv_dir.add(d.coordinate)
            p = ws.cell(row=r, column=cA + 3, value=f'=IF(OR({atual}{r}="",N({alvo}{r})=0),"",IF({dire}{r}="Menor é melhor",{alvo}{r}/MAX({atual}{r},0.000001),{atual}{r}/{alvo}{r}))')
            p.number_format = "0%"
            p.fill = FILL_CALC
            s = ws.cell(row=r, column=cA + 4, value=f'=IF({pct}{r}="","",IF({pct}{r}>=1,"No alvo",IF({pct}{r}>=0.7,"Atenção","Fora")))')
            s.alignment = CENTRO
            if kr.get("formato"):
                for col in list(range(c0, cA + 2)):
                    ws.cell(row=r, column=col).number_format = kr["formato"]
            r += 1
        fim = r - 1
        # soma dos pesos dos KRs dentro do objetivo
        chk = ws.cell(row=linha_obj, column=cA + 3, value=f"=SUM(A{ini}:A{fim})")
        chk.number_format = "0%"
        chk.font = F_BRANCA
        chk.fill = FILL_VINHO
        ws.cell(row=linha_obj, column=cA + 4, value=f'=IF(ROUND(SUM(A{ini}:A{fim})-A{linha_obj},4)=0,"pesos ok","pesos ≠ peso do O")').font = F_BRANCA
        ws.cell(row=linha_obj, column=cA + 4).fill = FILL_VINHO
        linhas_obj.append(linha_obj)
    stat = get_column_letter(cA + 4)
    ws.conditional_formatting.add(f"{stat}{cab+1}:{stat}{r}", CellIsRule(operator="equal", formula=['"No alvo"'], fill=PatternFill("solid", fgColor=VERDE)))
    ws.conditional_formatting.add(f"{stat}{cab+1}:{stat}{r}", CellIsRule(operator="equal", formula=['"Atenção"'], fill=PatternFill("solid", fgColor=AMARELO)))
    ws.conditional_formatting.add(f"{stat}{cab+1}:{stat}{r}", CellIsRule(operator="equal", formula=['"Fora"'], fill=PatternFill("solid", fgColor=VERMELHO)))
    r += 1
    ws.cell(row=r, column=1, value="Soma dos pesos dos objetivos")
    soma = "+".join(f"A{x}" for x in linhas_obj) or "0"
    c1 = ws.cell(row=r, column=3, value=f"={soma}")
    c1.number_format = "0%"
    ws.conditional_formatting.add(f"C{r}", FormulaRule(formula=[f"ROUND(C{r},4)<>1"], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.conditional_formatting.add(f"C{r}", FormulaRule(formula=[f"ROUND(C{r},4)=1"], fill=PatternFill("solid", fgColor=VERDE)))
    ws.cell(row=r + 1, column=1, value="Status: No alvo (100% ou mais do alvo) · Atenção (70% a 99%) · Fora (abaixo de 70%). Para KR em que menor é melhor (churn, custo), a conta inverte.").font = F_SUB
    ws.freeze_panes = f"D{cab + 1}"
    return [(f"KR {i}.{j}", kr.get("nome")) for i, obj in enumerate(o.get("objetivos", []), start=1) for j, kr in enumerate(obj.get("krs", []), start=1)]


def aba_pessoas(wb, cfg, krs):
    ws = wb.create_sheet("OKR por Pessoa")
    p = cfg.get("pessoas", {})
    funcoes = p.get("funcoes") or ["Coordenação", "Analista de dados", "Especialista em automação", "Atendimento"]
    tit(ws, "OKRs desdobrados por pessoa", "Cada coluna é uma pessoa ou função, com o peso de cada KR. O total precisa bater com o peso esperado daquela pessoa. Cada KR precisa de pelo menos um dono.")
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 44
    rotulo(ws, 4, 1, "Código")
    rotulo(ws, 4, 2, "Key result")
    for k, f in enumerate(funcoes, start=3):
        rotulo(ws, 4, k, f, FILL_VINHO)
        ws.column_dimensions[get_column_letter(k)].width = 15
    cdonos = 3 + len(funcoes)
    rotulo(ws, 4, cdonos, "Nº de donos")
    ws.column_dimensions[get_column_letter(cdonos)].width = 11
    pesos = p.get("pesos", {})
    r = 5
    for cod, nome in krs:
        ws.cell(row=r, column=1, value=cod)
        ws.cell(row=r, column=2, value=nome).alignment = QUEBRA
        for k, f in enumerate(funcoes, start=3):
            cel = ws.cell(row=r, column=k, value=(pesos.get(f) or {}).get(cod))
            cel.number_format = "0%"
            cel.fill = FILL_IN
            cel.border = BORDA
        last = get_column_letter(cdonos - 1)
        ws.cell(row=r, column=cdonos, value=f'=COUNTIF(C{r}:{last}{r},">0")').fill = FILL_CALC
        r += 1
    fim = r - 1
    esperado = p.get("peso_esperado", {})
    ws.cell(row=r, column=2, value="Total de peso da pessoa").font = Font(bold=True)
    ws.cell(row=r + 1, column=2, value="Peso esperado (combinado com a pessoa)").font = Font(bold=True)
    ws.cell(row=r + 2, column=2, value="Diferença").font = Font(bold=True)
    for k, f in enumerate(funcoes, start=3):
        col = get_column_letter(k)
        c = ws.cell(row=r, column=k, value=f"=SUM({col}5:{col}{fim})")
        c.number_format = "0%"
        c.font = Font(bold=True)
        e = ws.cell(row=r + 1, column=k, value=esperado.get(f, 1))
        e.number_format = "0%"
        e.fill = FILL_IN
        d = ws.cell(row=r + 2, column=k, value=f"={col}{r}-{col}{r+1}")
        d.number_format = "+0%;-0%;0%"
    tot = f"C{r}:{get_column_letter(cdonos-1)}{r}"
    ws.conditional_formatting.add(tot, FormulaRule(formula=[f"ROUND(C{r}-C{r+1},4)<>0"], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.conditional_formatting.add(tot, FormulaRule(formula=[f"ROUND(C{r}-C{r+1},4)=0"], fill=PatternFill("solid", fgColor=VERDE)))
    dn = get_column_letter(cdonos)
    ws.conditional_formatting.add(f"{dn}5:{dn}{fim}", CellIsRule(operator="equal", formula=["0"], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.cell(row=r + 4, column=1, value="O peso esperado muda de pessoa para pessoa: quem divide o tempo com outra área pode ter 70% aqui; quem é 100% desta área, 100%. Vermelho no total: a soma não bate com o combinado. Vermelho em 'Nº de donos': KR sem ninguém responsável.").font = F_SUB


def aba_perguntas(wb, cfg):
    ws = wb.create_sheet("Perguntas e Cenários")
    q = cfg.get("perguntas", {})
    tit(ws, "IA como parceira de pensamento", "Antes de fechar o plano: perguntas que o time ainda não fez, objeções que vão aparecer e cenários 'e se'. O objetivo não é a resposta certa, é chegar na sala com perguntas melhores.")
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 70
    ws.column_dimensions["C"].width = 40
    blocos = [("Hipóteses a testar", "hipoteses"), ("Perguntas que o time ainda não está fazendo", "perguntas"), ("Objeções esperadas e resposta", "objecoes"), ("Cenários 'e se'", "cenarios"), ("Riscos e o que monitorar", "riscos")]
    r = 4
    for nome, chave in blocos:
        rotulo(ws, r, 1, nome)
        rotulo(ws, r, 2, "Item", FILL_VINHO)
        rotulo(ws, r, 3, "Como validar / próximo passo", FILL_VINHO)
        r += 1
        itens = q.get(chave) or [""] * 3
        for it in itens:
            if isinstance(it, dict):
                caixa(ws, r, 2, it.get("item"))
                caixa(ws, r, 3, it.get("validar"))
            else:
                caixa(ws, r, 2, it)
                caixa(ws, r, 3, "")
            r += 1
        r += 1


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    wb = Workbook()
    aba_casa(wb, cfg)
    aba_contexto(wb, cfg)
    aba_jornada(wb, cfg)
    aba_fases(wb, cfg)
    aba_arvore(wb, cfg)
    krs = aba_okr(wb, cfg)
    aba_pessoas(wb, cfg, krs)
    aba_perguntas(wb, cfg)
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
    ws_cred = wb["Casa da Estratégia"]
    ws_cred.cell(row=14, column=1, value="Método: Planejamento Estratégico, por Jaqueline Amaro (CC BY-NC 4.0). Casa da Estratégia (Strategy House): modelo de origem no Sistema Toyota.").font = F_SUB
    wb.save(sys.argv[2])
    print(f"Planejamento criado: {sys.argv[2]} ({', '.join(ws.title for ws in wb.worksheets)})")


if __name__ == "__main__":
    main()
