"""Gera o índice da central de conhecimento.

Uso:
    python3 -I gerar_indice.py <raiz_do_repositorio> <saida.md>

Lista as skills (pastas com SKILL.md, com nome e descrição do cabeçalho)
e as fichas (arquivos .md dentro de fichas/, com tema e data do cabeçalho).
Não lê transcrições. Sem dependências externas.
"""
import pathlib
import re
import sys


def cabecalho(texto):
    m = re.match(r"^---\n(.*?)\n---", texto, re.S)
    dados = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                dados[chave.strip()] = valor.strip().strip('"')
    return dados


def skills(raiz):
    linhas = ["## Skills", ""]
    for skill in sorted(raiz.glob("*/SKILL.md")):
        d = cabecalho(skill.read_text(encoding="utf-8"))
        nome = d.get("name", skill.parent.name)
        desc = d.get("description", "").split(". ")[0]
        linhas.append(f"- **{nome}** (`{skill.parent.name}/`): {desc}")
    return linhas


def fichas(raiz):
    pasta = raiz / "fichas"
    linhas = ["", "## Fichas", ""]
    arquivos = sorted(pasta.rglob("*.md")) if pasta.exists() else []
    if not arquivos:
        linhas.append("_Nenhuma ficha ainda._")
    for f in arquivos:
        d = cabecalho(f.read_text(encoding="utf-8"))
        linhas.append(f"- {d.get('data', '')} · {d.get('tema', 'sem tema')} · {f.stem}")
    return linhas


def main():
    raiz = pathlib.Path(sys.argv[1])
    saida = pathlib.Path(sys.argv[2])
    linhas = ["# Índice da central de conhecimento", ""]
    linhas += skills(raiz)
    linhas += fichas(raiz)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"índice gerado em {saida}", file=sys.stderr)


if __name__ == "__main__":
    main()
