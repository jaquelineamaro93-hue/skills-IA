# Segundo cérebro

Central de conhecimento para não perder o que você aprende: fichas por fonte, temas, decisões e um índice gerado todo mês.

## Checklist: o que você precisa
- [ ] Uma pasta (ou repositório privado) para as fichas
- [ ] Os temas da sua área (3 a 6)
- [ ] Uma IA com acesso à pasta, para consultar antes de decidir
- [ ] Python 3, para gerar o índice e a página 3D
- [ ] Node, Playwright e ffmpeg, só se quiser o GIF

## Como usar
1. Leia `SKILL.md`.
2. Crie a estrutura de `references/estrutura.md`.
3. Preencha a primeira ficha com `references/ficha-modelo.md`.
4. Gere o índice: `python3 -I scripts/gerar_indice.py . indice/INDICE.md`.
5. Marque a revisão mensal.
6. Para ver em 3D: responda a entrevista de cores e rode `python3 -I scripts/gerar_cerebro_3d.py . cerebro.html --paleta neon`.

## Licença
CC BY-NC 4.0, com crédito à autora. Veja `LICENSE.md`.
