#!/usr/bin/env python3
"""Sanitiza fluxos do n8n (.json) antes de compartilhar.

Uso:
    python3 sanitizar_n8n.py entrada.json saida.json [--relatorio relatorio.txt]
    python3 sanitizar_n8n.py --pasta pasta_entrada pasta_saida
    Opções: --relatorio relatorio.txt   --nomes nomes.txt (uma troca por linha: Nome => Substituto)

O que faz:
- remove pinData (dados de teste com pessoas reais), staticData, meta.instanceId, id e versionId do fluxo
- troca IDs e nomes de credenciais, webhookId, errorWorkflow e caminhos de webhook com cara de ID
- troca e-mails, telefones, tokens longos, URLs de instalação do n8n e IDs numéricos de contas
  (5+ dígitos fora de expressões {{ }}) por textos de exemplo
- apaga o esquema de colunas cacheado das planilhas (traz nomes de campos de clientes)
- deixa o fluxo desativado (active: false)
- no fim, faz uma nova varredura e lista o que precisa de revisão humana (inclusive dentro de códigos)

Nada substitui a revisão humana: leia o relatório. E lembre: trocar um token por um texto de exemplo
NÃO invalida o token antigo. Se ele já circulou, gere um novo na ferramenta.

Criado por Jaqueline Amaro (CC BY-NC 4.0).
"""
import json
import os
import re
import sys

UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
EMAILS_OK = re.compile(r"(?i)(exemplo|example|seu|sua|postmaster@(desk\.)?msging\.net|noreply@)")
TEL = re.compile(r"(?<![\w.])\+?\(?(?:55)?\)?[\s-]?\(?\d{2}\)?[\s-]?9?\d{4}[\s-]?\d{4}(?![\w.])")
TOKEN = re.compile(r"(?<![A-Za-z0-9_\-])(?=[A-Za-z0-9_\-]*\d)(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{28,}(?![A-Za-z0-9_\-])")
N8N_URL = re.compile(r"https?://[^\s\"'/]+/webhook(-test)?/[A-Za-z0-9_\-]+")
GUID_IN_TEXT = re.compile(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}")
IPV4 = re.compile(r"(?<!\.)(?:\d{1,3}\.){3}\d{1,3}(?![.\d])")
DIGITOS = re.compile(r"(?<![\w$.])\d{5,}(?![\w])")
PLACEHOLDER = re.compile(r"(SEU|SUA|SEUS|SUAS)_[A-Z0-9_]+|_AQUI\b")
CHAVES_TECNICAS = {"id", "typeVersion", "position", "type", "webhookId"}
CHAVES_CODIGO = {"jsCode", "pythonCode", "code"}
NUMEROS_OK = {"1000000", "999999", "9000000000", "1000000000", "100000", "1000000000000"}


class Sanitizador:
    def __init__(self):
        self.trocas = []
        self.revisar = []

    def _troca(self, onde, antes, depois):
        if antes != depois:
            self.trocas.append((onde, antes[:80], depois[:80]))
        return depois

    def _fora_de_expressao(self, s, fn):
        """Aplica fn só nos trechos fora de {{ ... }}."""
        partes = re.split(r"(\{\{.*?\}\})", s, flags=re.S)
        return "".join(p if p.startswith("{{") else fn(p) for p in partes)

    def limpar_texto(self, s, onde):
        original = s
        if UUID.match(s.strip()):
            return self._troca(onde, s, "SEU_ID_AQUI")
        s = N8N_URL.sub("https://SUA_URL_N8N/webhook/SEU_WEBHOOK_PATH", s)
        s = IPV4.sub(lambda m: m.group(0) if m.group(0) in ("0.0.0.0", "127.0.0.1") else "0.0.0.0", s)
        s = EMAIL.sub(lambda m: m.group(0) if EMAILS_OK.search(m.group(0)) else "email@exemplo.com", s)
        if "docs.google.com" in s or "gid=" in s:
            s = re.sub(r"gid=\d+", "gid=SEU_GID_DA_ABA", s)
            s = re.sub(r"/spreadsheets/d/[A-Za-z0-9_\-]{20,}", "/spreadsheets/d/SEU_ID_DA_PLANILHA_GOOGLE", s)
        s = self._fora_de_expressao(s, lambda p: TOKEN.sub(lambda m: m.group(0) if PLACEHOLDER.search(m.group(0)) or UUID.match(m.group(0)) else "SEU_TOKEN_AQUI", p))
        s = self._fora_de_expressao(s, lambda p: TEL.sub("5511999999999", p))
        s = self._fora_de_expressao(s, lambda p: DIGITOS.sub("SEU_ID_AQUI", p))
        s = re.sub(r"(deal|contact|lead)_" + GUID_IN_TEXT.pattern, r"\1_SEU_CAMPO_AQUI", s)
        return self._troca(onde, original, s)

    def limpar_codigo(self, s, onde):
        """IDs de conta dentro de código viram 0 com comentário, sem quebrar o JavaScript."""
        original = s
        s = EMAIL.sub(lambda m: m.group(0) if EMAILS_OK.search(m.group(0)) else "email@exemplo.com", s)
        s = re.sub(r":(\s*)([A-Z][A-Z0-9]*_[A-Z0-9_]+)(\s*[,}\n])", lambda m: f":{m.group(1)}0 /* {m.group(2)} */{m.group(3)}" if PLACEHOLDER.search(m.group(2)) or m.group(2).startswith("ID_") else m.group(0), s)
        s = re.sub(r"(?<![\w.'\"])\d{6,}(?![\w'\"])", lambda m: m.group(0) if m.group(0) in NUMEROS_OK else "0 /* SEU_ID_AQUI */", s)
        return self._troca(onde, original, s)

    def revisar_codigo(self, s, onde):
        for pat, rot in ((EMAIL, "e-mail"), (TOKEN, "token"), (re.compile(r"(?<![\w.'\"])\d{7,}(?![\w'\"])"), "número longo")):
            for m in pat.finditer(s):
                v = m.group(0)
                if rot == "e-mail" and EMAILS_OK.search(v):
                    continue
                if rot == "número longo" and v in NUMEROS_OK:
                    continue
                if rot == "token" and (PLACEHOLDER.search(v) or UUID.match(v) or set(v) <= set("xy4-")):
                    continue
                self.revisar.append((onde, f"{rot} dentro de código: {v[:60]}"))

    def andar(self, o, caminho=""):
        if isinstance(o, dict):
            for k in list(o.keys()):
                v = o[k]
                onde = f"{caminho}/{k}"
                if k in CHAVES_TECNICAS and not isinstance(v, (dict, list)):
                    continue
                if k in CHAVES_CODIGO and isinstance(v, str):
                    o[k] = self.limpar_codigo(v, onde)
                    self.revisar_codigo(o[k], onde)
                    continue
                if k == "schema" and isinstance(v, list) and "columns" in caminho:
                    o[k] = []
                    self._troca(onde, "esquema de colunas", "removido")
                    continue
                if k == "cachedResultName" and isinstance(v, str):
                    o[k] = self._troca(onde, v, "Sua aba ou planilha")
                    continue
                o[k] = self.andar(v, onde)
            return o
        if isinstance(o, list):
            return [self.andar(v, caminho) for v in o]
        if isinstance(o, str):
            return self.limpar_texto(o, caminho)
        return o

    def sanitizar(self, fluxo):
        for k in ("pinData", "staticData"):
            if fluxo.get(k):
                self._troca(k, "dados salvos", "removido")
            fluxo.pop(k, None)
        fluxo["pinData"] = {}
        meta = fluxo.get("meta") or {}
        meta.pop("instanceId", None)
        fluxo["meta"] = meta
        for k in ("id", "versionId"):
            fluxo.pop(k, None)
        fluxo["active"] = False
        st = fluxo.get("settings") or {}
        if st.get("errorWorkflow") and not PLACEHOLDER.search(st["errorWorkflow"]):
            st["errorWorkflow"] = self._troca("settings/errorWorkflow", st["errorWorkflow"], "SEU_ID_WORKFLOW_DE_ERRO")
        for n in fluxo.get("nodes", []):
            nome = n.get("name", "")
            if n.get("webhookId"):
                n["webhookId"] = "SEU_WEBHOOK_ID"
            for cred in (n.get("credentials") or {}).values():
                cred["id"] = "SUA_CREDENCIAL_ID"
                if not str(cred.get("name", "")).startswith("[Reconfigurar]"):
                    cred["name"] = f"[Reconfigurar] {cred.get('name', 'Credencial')}"
            p = n.get("parameters") or {}
            if isinstance(p.get("path"), str) and (UUID.match(p["path"]) or re.fullmatch(r"[0-9a-f\-]{20,}", p["path"])):
                p["path"] = self._troca(f"{nome}/path", p["path"], "SEU_WEBHOOK_PATH")
            n["parameters"] = self.andar(p, nome)
        return fluxo

    def varredura_final(self, fluxo, arquivo):
        txt = json.dumps(fluxo, ensure_ascii=False)
        for m in EMAIL.finditer(txt):
            if not EMAILS_OK.search(m.group(0)) and m.group(0) != "email@exemplo.com":
                self.revisar.append((arquivo, f"e-mail: {m.group(0)}"))
        for m in re.finditer(r"(?i)(bearer\s+[A-Za-z0-9._\-]{20,}|sk-[A-Za-z0-9]{20,}|EAA[A-Za-z0-9]{30,}|xox[bp]-[A-Za-z0-9\-]+)", txt):
            self.revisar.append((arquivo, f"possível segredo: {m.group(0)[:40]}"))


def ler_nomes(caminho):
    """Arquivo com uma troca por linha: Nome original => Substituto (linhas com # são ignoradas)."""
    pares = []
    if caminho:
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=>" in linha:
                    a, b = (x.strip() for x in linha.split("=>", 1))
                    pares.append((a, b))
    return pares


def trocar_nomes(fluxo, pares, s):
    """Troca nomes (pessoas, empresas, clientes) em todo o fluxo, inclusive nomes de nós e referências."""
    if not pares:
        return fluxo
    txt = json.dumps(fluxo, ensure_ascii=False)
    for a, b in pares:
        padrao = re.compile(r"(?<![A-Za-zÀ-ÿ])" + re.escape(a) + r"(?![A-Za-zÀ-ÿ])")
        n = len(padrao.findall(txt))
        if n:
            txt = padrao.sub(b.replace("\\", "\\\\"), txt)
            s.trocas.append(("nomes", f"{a} ({n}x)", b))
    return json.loads(txt)


def processar(entrada, saida, relatorio=None, nomes=None):
    with open(entrada, encoding="utf-8") as f:
        fluxo = json.load(f)
    s = Sanitizador()
    fluxo = trocar_nomes(fluxo, nomes or [], s)
    fluxo = s.sanitizar(fluxo)
    s.varredura_final(fluxo, os.path.basename(entrada))
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(fluxo, f, ensure_ascii=False, indent=2)
    linhas = [f"# {os.path.basename(entrada)} → {os.path.basename(saida)}", f"Trocas: {len(s.trocas)}"]
    linhas += [f"  - {o}: {a!r} → {d!r}" for o, a, d in s.trocas]
    linhas.append(f"Para revisar: {len(s.revisar)}")
    linhas += [f"  ! {o}: {t}" for o, t in s.revisar]
    texto = "\n".join(linhas)
    if relatorio:
        with open(relatorio, "a", encoding="utf-8") as f:
            f.write(texto + "\n\n")
    return len(s.trocas), s.revisar


def main():
    args = sys.argv[1:]
    rel = None
    nomes = []
    if "--nomes" in args:
        i = args.index("--nomes")
        nomes = ler_nomes(args[i + 1])
        del args[i:i + 2]
    if "--relatorio" in args:
        i = args.index("--relatorio")
        rel = args[i + 1]
        del args[i:i + 2]
    if args and args[0] == "--pasta" and len(args) == 3:
        os.makedirs(args[2], exist_ok=True)
        for nome in sorted(os.listdir(args[1])):
            if nome.endswith(".json"):
                n, rev = processar(os.path.join(args[1], nome), os.path.join(args[2], nome), rel, nomes)
                print(f"{nome}: {n} trocas, {len(rev)} para revisar")
    elif len(args) == 2:
        n, rev = processar(args[0], args[1], rel, nomes)
        print(f"{n} trocas, {len(rev)} para revisar")
        for o, t in rev:
            print(f"  ! {o}: {t}")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
