"""Gera a página do cérebro em 3D a partir das fichas.

Uso:
    python3 -I gerar_cerebro_3d.py <pasta_do_cerebro> <saida.html> [--paleta neon] [--cores cores.json] [--titulo "meu cérebro"]

- <pasta_do_cerebro> tem a pasta fichas/ com subpastas por tema (cada .md é uma ficha).
- --paleta escolhe uma das paletas prontas de references/paletas.json.
- --cores usa um JSON com as cores da entrevista (mesmos campos das paletas).
Sem dependências externas.
"""
import argparse, json, pathlib, re

AQUI = pathlib.Path(__file__).resolve().parent.parent
NOMES = {'metodos': 'Métodos', 'decisoes': 'Decisões', 'visao': 'Visão', 'metricas': 'Métricas', 'preferencias': 'Preferências',
         'conteudo': 'Conteúdo', 'gestao': 'Gestão', 'ia': 'IA e ferramentas', 'lancamentos': 'Lançamentos', 'aprendizados': 'Aprendizados',
         'projetos': 'Projetos', 'entregas': 'Entregas', 'perfil': 'Perfil', 'vendas': 'Vendas'}


def hex_rgb(h):
    h = h.lstrip('#')
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def meta(t):
    d = {}
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    if m:
        for linha in m.group(1).splitlines():
            if ':' in linha:
                k, v = linha.split(':', 1)
                d[k.strip()] = v.strip()
    return d


def resumo(t):
    t = re.sub(r'^---\n.*?\n---\n', '', t, flags=re.S)
    out = []
    for l in t.splitlines():
        l = l.strip()
        if not l or l.startswith('#'):
            continue
        out.append(re.sub(r'^[-*]\s+', '', l).replace('**', ''))
        if len(out) == 3:
            break
    return out


def ler_fichas(raiz):
    temas = []
    base = raiz / 'fichas'
    for pasta in sorted(p for p in base.iterdir() if p.is_dir()) if base.exists() else []:
        fichas = []
        for f in sorted(pasta.glob('*.md')):
            if f.name.startswith('_'):
                continue
            t = f.read_text(encoding='utf-8')
            d = meta(t)
            m = re.search(r'^# (.+)$', t, re.M)
            fichas.append({'titulo': m.group(1).strip() if m else f.stem, 'resumo': resumo(t),
                           'privado': 'sim' in d.get('sensivel', '')})
        if fichas:
            temas.append({'nome': NOMES.get(pasta.name, pasta.name.replace('-', ' ').capitalize()), 'fichas': fichas})
    return temas


def css_e_cores(p):
    claro = bool(p.get('claro'))
    fundo_rgb = hex_rgb(p['fundo'])
    css = {
        'bg': p['fundo'], 'txt': p['texto'], 'mut': p['texto_suave'],
        'd1': p['destaque1'], 'd2': p['destaque2'], 'd3': p['destaque3'],
        'brilho1': f"rgba({hex_rgb(p['destaque1'])},.22)", 'brilho2': f"rgba({hex_rgb(p['destaque2'])},.10)",
        'grade': f"rgba({hex_rgb(p['destaque1'])},.14)", 'borda': f"rgba({hex_rgb(p['destaque1'])},.25)",
        'cartao': f"rgba({fundo_rgb},.72)" if not claro else 'rgba(255,255,255,.7)',
        'ficha': f"rgba({fundo_rgb},.85)" if not claro else '#fffdf6',
    }
    cores = {
        'claro': claro, 'halo': hex_rgb(p['destaque1']), 'linha': hex_rgb(p['destaque1']) if claro else hex_rgb(p['pontos']),
        'ponto': hex_rgb(p['pontos']), 'cerebelo': hex_rgb(p['cerebelo']), 'sinal': hex_rgb(p['destaque3']),
        'tema': hex_rgb(p['destaque2']), 'selecionado': hex_rgb(p['destaque3']),
        'nucleo': hex_rgb(p['texto']) if claro else '255,255,255', 'rotulo': p['texto'],
    }
    return ';'.join(f'--{k}:{v}' for k, v in css.items()), cores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta'); ap.add_argument('saida')
    ap.add_argument('--paleta', default='neon'); ap.add_argument('--cores'); ap.add_argument('--titulo', default='meu cérebro')
    a = ap.parse_args()
    paletas = json.loads((AQUI / 'references' / 'paletas.json').read_text(encoding='utf-8'))
    p = json.loads(pathlib.Path(a.cores).read_text(encoding='utf-8')) if a.cores else paletas[a.paleta]
    temas = ler_fichas(pathlib.Path(a.pasta))
    dados = {'temas': temas, 'total': sum(len(t['fichas']) for t in temas)}
    css, cores = css_e_cores(p)
    html = (AQUI / 'assets' / 'cerebro-3d.html').read_text(encoding='utf-8')
    html = html.replace('__CSS_VARS__', css).replace('__CORES__', json.dumps(cores)).replace('__DATA__', json.dumps(dados, ensure_ascii=False)).replace('__TITULO__', a.titulo)
    pathlib.Path(a.saida).write_text(html, encoding='utf-8')
    print(f"{dados['total']} fichas em {len(temas)} temas -> {a.saida}")


if __name__ == '__main__':
    main()
