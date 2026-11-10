#!/usr/bin/env python3
"""Monta a Planilha de Growth (.xlsx) a partir de um arquivo de configuração JSON.

Uso:
    python3 montar_planilha.py config.json saida.xlsx

Criado por Jaqueline Amaro (CC BY-NC 4.0). Requer: openpyxl.
"""
import json
import sys
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

MARROM = "4B342C"
CREME = "FFF8E9"
MANTEIGA = "F5E4A0"
VERMELHO = "F8D7D3"
VERDE = "DCEFD9"
CINZA = "EFEAE4"

FONTE_TITULO = Font(bold=True, size=14, color=MARROM)
FONTE_CAB = Font(bold=True, color="FFFFFF")
FILL_CAB = PatternFill("solid", fgColor=MARROM)
FILL_ENTRADA = PatternFill("solid", fgColor=CREME)
FILL_CALCULO = PatternFill("solid", fgColor=CINZA)
BORDA = Border(bottom=Side(style="thin", color="D9CFC4"))
QUEBRA = Alignment(wrap_text=True, vertical="top")

STATUS_TAREFA = ["Não iniciada", "Em andamento", "Bloqueada", "Concluída"]
STATUS_DEMANDA = ["Pedido", "Em produção", "Em análise", "Ajustes", "Aprovado", "Publicado"]
STATUS_REGUA = ["Ideia", "Planejamento", "Em construção", "Ativa", "Pausada"]
STATUS_COMPRA = ["Orçar", "Orçado", "Aprovado", "Pago", "Entregue"]
STATUS_CONTATO = ["Mapeado", "Mensagem enviada", "Em conversa", "Aceito", "Recusado", "Sem resposta"]
STATUS_ENVIO = ["Não enviado", "Enviado", "Recebido", "Postou", "Não postou"]
CATEG_INFLU = ["UGC (permuta)", "Influenciador (pago)", "Presente", "Afiliado", "Embaixador"]
OBJETIVOS = ["Awareness", "Consideração", "Aquisição", "Retenção"]
TIPO_REGUA = ["Cadastral", "Transacional", "Relacional", "Promocional", "Datas e campanhas"]
TIPO_DATA = ["Feriado", "Data comemorativa", "Data comercial", "Evento interno"]


def cabecalho(ws, linha, colunas, larguras=None):
    for i, nome in enumerate(colunas, start=1):
        c = ws.cell(row=linha, column=i, value=nome)
        c.font = FONTE_CAB
        c.fill = FILL_CAB
        c.alignment = Alignment(wrap_text=True, vertical="center")
        if larguras:
            ws.column_dimensions[get_column_letter(i)].width = larguras[i - 1]
    ws.row_dimensions[linha].height = 32
    ws.freeze_panes = ws.cell(row=linha + 1, column=1)


def titulo(ws, texto, sub=None):
    ws["A1"] = texto
    ws["A1"].font = FONTE_TITULO
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, color="756359")


def lista(ws, opcoes, intervalo):
    dv = DataValidation(type="list", formula1='"' + ",".join(opcoes) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(intervalo)


def pintar(ws, intervalo, fill):
    for linha in ws[intervalo]:
        for c in linha:
            c.fill = fill
            c.border = BORDA


def formato(ws, intervalo, fmt):
    for linha in ws[intervalo]:
        for c in linha:
            c.number_format = fmt


# ---------- datas comerciais ----------
def pascoa(ano):
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)


def nth_dia_semana(ano, mes, dia_semana, n):
    d = date(ano, mes, 1)
    while d.weekday() != dia_semana:
        d += timedelta(days=1)
    return d + timedelta(weeks=n - 1)


def datas_do_ano(ano):
    p = pascoa(ano)
    bf = nth_dia_semana(ano, 11, 3, 4) + timedelta(days=1)  # dia seguinte à 4ª quinta
    datas = [
        (date(ano, 1, 1), "Ano Novo", "Feriado"),
        (p - timedelta(days=48), "Carnaval (segunda)", "Feriado"),
        (p - timedelta(days=47), "Carnaval (terça)", "Feriado"),
        (date(ano, 3, 8), "Dia Internacional da Mulher", "Data comemorativa"),
        (date(ano, 3, 15), "Dia do Consumidor", "Data comercial"),
        (p - timedelta(days=2), "Sexta-feira Santa", "Feriado"),
        (p, "Páscoa", "Data comemorativa"),
        (date(ano, 4, 21), "Tiradentes", "Feriado"),
        (date(ano, 5, 1), "Dia do Trabalho", "Feriado"),
        (nth_dia_semana(ano, 5, 6, 2), "Dia das Mães", "Data comemorativa"),
        (p + timedelta(days=60), "Corpus Christi", "Feriado"),
        (date(ano, 6, 12), "Dia dos Namorados", "Data comemorativa"),
        (date(ano, 6, 24), "São João", "Data comemorativa"),
        (date(ano, 7, 20), "Dia do Amigo", "Data comemorativa"),
        (nth_dia_semana(ano, 8, 6, 2), "Dia dos Pais", "Data comemorativa"),
        (date(ano, 9, 7), "Independência do Brasil", "Feriado"),
        (date(ano, 9, 15), "Dia do Cliente", "Data comercial"),
        (date(ano, 10, 12), "Dia das Crianças / N. Sra. Aparecida", "Feriado"),
        (date(ano, 10, 31), "Halloween", "Data comemorativa"),
        (date(ano, 11, 2), "Finados", "Feriado"),
        (date(ano, 11, 11), "11.11 (Dia dos Solteiros)", "Data comercial"),
        (date(ano, 11, 15), "Proclamação da República", "Feriado"),
        (date(ano, 11, 20), "Consciência Negra", "Feriado"),
        (bf, "Black Friday", "Data comercial"),
        (bf + timedelta(days=3), "Cyber Monday", "Data comercial"),
        (date(ano, 12, 25), "Natal", "Feriado"),
    ]
    return sorted(datas)


# ---------- abas ----------
def aba_como_usar(wb, cfg):
    ws = wb.active
    ws.title = "Como usar"
    titulo(ws, f"Planilha de Growth — {cfg['empresa']}", "Central de comando de growth: tarefas, calendário, preço, influenciadores, conteúdo, mídia, CRM e eventos.")
    linhas = [
        ("Células creme", "são para você preencher."),
        ("Células cinza", "têm fórmula: não precisa mexer."),
        ("Listas", "colunas de status, categoria e tipo têm opções prontas (clique na célula)."),
        ("Alertas", "linhas ficam vermelhas quando algo precisa de atenção (prazo vencido, margem abaixo do mínimo, estoque baixo)."),
        ("Dados pessoais", "não guarde CPF, endereço ou telefone de pessoas aqui se a planilha for compartilhada com muita gente (LGPD). Use um arquivo restrito para envios."),
        ("Ritmo", "revise Tarefas toda semana, Criativos e Influenciadores a cada 15 dias, Preço e margem a cada mudança de custo."),
    ]
    for i, (a, b) in enumerate(linhas, start=4):
        ws.cell(row=i, column=1, value=a).font = Font(bold=True)
        ws.cell(row=i, column=2, value=b).alignment = QUEBRA
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 110
    ws.cell(row=12, column=1, value="Criado com a skill Planilha de Growth, por Jaqueline Amaro (CC BY-NC 4.0).").font = Font(italic=True, color="756359")


TAREFAS_BASE = [
    ("Marca", "Definir história, missão e valores da marca"),
    ("Marca", "Definir posicionamento e proposta de valor"),
    ("Pesquisa de mercado", "Definir público-alvo e personas"),
    ("Pesquisa de mercado", "Mapear concorrentes (preço, diferenciais, promoções)"),
    ("Preço", "Calcular custo de cada produto"),
    ("Preço", "Definir preço, margem mínima e espaço para cupom"),
    ("Identidade visual", "Adaptar identidade visual para redes, site e embalagem"),
    ("Conteúdo", "Criar banco de imagens e vídeos de produto"),
    ("Redes sociais", "Definir objetivos e KPIs por rede"),
    ("Redes sociais", "Criar linha editorial e calendário de conteúdo"),
    ("Mídia paga", "Escrever briefings de criativos por objetivo"),
    ("Mídia paga", "Configurar pixel, eventos e catálogo de produtos"),
    ("Influenciadores", "Montar lista de desejos de influenciadores e UGC"),
    ("Influenciadores", "Definir regras de parceria, cupons e programa de afiliados"),
    ("CRM", "Mapear e priorizar as réguas (cadastral, transacional, relacional)"),
    ("Site / e-commerce", "Revisar jornada de compra, frete e meios de pagamento"),
    ("Eventos e ativações", "Planejar ativações e orçar materiais"),
    ("Acompanhamento", "Marcar reunião semanal de resultados do time"),
]


def aba_tarefas(wb, cfg):
    ws = wb.create_sheet("Tarefas")
    titulo(ws, "Tarefas por frente", "Uma linha por tarefa. A linha fica vermelha quando o prazo passou e a tarefa não foi concluída.")
    cols = ["Frente", "Tarefa", "Status", "Responsável", "Início", "Prazo", "Próximo passo", "Bloqueios / pendências", "Links"]
    cabecalho(ws, 4, cols, [20, 48, 15, 16, 12, 12, 34, 30, 30])
    tarefas = cfg.get("tarefas") or TAREFAS_BASE
    n = max(len(tarefas) + 20, 60)
    for i, (frente, tarefa) in enumerate(tarefas, start=5):
        ws.cell(row=i, column=1, value=frente)
        ws.cell(row=i, column=2, value=tarefa)
        ws.cell(row=i, column=3, value="Não iniciada")
    pintar(ws, f"A5:I{n+4}", FILL_ENTRADA)
    formato(ws, f"E5:F{n+4}", "DD/MM/YYYY")
    lista(ws, STATUS_TAREFA, f"C5:C{n+4}")
    if cfg.get("responsaveis"):
        lista(ws, cfg["responsaveis"], f"D5:D{n+4}")
    ws.conditional_formatting.add(f"A5:I{n+4}", FormulaRule(formula=['AND($F5<>"",$F5<TODAY(),$C5<>"Concluída")'], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.conditional_formatting.add(f"A5:I{n+4}", FormulaRule(formula=['$C5="Concluída"'], fill=PatternFill("solid", fgColor=VERDE)))
    ws.auto_filter.ref = f"A4:I{n+4}"


def aba_calendario(wb, cfg):
    ws = wb.create_sheet("Calendário")
    ano = cfg["ano"]
    titulo(ws, f"Calendário comercial {ano}", "Datas do Brasil já preenchidas. Acrescente eventos internos (lançamentos, aniversário da marca) e a ação de cada data.")
    cols = ["Data", "Dia da semana", "Mês", "Data / evento", "Tipo", "Ação ou promoção", "Canais", "Começar a preparar em", "Status"]
    cabecalho(ws, 4, cols, [12, 14, 8, 34, 18, 40, 22, 18, 15])
    datas = datas_do_ano(ano) + [(date.fromisoformat(d["data"]), d["nome"], "Evento interno") for d in cfg.get("eventos_internos", [])]
    datas.sort()
    n = len(datas) + 15
    for i, (d, nome, tipo) in enumerate(datas, start=5):
        ws.cell(row=i, column=1, value=d)
        ws.cell(row=i, column=4, value=nome)
        ws.cell(row=i, column=5, value=tipo)
    for r in range(5, n + 5):
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",CHOOSE(WEEKDAY(A{r}),"domingo","segunda","terça","quarta","quinta","sexta","sábado"))')
        ws.cell(row=r, column=3, value=f'=IF(A{r}="","",MONTH(A{r}))')
        ws.cell(row=r, column=8, value=f'=IF(A{r}="","",A{r}-30)')
    pintar(ws, f"A5:I{n+4}", FILL_ENTRADA)
    pintar(ws, f"B5:C{n+4}", FILL_CALCULO)
    pintar(ws, f"H5:H{n+4}", FILL_CALCULO)
    formato(ws, f"A5:A{n+4}", "DD/MM/YYYY")
    formato(ws, f"H5:H{n+4}", "DD/MM/YYYY")
    lista(ws, TIPO_DATA, f"E5:E{n+4}")
    lista(ws, STATUS_TAREFA, f"I5:I{n+4}")
    ws.conditional_formatting.add(f"A5:I{n+4}", FormulaRule(formula=['$E5="Data comercial"'], fill=PatternFill("solid", fgColor=MANTEIGA)))
    ws.auto_filter.ref = f"A4:I{n+4}"


def aba_custos(wb, cfg):
    ws = wb.create_sheet("Custo do produto")
    titulo(ws, "Custo de cada produto", "Preencha os custos por unidade. O custo total soma tudo e aplica o imposto.")
    cols = ["Produto", "Matéria-prima", "Embalagem", "Mão de obra / produção", "Frete até o estoque", "Outros", "Subtotal", "Imposto %", "Custo total"]
    cabecalho(ws, 4, cols, [38, 14, 14, 16, 16, 12, 14, 11, 14])
    produtos = cfg.get("produtos", [])
    n = max(len(produtos) + 10, 20)
    for i, p in enumerate(produtos, start=5):
        ws.cell(row=i, column=1, value=p["nome"])
        for j, k in enumerate(["materia_prima", "embalagem", "mao_de_obra", "frete", "outros"], start=2):
            if k in p:
                ws.cell(row=i, column=j, value=p[k])
    for r in range(5, n + 5):
        ws.cell(row=r, column=7, value=f'=IF(A{r}="","",SUM(B{r}:F{r}))')
        if ws.cell(row=r, column=8).value is None:
            ws.cell(row=r, column=8, value=cfg.get("imposto", 0.08) if r < 5 + len(produtos) else None)
        ws.cell(row=r, column=9, value=f'=IF(A{r}="","",G{r}*(1+H{r}))')
    pintar(ws, f"A5:H{n+4}", FILL_ENTRADA)
    pintar(ws, f"G5:G{n+4}", FILL_CALCULO)
    pintar(ws, f"I5:I{n+4}", FILL_CALCULO)
    formato(ws, f"B5:G{n+4}", '"R$" #,##0.00')
    formato(ws, f"I5:I{n+4}", '"R$" #,##0.00')
    formato(ws, f"H5:H{n+4}", "0%")
    ws.cell(row=n + 6, column=1, value="Dica: para custos que chegam em lote (frete de 3.000 latas, 500 envelopes), divida o valor total pela quantidade e lance o valor por unidade.").font = Font(italic=True, color="756359")
    return n


def aba_preco(wb, cfg, n_custos):
    ws = wb.create_sheet("Preço e margem")
    titulo(ws, "Preço e margem", "O custo vem da aba Custo do produto. Você define a margem mínima e o preço final; a planilha mostra a margem real, inclusive com cupom.")
    cols = ["Produto", "Custo total", "Margem mínima %", "Preço mínimo", "Espaço p/ cupom %", "Preço sugerido", "Preço final de venda", "Margem real %", "Cupom mais usado %", "Preço com cupom", "Margem com cupom %", "Observações / combos"]
    cabecalho(ws, 4, cols, [38, 13, 12, 13, 12, 13, 14, 12, 12, 13, 13, 34])
    produtos = cfg.get("produtos", [])
    n = n_custos
    for r in range(5, n + 5):
        ws.cell(row=r, column=1, value=f"='Custo do produto'!A{r}")
        ws.cell(row=r, column=2, value=f"=IF('Custo do produto'!A{r}=\"\",\"\",'Custo do produto'!I{r})")
        idx = r - 5
        if idx < len(produtos):
            ws.cell(row=r, column=3, value=cfg.get("margem_minima", 0.5))
            ws.cell(row=r, column=5, value=cfg.get("espaco_cupom", 0.2))
            ws.cell(row=r, column=9, value=cfg.get("cupom_padrao", 0.15))
            if "preco_final" in produtos[idx]:
                ws.cell(row=r, column=7, value=produtos[idx]["preco_final"])
        ws.cell(row=r, column=4, value=f'=IF(OR(B{r}="",C{r}=""),"",B{r}/(1-C{r}))')
        ws.cell(row=r, column=6, value=f'=IF(D{r}="","",D{r}*(1+E{r}))')
        ws.cell(row=r, column=8, value=f'=IF(OR(G{r}="",B{r}=""),"",(G{r}-B{r})/G{r})')
        ws.cell(row=r, column=10, value=f'=IF(G{r}="","",G{r}*(1-I{r}))')
        ws.cell(row=r, column=11, value=f'=IF(OR(J{r}="",B{r}=""),"",(J{r}-B{r})/J{r})')
    pintar(ws, f"A5:L{n+4}", FILL_ENTRADA)
    for col in ["A", "B", "D", "F", "H", "J", "K"]:
        pintar(ws, f"{col}5:{col}{n+4}", FILL_CALCULO)
    formato(ws, f"B5:B{n+4}", '"R$" #,##0.00')
    formato(ws, f"D5:D{n+4}", '"R$" #,##0.00')
    formato(ws, f"F5:G{n+4}", '"R$" #,##0.00')
    formato(ws, f"J5:J{n+4}", '"R$" #,##0.00')
    for col in ["C", "E", "H", "I", "K"]:
        formato(ws, f"{col}5:{col}{n+4}", "0.0%")
    ws.conditional_formatting.add(f"G5:K{n+4}", FormulaRule(formula=['AND($K5<>"",$C5<>"",$K5<$C5)'], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.cell(row=n + 6, column=1, value="Vermelho = com o cupom mais usado, a margem fica abaixo da mínima. Revise o preço, o cupom ou o custo.").font = Font(italic=True, color="756359")


def aba_concorrentes(wb, cfg):
    ws = wb.create_sheet("Concorrentes")
    titulo(ws, "Comparação com concorrentes", "Preço por unidade de medida (g, ml, cápsula) para comparar produtos de tamanhos diferentes.")
    cols = ["Marca", "Produto", "Tamanho", "Unidade (g, ml, un)", "Preço", "Preço por unidade", "Diferenciais na embalagem", "Promoções no site", "Canal", "Link", "Data da consulta"]
    cabecalho(ws, 4, cols, [18, 34, 10, 12, 12, 14, 36, 36, 14, 30, 14])
    conc = cfg.get("concorrentes", [])
    n = max(len(conc) + 15, 30)
    for i, c in enumerate(conc, start=5):
        for j, k in enumerate(["marca", "produto", "tamanho", "unidade", "preco"], start=1):
            if k in c:
                ws.cell(row=i, column=j, value=c[k])
    for r in range(5, n + 5):
        ws.cell(row=r, column=6, value=f'=IF(OR(C{r}="",E{r}=""),"",E{r}/C{r})')
    pintar(ws, f"A5:K{n+4}", FILL_ENTRADA)
    pintar(ws, f"F5:F{n+4}", FILL_CALCULO)
    formato(ws, f"E5:E{n+4}", '"R$" #,##0.00')
    formato(ws, f"F5:F{n+4}", '"R$" #,##0.000')
    formato(ws, f"K5:K{n+4}", "DD/MM/YYYY")
    ws.auto_filter.ref = f"A4:K{n+4}"


def aba_influs(wb, cfg):
    ws = wb.create_sheet("Influenciadores")
    titulo(ws, "Influenciadores, UGC e afiliados", "Do mapeamento ao resultado. O retorno é calculado pelas vendas com o cupom de cada pessoa.")
    cols = ["Categoria", "Nome / @", "Nicho", "Seguidores", "Engajamento %", "Rede", "Responsável", "Status do contato", "Acordo (entregas)", "Valor pago", "Custo de produto enviado", "Cupom", "Status do envio", "Rastreio", "Data do post", "Link do post", "Vendas com cupom (pedidos)", "Receita com cupom", "Custo total", "Retorno (receita ÷ custo)"]
    cabecalho(ws, 4, cols, [18, 24, 20, 11, 11, 10, 14, 16, 30, 11, 13, 14, 13, 16, 12, 26, 12, 13, 12, 12])
    n = 80
    for r in range(5, n + 5):
        ws.cell(row=r, column=19, value=f'=IF(B{r}="","",N(J{r})+N(K{r}))')
        ws.cell(row=r, column=20, value=f'=IF(OR(S{r}="",S{r}=0,R{r}=""),"",R{r}/S{r})')
    pintar(ws, f"A5:T{n+4}", FILL_ENTRADA)
    pintar(ws, f"S5:T{n+4}", FILL_CALCULO)
    lista(ws, CATEG_INFLU, f"A5:A{n+4}")
    lista(ws, STATUS_CONTATO, f"H5:H{n+4}")
    lista(ws, STATUS_ENVIO, f"M5:M{n+4}")
    lista(ws, ["Instagram", "TikTok", "YouTube", "Kwai", "LinkedIn", "Outra"], f"F5:F{n+4}")
    if cfg.get("responsaveis"):
        lista(ws, cfg["responsaveis"], f"G5:G{n+4}")
    formato(ws, f"E5:E{n+4}", "0.0%")
    formato(ws, f"J5:K{n+4}", '"R$" #,##0.00')
    formato(ws, f"R5:S{n+4}", '"R$" #,##0.00')
    formato(ws, f"T5:T{n+4}", '0.0"x"')
    formato(ws, f"O5:O{n+4}", "DD/MM/YYYY")
    ws.conditional_formatting.add(f"A5:T{n+4}", FormulaRule(formula=['AND($M5="Recebido",$O5="")'], fill=PatternFill("solid", fgColor=MANTEIGA)))
    ws.auto_filter.ref = f"A4:T{n+4}"
    ws.cell(row=n + 6, column=1, value="Amarelo = recebeu o produto e ainda não postou: hora de lembrar. Endereços e telefones: guarde num arquivo restrito (LGPD).").font = Font(italic=True, color="756359")


def aba_regras_influs(wb, cfg):
    ws = wb.create_sheet("Regras de parceria")
    titulo(ws, "Regras de parceria com influenciadores", "Ajuste com as regras da sua marca. Todo mundo do time segue o mesmo caminho.")
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 70
    ws.column_dimensions["C"].width = 22
    r = 4
    ws.cell(row=r, column=1, value="Dicionário").font = Font(bold=True, size=12, color=MARROM)
    r += 1
    dic = [
        ("UGC (permuta)", "Recebe produto e tem acordo obrigatório de conteúdo (posts, vídeos para a marca usar)."),
        ("Influenciador (pago)", "Recebe pagamento por entregas combinadas antes (quantidade, formato, datas)."),
        ("Presente", "Amigo da marca ou parceiro que recebe produto sem obrigação de postar."),
        ("Afiliado", "Divulga com link ou cupom próprio e ganha comissão por venda."),
        ("Embaixador", "Parceria longa, com exclusividade e entregas recorrentes."),
    ]
    for a, b in dic:
        ws.cell(row=r, column=1, value=a).font = Font(bold=True)
        ws.cell(row=r, column=2, value=b).alignment = QUEBRA
        r += 1
    r += 1
    for titulo_fluxo, passos in [
        ("Fluxo: perfil indicado por alguém do time", [
            "Classificar: UGC, influenciador ou presente",
            "Analisar o perfil (seguidores, perfil aberto, engajamento, combina com a marca)",
            "Entender o que já foi combinado por quem indicou",
            "Sem combinado: seguir o fluxo do zero. Com combinado: seguir o combinado, criar o cupom e mandar o direcional",
        ]),
        ("Fluxo: pessoa pediu parceria (DM ou e-mail)", [
            "Classificar: UGC, influenciador ou presente",
            "Analisar o perfil",
            "Combinar valor x entregas",
            "Criar o cupom e enviar o produto com o código de rastreio",
            "Mandar o direcional de conteúdo",
            "Receber e aprovar os conteúdos, combinar as datas dos posts",
            "Acompanhar e devolver o resultado de vendas com o cupom",
        ]),
    ]:
        ws.cell(row=r, column=1, value=titulo_fluxo).font = Font(bold=True, size=12, color=MARROM)
        ws.cell(row=r, column=3, value="Responsável").font = Font(bold=True)
        r += 1
        for i, p in enumerate(passos, start=1):
            ws.cell(row=r, column=1, value=f"Passo {i}")
            ws.cell(row=r, column=2, value=p).alignment = QUEBRA
            ws.cell(row=r, column=3).fill = FILL_ENTRADA
            r += 1
        r += 1
    ws.cell(row=r, column=1, value="Regras antes de enviar produto").font = Font(bold=True, size=12, color=MARROM)
    r += 1
    for regra in ["Acordo de entregas registrado na aba Influenciadores", "Cupom criado e testado", "Produto com estoque", "Mensagem de envio com rastreio"]:
        ws.cell(row=r, column=2, value="☐ " + regra)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Programa de afiliados").font = Font(bold=True, size=12, color=MARROM)
    r += 1
    for j, h in enumerate(["Nível", "Comissão por venda", "Regra para entrar"], start=1):
        c = ws.cell(row=r, column=j, value=h)
        c.font = FONTE_CAB
        c.fill = FILL_CAB
    r += 1
    for nivel, com, regra in cfg.get("afiliados") or [("Bronze", 0.10, "Padrão, ao entrar"), ("Prata", 0.12, "Vende combos"), ("Ouro", 0.15, "Vende assinaturas / recorrência"), ("Platina", None, "Acima de R$ ___ por mês")]:
        ws.cell(row=r, column=1, value=nivel)
        c = ws.cell(row=r, column=2, value=com)
        c.number_format = "0%"
        ws.cell(row=r, column=3, value=regra)
        pintar(ws, f"A{r}:C{r}", FILL_ENTRADA)
        r += 1


def aba_demandas(wb, cfg):
    ws = wb.create_sheet("Demandas de conteúdo")
    titulo(ws, "Demandas de conteúdo e peças", "Tudo que alguém pediu para o design ou para o conteúdo: banners, posts, cartas, embalagens, landing pages.")
    cols = ["Peça / conteúdo", "Tipo (site, rede, impresso, e-mail)", "Formato / tamanho", "Detalhes e texto", "Quem pediu", "Responsável", "Status", "Prazo", "Referência", "Link da entrega", "Observações"]
    cabecalho(ws, 4, cols, [30, 18, 22, 40, 14, 14, 14, 12, 26, 26, 26])
    n = 60
    pintar(ws, f"A5:K{n+4}", FILL_ENTRADA)
    lista(ws, STATUS_DEMANDA, f"G5:G{n+4}")
    formato(ws, f"H5:H{n+4}", "DD/MM/YYYY")
    ws.conditional_formatting.add(f"A5:K{n+4}", FormulaRule(formula=['AND($H5<>"",$H5<TODAY(),$G5<>"Aprovado",$G5<>"Publicado")'], fill=PatternFill("solid", fgColor=VERMELHO)))
    ws.auto_filter.ref = f"A4:K{n+4}"


def aba_briefing(wb, cfg):
    ws = wb.create_sheet("Briefing de criativos")
    titulo(ws, "Briefing de criativos para anúncios", "Uma linha por criativo pedido. Deixe claro o objetivo, o ângulo e a referência.")
    cols = ["Objetivo", "Plataformas", "Formato", "Medidas", "Regras do criativo", "Ângulo / o que mostrar", "Referências (links)", "O que o criativo precisa fazer a pessoa sentir ou entender", "Status"]
    cabecalho(ws, 4, cols, [14, 22, 12, 26, 30, 26, 30, 44, 14])
    base = [
        ("Awareness", "Meta, TikTok, Google", "Vídeo", "1080x1920 / 1080x1080 / 1080x1350", "Até 15 s; pouco texto na tela", "Atributos do produto"),
        ("Awareness", "Meta, TikTok, Google", "Estático", "1200x1200 / 1200x628 / 960x1200", "Pouco texto na imagem", "Uso no dia a dia"),
        ("Consideração", "Meta, TikTok", "Vídeo", "1080x1920", "Até 30 s", "Prova social / depoimento"),
        ("Aquisição", "Meta, Google", "Estático", "1200x1200 / 1200x628 / 960x1200", "Oferta em destaque", "Promoção / frete grátis"),
        ("Aquisição", "Meta, TikTok", "Vídeo", "1080x1920 / 1080x1350", "Até 15 s", "Unboxing / combo"),
        ("Retenção", "Meta", "Estático", "1080x1080", "Personalizado para clientes", "Recompra / novidade"),
    ]
    n = 40
    for i, row in enumerate(base, start=5):
        for j, v in enumerate(row, start=1):
            ws.cell(row=i, column=j, value=v)
    pintar(ws, f"A5:I{n+4}", FILL_ENTRADA)
    for r in range(5, n + 5):
        for c in range(1, 10):
            ws.cell(row=r, column=c).alignment = QUEBRA
    lista(ws, OBJETIVOS, f"A5:A{n+4}")
    lista(ws, ["Vídeo", "Estático", "Carrossel", "Stories"], f"C5:C{n+4}")
    lista(ws, STATUS_DEMANDA, f"I5:I{n+4}")


def aba_criativos(wb, cfg):
    ws = wb.create_sheet("Criativos")
    titulo(ws, "Desempenho dos criativos", "Lance os números da plataforma de anúncios. CTR, custo por resultado e retorno saem sozinhos.")
    cols = ["Criativo", "Plataforma", "Objetivo", "Status", "Início", "Investimento", "Impressões", "Cliques", "CTR", "Conversões", "Custo por conversão", "Receita", "Retorno (ROAS)", "Link do anúncio", "O que aprendemos"]
    cabecalho(ws, 4, cols, [26, 12, 13, 11, 11, 13, 12, 10, 8, 11, 13, 13, 10, 26, 40])
    n = 60
    for r in range(5, n + 5):
        ws.cell(row=r, column=9, value=f'=IF(OR(G{r}="",G{r}=0),"",H{r}/G{r})')
        ws.cell(row=r, column=11, value=f'=IF(OR(J{r}="",J{r}=0),"",F{r}/J{r})')
        ws.cell(row=r, column=13, value=f'=IF(OR(F{r}="",F{r}=0,L{r}=""),"",L{r}/F{r})')
    pintar(ws, f"A5:O{n+4}", FILL_ENTRADA)
    for col in ["I", "K", "M"]:
        pintar(ws, f"{col}5:{col}{n+4}", FILL_CALCULO)
    lista(ws, OBJETIVOS, f"C5:C{n+4}")
    lista(ws, ["Ativo", "Pausado", "Em teste"], f"D5:D{n+4}")
    lista(ws, ["Meta", "TikTok", "Google", "YouTube", "Pinterest", "Outra"], f"B5:B{n+4}")
    formato(ws, f"E5:E{n+4}", "DD/MM/YYYY")
    formato(ws, f"F5:F{n+4}", '"R$" #,##0.00')
    formato(ws, f"K5:L{n+4}", '"R$" #,##0.00')
    formato(ws, f"I5:I{n+4}", "0.00%")
    formato(ws, f"M5:M{n+4}", '0.0"x"')
    ws.auto_filter.ref = f"A4:O{n+4}"


REGUAS = [
    ("Cadastro incompleto", "Cadastral", "Começou o cadastro e não terminou"),
    ("Boas-vindas", "Cadastral", "Cadastro concluído"),
    ("Alteração / recuperação de senha", "Cadastral", "Pediu nova senha"),
    ("Carrinho abandonado", "Transacional", "Colocou no carrinho e não comprou"),
    ("Compra aprovada", "Transacional", "Pagamento aprovado"),
    ("Pagamento recusado", "Transacional", "Pagamento negado"),
    ("Pedido em preparação / enviado", "Transacional", "Mudou a situação do pedido"),
    ("Pedido entregue + cupom para a próxima compra", "Transacional", "Entrega confirmada"),
    ("Produto relacionado / upsell", "Transacional", "Dias depois da compra"),
    ("Preço baixou", "Transacional", "Produto visto ficou mais barato"),
    ("Voltou ao estoque (avise-me)", "Transacional", "Produto esgotado voltou"),
    ("Aniversário", "Relacional", "Data de aniversário"),
    ("Conteúdo de uso do produto", "Relacional", "Dias depois da entrega"),
    ("Conteúdo da categoria / dicas", "Relacional", "Periodicidade fixa"),
    ("Tempo desde a última compra (recompra)", "Relacional", "X dias sem comprar"),
    ("Reativação", "Relacional", "Muitos dias sem comprar ou abrir"),
    ("Frete grátis", "Promocional", "Campanha"),
    ("Promoção por produto / categoria", "Promocional", "Campanha"),
    ("Combos e kits", "Promocional", "Campanha"),
    ("Assinatura / compra recorrente", "Promocional", "Comprou 2 vezes o mesmo produto"),
    ("Lançamento", "Datas e campanhas", "Data do lançamento"),
    ("Datas do calendário (Mães, Pais, Namorados, Black Friday, Natal...)", "Datas e campanhas", "Ver aba Calendário"),
]


def aba_reguas(wb, cfg):
    ws = wb.create_sheet("Réguas de CRM")
    titulo(ws, "Réguas de CRM", "Catálogo das comunicações automáticas. Priorize: primeiro as transacionais, depois carrinho, boas-vindas e recompra.")
    cols = ["Régua", "Tipo", "Gatilho", "Canal (e-mail, WhatsApp, push, SMS)", "Ferramenta", "Responsável", "Status", "Prioridade", "Métrica principal", "Regra de saída", "Observações"]
    cabecalho(ws, 4, cols, [40, 18, 32, 22, 16, 14, 14, 10, 22, 26, 30])
    n = len(REGUAS) + 15
    for i, (nome, tipo, gat) in enumerate(REGUAS, start=5):
        ws.cell(row=i, column=1, value=nome)
        ws.cell(row=i, column=2, value=tipo)
        ws.cell(row=i, column=3, value=gat)
        ws.cell(row=i, column=7, value="Ideia")
    pintar(ws, f"A5:K{n+4}", FILL_ENTRADA)
    lista(ws, TIPO_REGUA, f"B5:B{n+4}")
    lista(ws, STATUS_REGUA, f"G5:G{n+4}")
    lista(ws, ["Alta", "Média", "Baixa"], f"H5:H{n+4}")
    ws.conditional_formatting.add(f"A5:K{n+4}", FormulaRule(formula=['$G5="Ativa"'], fill=PatternFill("solid", fgColor=VERDE)))
    ws.auto_filter.ref = f"A4:K{n+4}"


def aba_eventos(wb, cfg):
    ws = wb.create_sheet("Eventos e ativações")
    titulo(ws, "Eventos, ativações e materiais", "Uma linha por item de cada evento. O total por evento aparece no fim.")
    cols = ["Evento", "Data", "Item", "Descrição", "Fornecedor", "Quantidade", "Valor unitário", "Valor total", "Status", "Forma de pagamento", "Prazo de entrega", "Link da arte / comprovante"]
    cabecalho(ws, 4, cols, [22, 11, 22, 34, 18, 11, 13, 13, 12, 16, 14, 28])
    n = 80
    for r in range(5, n + 5):
        ws.cell(row=r, column=8, value=f'=IF(OR(F{r}="",G{r}=""),"",F{r}*G{r})')
    pintar(ws, f"A5:L{n+4}", FILL_ENTRADA)
    pintar(ws, f"H5:H{n+4}", FILL_CALCULO)
    lista(ws, STATUS_COMPRA, f"I5:I{n+4}")
    formato(ws, f"B5:B{n+4}", "DD/MM/YYYY")
    formato(ws, f"K5:K{n+4}", "DD/MM/YYYY")
    formato(ws, f"G5:H{n+4}", '"R$" #,##0.00')
    t = n + 6
    ws.cell(row=t, column=1, value="Total por evento").font = Font(bold=True, color=MARROM)
    ws.cell(row=t + 1, column=1, value="Evento").font = Font(bold=True)
    ws.cell(row=t + 1, column=2, value="Total").font = Font(bold=True)
    for k in range(t + 2, t + 12):
        ws.cell(row=k, column=1).fill = FILL_ENTRADA
        c = ws.cell(row=k, column=2, value=f'=IF(A{k}="","",SUMIF($A$5:$A${n+4},A{k},$H$5:$H${n+4}))')
        c.number_format = '"R$" #,##0.00'
        c.fill = FILL_CALCULO
    ws.cell(row=t + 12, column=1, value="Total geral").font = Font(bold=True)
    c = ws.cell(row=t + 12, column=2, value=f"=SUM(H5:H{n+4})")
    c.number_format = '"R$" #,##0.00'
    ws.auto_filter.ref = f"A4:L{n+4}"


def aba_brindes(wb, cfg):
    ws = wb.create_sheet("Brindes e estoque")
    titulo(ws, "Brindes e produtos para envios", "Controle o que sai para influenciadores, eventos e clientes. Fica vermelho quando chega no mínimo.")
    cols = ["Item", "Total comprado", "Enviados para influenciadores", "Usados em eventos", "Outros envios", "Estoque atual", "Estoque mínimo", "Observações"]
    cabecalho(ws, 4, cols, [26, 13, 16, 13, 12, 13, 13, 34])
    n = 30
    for r in range(5, n + 5):
        ws.cell(row=r, column=6, value=f'=IF(A{r}="","",N(B{r})-N(C{r})-N(D{r})-N(E{r}))')
    pintar(ws, f"A5:H{n+4}", FILL_ENTRADA)
    pintar(ws, f"F5:F{n+4}", FILL_CALCULO)
    ws.conditional_formatting.add(f"A5:H{n+4}", FormulaRule(formula=['AND($A5<>"",$G5<>"",$F5<=$G5)'], fill=PatternFill("solid", fgColor=VERMELHO)))

    r0 = n + 7
    ws.cell(row=r0, column=1, value="Lista de espera (produto esgotado / avise-me)").font = Font(bold=True, size=12, color=MARROM)
    for j, h in enumerate(["Primeiro nome", "Produto", "Data do pedido", "Avisado?"], start=1):
        c = ws.cell(row=r0 + 1, column=j, value=h)
        c.font = FONTE_CAB
        c.fill = FILL_CAB
    pintar(ws, f"A{r0+2}:D{r0+31}", FILL_ENTRADA)
    lista(ws, ["Sim", "Não"], f"D{r0+2}:D{r0+31}")
    formato(ws, f"C{r0+2}:C{r0+31}", "DD/MM/YYYY")


ABAS = {
    "tarefas": aba_tarefas,
    "calendario": aba_calendario,
    "concorrentes": aba_concorrentes,
    "influenciadores": aba_influs,
    "regras_parceria": aba_regras_influs,
    "demandas": aba_demandas,
    "briefing": aba_briefing,
    "criativos": aba_criativos,
    "reguas": aba_reguas,
    "eventos": aba_eventos,
    "brindes": aba_brindes,
}
ORDEM = ["tarefas", "calendario", "custos_preco", "concorrentes", "influenciadores", "regras_parceria", "demandas", "briefing", "criativos", "reguas", "eventos", "brindes"]


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("empresa", "Sua marca")
    cfg.setdefault("ano", date.today().year)
    escolhidas = cfg.get("abas") or ORDEM
    wb = Workbook()
    aba_como_usar(wb, cfg)
    for chave in ORDEM:
        if chave not in escolhidas:
            continue
        if chave == "custos_preco":
            n = aba_custos(wb, cfg)
            aba_preco(wb, cfg, n)
        else:
            ABAS[chave](wb, cfg)
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
    wb.save(sys.argv[2])
    print(f"Planilha criada: {sys.argv[2]} ({len(wb.worksheets)} abas: {', '.join(ws.title for ws in wb.worksheets)})")


if __name__ == "__main__":
    main()
